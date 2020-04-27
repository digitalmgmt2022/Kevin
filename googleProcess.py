from google_auth_oauthlib.flow import Flow
from google.oauth2 import service_account
from googleapiclient.discovery import build
import re,os

#----------------------------------------------------------------
                    #Support Functions
def read_paragraph_element(element):
    """Returns the text in the given ParagraphElement.
        Args:
            element: a ParagraphElement from a Google Doc.
    """
    text_run = element.get('textRun')
    if not text_run:
        return ''
    return text_run.get('content')

def read_strucutural_elements(elements):
    """Recurses through a list of Structural Elements to read a document's text where text may be
        in nested elements.

        Args:
            elements: a list of Structural Elements.
    """
    text = ''
    for value in elements:
        if 'paragraph' in value:
            elements = value.get('paragraph').get('elements')
            for elem in elements:
                text += read_paragraph_element(elem)
        elif 'table' in value:
            # The text in table cells are in nested Structural Elements and tables may be
            # nested.
            table = value.get('table')
            for row in table.get('tableRows'):
                cells = row.get('tableCells')
                for cell in cells:
                    text += read_strucutural_elements(cell.get('content'))
        elif 'tableOfContents' in value:
            # The text in the TOC is also in a Structural Element.
            toc = value.get('tableOfContents')
            text += read_strucutural_elements(toc.get('content'))
    return text
#----------------------------------------------------------------

def getvalue_excel(link_spreadsheet):
    spreadsheet_id=re.search("/spreadsheets/d/([a-zA-Z0-9-_]+)",link_spreadsheet).group().replace("/spreadsheets/d/","")
    #-------------------------------------------------------------------
                #Authorization and Getting Credentials for a Service Account
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    SERVICE_ACCOUNT_FILE = 'service_secrets.json'

    credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    #-------------------------------------------------------------------
                #Creating Build
    service=build('sheets','v4',credentials=credentials)

    #Geting Spreadsheet

    sheet=service.spreadsheets()
    result=sheet.values().get(spreadsheetId=spreadsheet_id,range="Jobs!A1:F200").execute()
    values = result.get('values', [])

    return values

def getvalue_docs(link_docs):
    doc_id=re.search("/document/d/([a-zA-Z0-9-_]+)",link_docs).group().replace("/document/d/","")
    #-------------------------------------------------------------------
                #Authorization and Getting Credentials for a Service Account
    SCOPES = ['https://www.googleapis.com/auth/documents.readonly']
    SERVICE_ACCOUNT_FILE = 'service_secrets.json'

    credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    #-------------------------------------------------------------------
                #Creating Build
    service=build('docs','v1',credentials=credentials)

    #Geting Spreadsheet
    docs=service.documents()
    document=docs.get(documentId=doc_id).execute()
    document_content=document.get('body').get('content')

    clean_content=read_strucutural_elements(document_content)
       
    return clean_content
