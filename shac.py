import requests
import re
import hashlib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
def get_md5(input_string):

  # Encode the input string as bytes
  input_bytes = input_string.encode()

  # Create a new hash object
  hash_object = hashlib.md5()

  # Update the hash object with the input bytes
  hash_object.update(input_bytes)

  # Get the hexadecimal representation of the hash
  hash_hex = hash_object.hexdigest()

  return hash_hex
# foundConfLink = False
apiKeys = ['JQyIuHfKwbCdsSsUR1SrmakO5Lk8ZEq0'
,'mjCd0coUfwOxDH1vpkZiGpWEFvrRPGV6']
currentAPIKeyN = 0
foundAWorkingApiKey = False
currentAPIKey = apiKeys[currentAPIKeyN]
def apikeyChanger():
    global currentAPIKeyN
    currentAPIKeyN += 1
def confirmEmail(email):
    global  usernameBeingUsed, emailBeingUsed, foundAWorkingApiKey, currentAPIKey
    foundConfLink = False
    url = "https://api.apilayer.com/temp_mail/mail/id/%s" % get_md5(email)
    payload = {}
    headers= {
    "apikey": currentAPIKey
    }
    response = requests.request("GET", url, headers=headers, data = payload)
    status_code = response.status_code

    while status_code == 429:
            apikeyChanger()
            currentAPIKey = apiKeys[currentAPIKeyN]
            print('[+] attempting to change api key to %s:%s' %(currentAPIKey, status_code))
            
            response = requests.request("GET", url, headers=headers, data = payload)
            status_code = response.status_code
            if status_code == 200:
                print('[+] found a working apikey %s:%s' %(currentAPIKey, status_code))
                foundAWorkingApiKey = True
                break
            else:
                print('[+] still looking for apikey %s:%s' %(currentAPIKey, status_code))
 

    
    resp = response.text
    print(status_code)
    while foundConfLink != True:
        activationLink = re.search(r'https:\/\/account.shodan.io\/[^"]*', resp)
        if activationLink != None:
            print('[+] attempting to find confirmation link')
            activationLink = re.search(r'https:\/\/account.shodan.io\/[^"]*', resp).group()
            foundConfLink = True
        else:
            response = requests.request("GET", url, headers=headers, data = payload)
            resp = response.text


    # foundConfLink = False
    return activationLink.replace('\\','')

usernameGenCounter = 700


def usernameGen():
    global usernameGenCounter
    usernameGenCounter +=1
    base_uname = 'tmux0x0'
    return base_uname + str(usernameGenCounter)
password = '472002Mm@123'
def emailGenerator():
    global usernameBeingUsed
    baseMail = 'tmux0x0' + str(usernameGenCounter) + '@cevipsa.com'
    return baseMail

options = Options()
# options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
# driver = webdriver.Chrome(options=options)
emailBeingUsed = ''
usernameBeingUsed = ''
for x in range (1,300):
    # options = Options()
    # options.add_argument('--headless')
    # driver = webdriver.Chrome(options=options)
    driver.delete_all_cookies()
    # driver.execute_script("window.localStorage.clear();")
    usernameBeingUsed = usernameGen()
    emailBeingUsed = emailGenerator()
    print('[+] Attempting to create %s:%s:%s' %(usernameBeingUsed,password,emailBeingUsed))

    driver.get("https://account.shodan.io/register")
    uname_field = driver.find_element(By.XPATH,'//*[@id="username"]')
    uname_field.send_keys(usernameBeingUsed)
    pwd_field = driver.find_element(By.XPATH,'//*[@id="password"]')
    pwd_field.send_keys(password)
    cpwd_field = driver.find_element(By.XPATH,'//*[@id="password_confirm"]')
    cpwd_field.send_keys(password)
    email_field = driver.find_element(By.XPATH,'//*[@id="email"]')
    email_field.send_keys(emailBeingUsed)
    email_field.send_keys(Keys.ENTER)
    time.sleep(2)
    driver.get(confirmEmail(emailBeingUsed))
    driver.get("https://account.shodan.io/login?continue=http%3A%2F%2Fwww.shodan.io%2Fdashboard")
    uname_field = driver.find_element(By.XPATH,'//*[@id="username"]')
    uname_field.send_keys(usernameBeingUsed)
    pwd_field = driver.find_element(By.XPATH,'//*[@id="password"]')
    pwd_field.send_keys(password)
    time.sleep(5)

    pwd_field.send_keys(Keys.ENTER)
    time.sleep(5)

    cookies = driver.get_cookies()

    print('[+] Created ' + usernameBeingUsed+','+password+','+emailBeingUsed+','+cookies[0]['value'])
    with open('shodan-accounts.txt', 'a') as f: f.write(usernameBeingUsed+','+password+','+emailBeingUsed+','+cookies[0]['value']+'\n')
    # driver.close()
    driver.get('https://account.shodan.io/logout')
    # driver.delete_all_cookies()
    # driver.execute_script("window.localStorage.clear();")