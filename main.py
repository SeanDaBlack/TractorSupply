from faker import Faker
import random
import requests
import time
from webdriver_manager.chrome import ChromeDriverManager
# from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from select_store import select_store, find_store_on_yelp
MAIL_GENERATION_WEIGHTS = [1, 0.95, 0.7, 0.75, 0.7, 0.5]


fake = Faker()


def random_email(name=None):
    if name is None:
        name = fake.name()

    mailGens = [lambda fn, ln, *names: fn + ln,
                lambda fn, ln, *names: fn + "_" + ln,
                lambda fn, ln, *names: fn[0] + "_" + ln,
                lambda fn, ln, *names: fn + ln +
                str(int(1 / random.random() ** 3)),
                lambda fn, ln, *names: fn + "_" + ln +
                str(int(1 / random.random() ** 3)),
                lambda fn, ln, *names: fn[0] + "_" + ln + str(int(1 / random.random() ** 3)), ]

    return random.choices(mailGens, MAIL_GENERATION_WEIGHTS)[0](*name.split(" ")).lower() + "@" + requests.get(
        'https://api.mail.tm/domains').json().get('hydra:member')[0].get('domain')

def createFakeIdentity():
    fake_identity = {}
    fake_identity['first_name'] = fake.first_name()
    fake_identity['last_name'] = fake.last_name()
    fake_identity['email'] = random_email(
        fake_identity['first_name'] + ' ' + fake_identity['last_name'] + str(random.randint(1, 999999)))
    fake_identity['password'] = fake.password()
    fake_identity['zip'] = random.randint(10000,99999)

    return fake_identity

def createMail(fake_identity):
    # Create Email with MailTM

    # ran_email = random_email(
    #     fake_identity['first_name'] + ' ' + fake_identity['last_name'] + str(random.randint(1, 99999)))

    print(f"USING MAILTM TO CREATE EMAIL")
    fake_email = requests.post('https://api.mail.tm/accounts', data='{"address":"'+fake_identity["email"]+'","password":" "}', headers={
        'Content-Type': 'application/json'}).json().get('address')
    mail_sid = requests.post('https://api.mail.tm/token', data='{"address":"'+fake_identity["email"]+'","password":" "}', headers={
        'Content-Type': 'application/json'}).json().get('token')

    fake_identity['sid'] = mail_sid
    fake_identity['email'] = fake_email
    print(f"EMAIL CREATED")

    return fake_identity

def start_driver(url):

    # if (args.cloud == CLOUD_ENABLED):

#     #driver = geckodriver("./extensions/Tampermonkey.xpi")
    options = webdriver.ChromeOptions()
    
    service = Service(ChromeDriverManager().install())
    
    
#     options.add_argument('--headless')
#     options.add_argument('--no-sandbox')
#     options.add_argument('--disable-dev-shm-usage')

#     options.add_argument("window-size=1200x600")
    # driver = webdriver.Chrome(
    #     'chromedriver', options=options)

    # else:
    # options = webdriver.ChromeOptions()
    # options.add_argument(
    #     "--disable-blink-features=AutomationControlled")
    # # options.add_extension("./tractorDEI/extensions/vpn.crx")
    # # options.add_extension("/Users/seanwiggs/Documents/Code/Yelp/tractorDEI/extensions/vpn2.crx")
    driver = webdriver.Chrome(service=
        service, options=options)
    
    # driver = webdriver.Chrome()

    # installCaptcha(driver)

    driver.get(url)

    return driver

def getMailCode(driver, fake_identity):

    for i in range(120):
        time.sleep(2)
        print("Checking for mail...")

        time.sleep(.5)

        mail = requests.get("https://api.mail.tm/messages?page=1", headers={
            'Authorization': 'Bearer ' + fake_identity['sid']}).json().get('hydra:member')
        
        # print(mail, fake_identity["sid"])

        print("Checking if mail was received...")
        if mail:

            print("Mail received")
            print(mail)
            print((mail[0]['intro'].split('(')[1].split(')')[0]))

            driver.get((mail[0]['intro'].split('(')[1].split(')')[0]))

            break

    driver.execute_script("window.history.go(-1)")

