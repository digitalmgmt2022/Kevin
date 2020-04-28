import time,os,requests,sys,csv,platform,json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

#Auxiliary Functions
from googleProcess import getvalue_excel,getvalue_docs
from functions import setcompleted_jobs,idcompleted

#Identify platform
platform_system=platform.platform()

#Options
options = Options()
options.add_argument("--headless") # Runs Chrome in headless mode.
options.add_argument('--no-sandbox') # Bypass OS security model
options.add_argument('--disable-gpu')  #gpu windows only
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")

#Init Chrome Driver
if "Linux" in platform_system:
  navegador=webdriver.Chrome(executable_path="chromedriver",chrome_options=options)
else:
  navegador=webdriver.Chrome(executable_path=os.getcwd()+"\\chromedriver.exe",chrome_options=options)

navegador=webdriver.Chrome(executable_path=os.getcwd()+"\\chromedriver.exe")
navegador.maximize_window()


#----------------------------------------------------------------------------------------------------------
                                        #Function Support
def waitByID(ElementID,time_wait,navegador=navegador,extratime=0):
    """ This Function is used to wait a element with an ID=ElementID. 
        It will wait for the element during the time=time_wait
    """
    while True:
        try:
            try:
                WebDriverWait(navegador,time_wait).until(
                    EC.presence_of_element_located((By.ID,ElementID))
                )
                time.sleep(extratime)
                return navegador.find_element_by_id(ElementID)
            except:
                print("The element with ID:  "+ElementID+" does not appeared within "+str(time_wait))
                return "Element not found"
        except:
            print("Waiting for element...")

def waitByName(ElementName,time_wait,navegador=navegador,extratime=0):
    """ This Function is used to wait a element with an ID=ElementID. 
        It will wait for the element during the time=time_wait
    """
    while True:
        try:
            try:
                WebDriverWait(navegador,time_wait).until(
                    EC.presence_of_element_located((By.NAME,ElementName))
                )
                time.sleep(extratime)
                return navegador.find_element_by_name(ElementName)
            except Exception as e:
                print("The element with Name:  "+ElementName+" does not appeared within "+str(time_wait))
                return "Element not found"
        except:
            print("Waiting for element...")

def waitByXpath(ElementXpath,time_wait,navegador=navegador,extratime=0):
    """ This Function is used to wait a element with an Xpath=ElementXpath.
        It will wait for the element during the time=time_wait.
    """
    while True:
        try:
            try:
                WebDriverWait(navegador,time_wait).until(
                    EC.presence_of_element_located((By.XPATH,ElementXpath))
                )
                time.sleep(extratime)
                return navegador.find_element_by_xpath(ElementXpath)
            except:
                print("The element with Xpath:  "+ElementXpath+" does not appeared within "+str(time_wait))
                return "Element not found"
        except:
            print("Waiting for element...")

def waitElementsBycssSelector(cssSelector,time_wait,navegador=navegador,extratime=0):
    """ This Function is used to wait for elements with a cssSelector=cssSelector.
        It will wait for the elements during the time=time_wait.
    """
    while True:
        try:
            try:
                WebDriverWait(navegador,time_wait).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR,cssSelector))
                )
                time.sleep(extratime)
                return navegador.find_elements_by_css_selector(cssSelector)
            except:
                print("The elements with cssSelector:  "+cssSelector+" does not appeared within "+str(time_wait))
                return "Element not found"
        except:
            print("Waiting for element...")

def waitElementsByTagName(tagName,time_wait,navegador=navegador,extratime=0):
    """ This Function is used to wait for elements with a html tag=tagName
        It will wait for the elements during the time=time_wait.
    """
    while True:
        try:
            try:
                WebDriverWait(navegador,time_wait).until(
                    EC.presence_of_element_located((By.TAG_NAME,tagName))
                )
                time.sleep(extratime)
                return navegador.find_elements_by_tag_name(tagName)
            except:
                print("Elements with tag: "+tagName+" does not appeared within "+str(time_wait))
                return "Element not found"
        except:
            print("Waiting for element...")

#---------------------------------------------------------------------
                    #Getting Credentials Google Hire
credeitials_json=json.loads(open("googlehire_credentials.json").read())

