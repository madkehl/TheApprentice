from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import sys

urlMW = "https://app.metricwire.com/"
urlPitt = "https://my.pitt.edu"
urlSONA = "https://pitt.sona-systems.com/"

path_SBDL = "#root > div > main > div > div > div.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-12.MuiGrid-grid-sm-12.MuiGrid-grid-md-8 > div > div.MuiCardContent-root > table > tbody > tr:nth-child(2) > td:nth-child(3) > a > span.MuiButton-label"
path_EDL = "#root > div > main > div > div > div.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-12.MuiGrid-grid-sm-12.MuiGrid-grid-md-8 > div > div.MuiCardContent-root > table > tbody > tr:nth-child(1) > td:nth-child(3) > a > span.MuiButton-label"
pgconst_SBDL = 4
pgconst_EDL = 4

email_MW = ''
pass_MW = ''

email_Pitt = ''
pass_Pitt =''

email_SONA = ''
pass_SONA = ''

#MW funcs

def loginMetricWire(my_email = email_MW, my_passw = pass_MW, OS = 'Mac'):
    '''
    INPUT: str formatted username and password for MetricWire account
    
    OUTPUT: driver for next function, simply opens in a test browser
    '''
    driver = webdriver.Chrome()
    
    
    driver.get(urlMW)

    time.sleep(3)
    email_inp = driver.find_element_by_css_selector("#root > div > div > div > div > div > form > div:nth-child(4) > div > input")
    email_inp.send_keys(my_email)

    pass_inp = driver.find_element_by_css_selector("#root > div > div > div > div > div > form > div:nth-child(5) > div > input")
    pass_inp.send_keys(my_passw)

    login_btn = driver.find_element_by_css_selector("#root > div > div > div > div > div > form > div.card-action.border-0.text-right.mt-3 > button > span.MuiButton-label")
    login_btn.click()
    return(driver)

def openStudy(study_path, driver, pgconst):
    '''
    INPUT: path to workspace for study of interest
    
    OUTPUT: None, simply operates in test browser
    
    Notes: login must be run before running this 
    '''
    
    try:
        sbdl_wksp = driver.find_element_by_css_selector(study_path)
        sbdl_wksp.click()
    except:
        time.sleep(3)
        sbdl_wksp = driver.find_element_by_css_selector(study_path)
        sbdl_wksp.click()

    time.sleep(1)
    sbdl_study = driver.find_element_by_css_selector("#root > div > main > div > div.MuiGrid-root.MuiGrid-container.MuiGrid-spacing-xs-4 > div:nth-child(2) > a > div > div > div.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-8")
    sbdl_study.click()

    time.sleep(1)
    sbdl_view = driver.find_element_by_css_selector("#root > div > main > div > div > div > div > table > tbody > tr > td:nth-child(4) > a > button > span.MuiButton-label")
    sbdl_view.click()

    time.sleep(5)
    part_btn = driver.find_element_by_css_selector("#root > div > main > div > div > header > div > div > div > div > div > button:nth-child(6)")
    part_btn.click()

    time.sleep(7)

    expand_btn = driver.find_element_by_xpath("/html/body/div[1]/div/main/div/div/div/div/div[2]/div/div/div/table/tfoot/tr/td/div/div[2]/div")
    expand_btn.click()

    sel300 = driver.find_element_by_xpath("/html/body/div[" + str(pgconst) + "]/div[3]/ul/li[3]")
    sel300.click()
    return(driver)

def get_emails(date, driver):
    '''
    INPUT: date of enrollment that you are interested in grabbing
    
    OUTPUT: result list of email and number of submissions
    '''
    table = driver.find_element_by_css_selector('#root > div > main > div > div > div > div > div.MuiPaper-root.MuiCard-root.MuiPaper-elevation1.MuiPaper-rounded > div > div > div > div.jss97 > div > div > div > table > tbody')

