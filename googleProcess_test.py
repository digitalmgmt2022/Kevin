from google_auth_oauthlib.flow import Flow
from google.oauth2 import service_account
from googleapiclient.discovery import build

def getvalue_excel():
    #-------------------------------------------------------------------
                #Authorization and Getting Credentials for a Service Account
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    SERVICE_ACCOUNT_FILE = 'service_secrets.json'

    credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    print("ok")

    #-------------------------------------------------------------------
                #Creating Build
    service=build('sheets','v4',credentials=credentials)

    #Geting Spreadsheet

    sheet=service.spreadsheets()
    result=sheet.values().get(spreadsheetId="17-oPWMYYx4TeZ_JkgGmSC9bcn2YhLjQlacETBXX_Zoc",range="Jobs!A1:B20").execute()
    values = result.get('values', [])

    return values