def doReview(driver, fake_identity, center, account_created, place_url):

    # If no account was created, create one
    if not account_created:
        try:
            account_created = createAccount(driver, fake_identity, center)
        except Exception as e:
            raise e
        
        getMailCode(driver, fake_identity)
        # time.sleep(30000)
        
        writeReview(driver, fake_identity, place_url)

    # If account was created, just write review
    else:
        # writeReview(driver, fake_identity, place_url)
        pass
     
def writeReview(driver, fake_identity, place_url):
    
    driver.get(place_url)
    time.sleep(200)
    
def send_key_to_element(driver, XPATH, key):
    driver.find_element(By.XPATH, XPATH).send_keys(key)
    time.sleep(random.randint(0, 1))

def createAccount(driver, fake_identity, center):

    print("No Account Created: Creating Account")
    # click on sign up button
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
        (By.CLASS_NAME, 'y-css-1ewzev'))).click()

    # wait for new screen to load
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
        (By.XPATH, "//*[contains(text(),'Continue with email')]"))).click()

    # sleep random amount of time
    time.sleep(random.randint(1, 2))


    send_key_to_element(driver, "//input[@placeholder='First Name']", fake_identity['first_name'])
    send_key_to_element(driver, "//input[@placeholder='Last Name']", fake_identity['last_name'])
    send_key_to_element(driver, "//input[@placeholder='Email']", fake_identity['email'])
    send_key_to_element(driver, "//input[@placeholder='Password']", fake_identity['password'])
    send_key_to_element(driver, "//input[@placeholder='ZIP Code']", fake_identity['zip'])
    

    # click on sign up button
    signup_button = driver.find_element(By.XPATH, "//*[text()='Sign up']")
    
    signup_button.get_attribute("data-activated")
    driver.execute_script("arguments[0].setAttribute('data-activated',arguments[1])",signup_button, "true")

    WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
    (By.XPATH, "//*[text()='Sign up']"))).click()


    time.sleep(1)

    # Check if captcha is present
    
    try:
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
    (By.XPATH, '//*[@id="extra-form-save"]')))


    # if check_exists_by_xpath(driver, '//*[@id="extra-form-save"]'):

    # else:
        print("Captcha Present, Solving Captcha")

        # switch to frame
        # driver.switch_to.frame("0rfap4u3001")
        driver.switch_to.frame(driver.find_element(
            by=By.TAG_NAME, value="iframe"))
        time.sleep(1)
        WebDriverWait(driver, 600).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'check')))
        # WebDriverWait(driver, 600).until(lambda _: len(visible(
        #     driver, '//div[@class="h-captcha"]/iframe').get_attribute('data-hcaptcha-response')) > 0)
        # driver.switch_to.default_content()
        print('Captcha Solved')

        driver.find_element(By.ID, 'signup-button').click()
        try:
            WebDriverWait(driver, 180).until(EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="extra-form-save"]'))).click()
        except:
            raise Exception("Captcha Failed")


    except Exception as e:
        
            
        print("No Captcha Present")

        time.sleep(3)
        # print(driver.find_element(By.XPATH,
        #                           '//*[@id="extra-form"]/div[3]/div[2]/a').get_attribute('href'))

        # driver.get(driver.find_element(By.XPATH,
        #             '//*[@id="extra-form"]/div[3]/div[2]/a').get_attribute('href'))

        time.sleep(3)
        # print(driver.current_url)
        print('Confirming Email')

        
    
    

    return True

if __name__ == "__main__":




    fake_identity = createFakeIdentity()
    
    
    
    
    fake_identity = createMail(fake_identity)
    # print(fake_identity)


    driver = start_driver("https://yelp.com")
    # select_store(driver, fake_identity['zip'])
    find_store_on_yelp(driver, fake_identity['zip'])

    doReview(driver, fake_identity, "", "", "https://www.yelp.co.uk/biz/tractor-supply-ridgecrest?osq=Tractor+Supply+Co")


    time.sleep(2)


    getMailCode("", fake_identity)
    # print()