#iterate through participants

    participant_email = []
    participant_subm = []
    for row in table.find_elements_by_css_selector('tr'):
        try:
            row_num = row.get_attribute("index")
            try:
                enroll_date = driver.find_element_by_css_selector('#root > div > main > div > div > div > div > div.MuiPaper-root.MuiCard-root.MuiPaper-elevation1.MuiPaper-rounded > div > div > div > div.jss97 > div > div > div > table > tbody > tr:nth-child(' + str(row_num) + ') > td:nth-child(10)')
            except:
                time.sleep(3)
                enroll_date = driver.find_element_by_css_selector('#root > div > main > div > div > div > div > div.MuiPaper-root.MuiCard-root.MuiPaper-elevation1.MuiPaper-rounded > div > div > div > div.jss97 > div > div > div > table > tbody > tr:nth-child(' + str(row_num) + ') > td:nth-child(10)')
            
            if enroll_date.text[:10] == date:
                email_ob = driver.find_element_by_css_selector('#root > div > main > div > div > div > div > div.MuiPaper-root.MuiCard-root.MuiPaper-elevation1.MuiPaper-rounded > div > div > div > div.jss97 > div > div > div > table > tbody > tr:nth-child(' + str(row_num) + ') > td:nth-child(5)')
                email = email_ob.text.split('@')[0]
                print(email)
                participant_email.append(email)
        
                launch_btn = driver.find_element_by_css_selector('#root > div > main > div > div > div > div > div.MuiPaper-root.MuiCard-root.MuiPaper-elevation1.MuiPaper-rounded > div > div > div > div.jss97 > div > div > div > table > tbody > tr:nth-child(' + str(row_num) + ') > td:nth-child(7) > a')
                participant_link = launch_btn.get_attribute('href')
        
                driver.execute_script("window.open('{}');".format(participant_link))
                driver.switch_to.window(driver.window_handles[1])
                time.sleep(3)
                try:
                    fullsched_btn = driver.find_element_by_css_selector('#root > div > main > div > div > div.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-8 > div > div > div > div > div > div > div:nth-child(1) > div > div:nth-child(2) > div > button')
                    fullsched_btn.click()
                except:
                    time.sleep(3)
                    fullsched_btn = driver.find_element_by_css_selector('#root > div > main > div > div > div.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-8 > div > div > div > div > div > div > div:nth-child(1) > div > div:nth-child(2) > div > button')
                    fullsched_btn.click()
                time.sleep(2)
                submissions = driver.find_element_by_css_selector('#root > div > main > div > div > div.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-8 > div > div > div > div > div > div > div.MuiCardContent-root.text-xs-center > div > div:nth-child(4) > h3').text
                print(submissions)
                participant_subm.append(submissions)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
        except:
            pass
    return(participant_email, participant_subm)
        
def full_email_path(study_path, date, pgconst, cutoff, OS):
    '''
    INPUT: study_path, date of enrollment
    
    OUTPUT: result df
    
    Runs everything above in sequence
    '''
    driver = loginMetricWire(OS = OS)
    driver =openStudy(study_path, driver, pgconst)
    participant_email, participant_subm = get_emails(date, driver)
    
    results = pd.DataFrame({
    
        'email': participant_email,
        'surveys': participant_subm,
        'credit': [1 if int(i) > cutoff else 0 for i in participant_subm],
        'action': [float('nan') for i in participant_subm]
    
        })
    return results


### login pitt_email
def loginPitt(email = email_Pitt, passw = pass_Pitt):
    '''
    INPUT: user credentials
    
    OUTPUT: driver
    
    logs in to Pitt
    
    '''
    driver = webdriver.Chrome()
    driver.get(urlPitt)

    menu_btn = driver.find_element_by_id("headerMenuDropdown")
    menu_btn.click()

    signin_btn = driver.find_element_by_xpath("/html/body/div[1]/div[4]/section[1]/div/nav/div/div[2]/ul/li[2]/ul/li[1]/a")
    signin_btn.click()

    username = driver.find_element_by_xpath("/html/body/div/div/div[1]/div/form/div[1]/input")
    username.send_keys(email)

    password =  driver.find_element_by_xpath("/html/body/div/div/div[1]/div/form/div[2]/input")
    password.send_keys(passw)

    submit_btn = driver.find_element_by_xpath("/html/body/div/div/div[1]/div/form/button")
    submit_btn.click()

    
    print('PLEASE CONFIRM IN BROWSER')
    key_pressed = input('Press ENTER to continue: ')
    

    return(driver)

def openOutlook(driver):
    '''
    INPUT:driver
    
    OUTPUT: driver
    
    '''
    
    time.sleep(5)
    email_btn = driver.find_element_by_xpath("/html/body/div[1]/div[5]/div[3]/div/div[2]/div[2]/div[3]/div[1]/div/div/a")
    email_btn.click()
    driver.switch_to.window(driver.window_handles[1])
    
    time.sleep(3)    
    email_search_activate = driver.find_element_by_id("searchBoxId-Mail")
    email_search_activate.click()
    email_search = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div/div[1]/div[2]/div/div/div/div/div[1]/div[2]/div/div/div/div/div[1]/div/div[2]/div/input")
    search_btn = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div/div[1]/div[2]/div/div/div/div/div[1]/div[2]/div/div/div/div/div[1]/button")
    
    return driver, email_search, email_search_activate

def return_name(email, driver, email_search, email_search_activate, OS):
    '''
    takes an email and gets name
    '''
    email_search.send_keys(email)
    email_search_activate.click()
    time.sleep(5)
    try:
        results = driver.find_element_by_id("searchSuggestionsCallout")
        soup = BeautifulSoup(results.get_attribute('innerHTML'), 'html.parser')
        name = soup.find("div", {"id":"searchSuggestion-0" })['aria-label']
        
        if OS == 'MAC':
            email_search.send_keys(Keys.COMMAND + "a")
        else:
            email_search.send_keys(Keys.CONTROL + "a")
            
        email_search.send_keys(Keys.DELETE)
        
        return(name, driver)
    except:
        if OS == 'MAC':
            email_search.send_keys(Keys.COMMAND + "a")
        else:
            email_search.send_keys(Keys.CONTROL + "a")
            
        email_search.send_keys(Keys.DELETE)
        
        return('NONE', driver)