while True:
    try:
        #----------------------------------------------------------------------
                    #Getting Information from Google Drives
        ids=idcompleted()
        jobs=getvalue_excel(credeitials_json["sheeturl"])
        jobs=[job for job in jobs if (job[0] not in [""," "]) and (job[3] not in ids)]
        jobs.pop(0)
        #---------------------------------------------------------------------
                            # GETTING INTO LINK
        #Getting to google hire
        navegador.get("https://hire.withgoogle.com/t/theadmasterscom/hiring/jobs?sortBy=status&sortDescending=false&scope=all&position-status=open")
        #---------------------------------------------------------------------- 
                            #LOGIN PROCESS
        #1- Goes into url
        buttons=waitElementsByTagName("a",20)
        for button in buttons:
            if "Sign in" in button.text:
                button.click()
                break

        #2- Typing Email
        waitByID("identifierId",20).send_keys(credeitials_json["user"]+"\n") 
        #waitByID("identifierNext",20).click() #identifierNext

        #3- Type password
        waitByName(ElementName="password",time_wait=20,extratime=2).send_keys(credeitials_json["password"]+"\n")
        #waitByID("passwordNext",20).click() #identifierNext
        #---------------------------------------------------------------------- 
                            #CREATING JOBS IN google hire
        for job in jobs:

            #Click in Job
            print("click in job")
            inputs=waitElementsByTagName(tagName="a",time_wait=20,extratime=8)
            for inputelement in inputs:
                textelement=inputelement.text
                textelement=textelement.lower()
                if ("jobs" in textelement) and ("view" not in textelement) and ("create" not in textelement):
                    inputelement.click()
                    break

            #Click in Create a Job
            while True:
                end_loop=False
                buttons=waitElementsByTagName("button",120)
                for button in buttons:
                    if "Create job" in button.text:
                        button.click()
                        end_loop=True
                        break
                if end_loop:
                    break
            
            #---------Filling the form--------
            #time.sleep(5)
            form=waitByName(ElementName="model.createJobForm",time_wait=30,extratime=10)
            #1- Job Title
            inputs=waitElementsByTagName("input",20,form)
            for inputelement in inputs:
                if "add title" in inputelement.get_attribute("placeholder").lower():
                    inputelement.send_keys(job[0])
                    break
            
            #2- Aplication Form
            try:
                aplicationform=waitByName(ElementName="application-form",time_wait=20,navegador=form)
                inputs=waitElementsByTagName("input",20,aplicationform)
                print(str(len(inputs)))
                inputs[0].send_keys("Resume optional")
            except:
                aplicationform=waitByXpath("/html/body/div[3]/div/bb-dialog/form/bb-dialog-content/bb-wizard/div[2]/div[1]/div/div/div[2]/bb-combobox/fieldset/button/span/input",20,form)
                aplicationform.send_keys("Resume optional")

            #3- Location
            inputs=waitElementsByTagName("input",20,form)
            for inputelement in inputs:
                if "enter addres" in inputelement.get_attribute("placeholder").lower():
                    inputelement.send_keys(job[2])
                    time.sleep(2)
                    inputelement.send_keys(Keys.RETURN)
                    break

            #4- Next
            buttons=waitElementsByTagName("button",20,form)
            for button in buttons:
                textbutton=button.text
                textbutton=textbutton.lower()
                if "next" in textbutton:
                    time.sleep(2)
                    button.click()
                    break

            #5- Pasting Job Description
            jobdescription=getvalue_docs(job[1])
            try:
                textboxs=waitElementsByTagName("TRIX-EDITOR",20,form)
                for box in textboxs:
                    text_placeholder=box.get_attribute("placeholder").lower()
                    if "please describe the day" in text_placeholder:
                        box.send_keys(jobdescription)
            except:
                waitByID(ElementID="bb-rich-text-editor-91",time_wait=20,extratime=2).send_keys(jobdescription)

            #6- Next
            buttons=waitElementsByTagName("button",20,form)
            for button in buttons:
                textbutton=button.text
                textbutton=textbutton.lower()
                if "next" in textbutton:
                    button.click()
                    break
            
            time.sleep(5)

            #7- Next
            buttons=waitElementsByTagName("button",20,form)
            for button in buttons:
                textbutton=button.text
                textbutton=textbutton.lower()
                if "next" in textbutton:
                    button.click()
                    break

            time.sleep(5)

            #8- Create a job
            buttons=waitElementsByTagName("button",20,form)
            for button in buttons:
                textbutton=button.text
                textbutton=textbutton.lower()
                print(textbutton)
                if "create j" in textbutton:
                    button.click()
                    break

            time.sleep(5)

            #9- View Job
            buttons=waitElementsByTagName("button",20)
            for button in buttons:
                textbutton=button.text
                textbutton=textbutton.lower()
                if "view job" in textbutton:
                    button.click()
                    break
            
            time.sleep(10)

            #10- Publish Job
            buttons=waitElementsByTagName("button",60)
            for button in buttons:
                textbutton=button.text
                textbutton=textbutton.lower()
                if "publish" in textbutton:
                    button.click()
                    break

            time.sleep(5)
            print("Selection Clasification")
            #11- Selection Clasification
            inputs=waitElementsByTagName("input",60)
            for inputelement in inputs:
                try:
                    textbutton=inputelement.get_attribute("placeholder").lower()
                except:
                    textbutton="na"
                if "choose" in textbutton:
                    inputelement.send_keys(job[4]+"\n")
                    break

            #12- Publish Job
            time.sleep(8)
            print("Publishing")
            buttons=waitElementsByTagName("button",20)
            for button in buttons:
                textbutton=button.text
                textbutton=textbutton.lower()
                if "publish" in textbutton:
                    button.click()
                    break
            
            time.sleep(5)
            #13- Click on Done
            buttons=waitElementsByTagName("button",20)
            for button in buttons:
                textbutton=button.text
                textbutton=textbutton.lower()
                if "done" in textbutton:
                    button.click()
                    break

            time.sleep(5)
            setcompleted_jobs(job[0],job[1],job[2],job[3])
            #---------------------------------
        #---------------------------------------------------------------------- 
    except Exception as e:
        print("Error In the global process")
        navegador.close()
        print("-------------------------------------\n")
        print(str(e))
        print("-------------------------------------\n")

        #Delete Navegador
        del(navegador)

        print("Start over again")
        time.sleep(15)
        #Init Chrome Driver
        if "Linux" in platform_system:
            navegador=webdriver.Chrome(executable_path="chromedriver",chrome_options=options)
        else:
            navegador=webdriver.Chrome(executable_path=os.getcwd()+"\\chromedriver.exe",chrome_options=options)

        navegador=webdriver.Chrome(executable_path=os.getcwd()+"\\chromedriver.exe")
        navegador.maximize_window()