def full_path_to_names(ids, OS):
    '''
    INPUT: id df
    
    OUTPUT: df of emails and names 
    '''
    ids = ids[ids['action'].isnull()]
    emails = ids['email'].values
    driver = loginPitt()
    time.sleep(3)
    driver, email_search, email_search_activate = openOutlook(driver)
    name_ls = []
    for i in emails:
        name = return_name(i, driver, email_search, email_search_activate, OS)[0]
        
        print(name)
        name_ls.append(name)
        
    emails2names = pd.DataFrame({
        'email': emails, 
        'name': name_ls,
        'credit': ids['credit'],
        'action': ids['action']
    })
    
    return(emails2names)

###SONA script

def transform(name):
    '''
    takes names as given from the other script and cleans them
    '''
    name_s = name.split(',')
    try:
        new_name = name_s[1] + ' ' + name_s[0]
    except:
        print('WEIRD NAME ENTRY')
        new_name = name_s[0]
    return(new_name.lstrip())

def sonaLogin(email, passw):
    '''
    INPUT: user credentials
    
    OUTPUT: webdriver
    '''
    driver = webdriver.Chrome()
    driver.get(urlSONA)

    username = driver.find_element_by_xpath("/html/body/form/div[3]/section/section/section/div[2]/div[1]/section/div/div/div/div/input[1]")
    username.send_keys(email)

    password =  driver.find_element_by_xpath("/html/body/form/div[3]/section/section/section/div[2]/div[1]/section/div/div/div/div/input[2]")
    password.send_keys(passw)

    submit_btn = driver.find_element_by_xpath("/html/body/form/div[3]/section/section/section/div[2]/div[1]/section/div/div/div/div/input[3]")
    submit_btn.click()

    to_credit = driver.find_element_by_xpath("/html/body/form/div[3]/section/section/section/div[2]/div[1]/section[1]/div/a[3]")
    to_credit.click()
    
    return(driver)

def give_credit(driver, study_name, keys):
    '''
    INPUT: study_name, webdriver
    
    OUTPUT: none, makes edits to sona credit options
    
    iterates through table, assesses if it matches study, locates name cell, checks table to see if credit updates,
    then marks the appropriate box
    
    Submit is not automated to allow for spot checks
    '''
    credits = driver.find_element_by_css_selector('#no-more-tables > table')

#iterate through participants
    row_num = 0
    for row in credits.find_elements_by_css_selector('tr'):
        isSBDL = False
        keep_next = False
        checked_credit = False
        gets_credit = False
    
    #iterate through row
        for cell in row.find_elements_by_tag_name('td'):
        #make sure it is sbdl
            if cell.text == study_name:
                isSBDL = True
                print('isSBDL')
        #placeholder
            elif 'Online study' in cell.text and isSBDL == True:
                keep_next = True
        #check credit
            elif keep_next == True:
            
                key = cell.text
                print(key + ' NOW SEARCHING')
                part_row = keys[keys['cleanname'] == key]
            
                if len(part_row) > 0:
                    print(key + ' FOUND')
                    if part_row['credit'].mean() == 1:
                        gets_credit = True
                    checked_credit = True
                else:
                    print(key + ' NOT FOUND')
            
            
                keep_next = False
            
            elif checked_credit == True:
                time.sleep(2)
                if gets_credit == True:
                    grant_credit = driver.find_element_by_xpath('//tr[' + str(row_num) + ']/td[5]/div/label[2]/label')
                    print(key + ' GRANT')
                    time.sleep(1)
                    grant_credit.click()
                else:
                    time.sleep(1)
                    ens = driver.find_element_by_xpath('//tr[' + str(row_num) + ']/td[5]/div/label[4]/label')
                    print(key + ' ENS')
                    ens.click()
        row_num += 1
    key_pressed = input('Press ENTER to continue: ')
    return

def full_path_credit(keys, study_name, email = email_SONA, passw = pass_SONA):
    keys['cleanname'] = keys['name'].apply(transform)
    driver = sonaLogin(email,passw)
    give_credit(driver, study_name, keys)
    

def main(study, date, OS):
    print(study)
    if study == 'EDL':
        print('edl in progress')
        study_path = path_EDL
        pgconst = pgconst_EDL
        study_name = 'Emotions in Daily Life'
        cutoff = 32
    elif study == 'SBDL':
        print('sbdl in progress')
        study_path = path_SBDL
        pgconst = pgconst_EDL
        study_name = 'Social Behavior in Daily Life Study'
        cutoff = 24
    else:
        print('not a valid study')
        return
    ids = full_email_path(study_path, date, pgconst, cutoff, OS)
    keys = full_path_to_names(ids, OS)
    full_path_credit(keys, study_name)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print('MISSING REQUIRED ARGUMENT.  CHECK IF STUDY_NAME, DATE, OS')
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
