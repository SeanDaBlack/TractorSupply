# from .main import fake_identity
import time, random
from selenium.webdriver.common.by import By


states = [
"Alabama",
"Arkansas",
"Arizona",
"California",
"Colorado",
"Connecticut",
"Delaware",
"Florida",
"Georgia",
"Iowa",
"Idaho",
"Illinois",
"Kansas",
"Kentucky",
"Louisiana",
"Massachusetts",
"Maryland",
"Maine",
"Michigan",
"Minnesota",
"Missouri",
"Mississippi",
"Montana",
"North Carolina",
"North Dakota",
"Nebraska",
"New Hampshire",
"New Jersey",
"New Mexico",
"Nevada",
"New York",
"Ohio",
"Oklahoma",
"Pennsylvania",
"Rhode Island",
"South Carolina",
"South Dakota",
"Tennessee",
"Texas",
"Utah",
"Virginia",
"Vermont",
"Washington",
"Wisconsin",
"West Virginia",
"Wyoming"]











def select_store(driver, fake_identity):
    
    
    random_state = random.choice(states).lower().replace(" ", "-")
    
    
    
    
    
    
    
    
    store_url = f"https://www.tractorsupply.com/tsc/store-locations/{random_state}"
    
    print("Selecting Store")
    driver.get(store_url)
    
    # Get elements with class "store-card" and select a random one
    
    time.sleep(2)
    # wait for page to load
    
    driver.implicitly_wait(10)
    
    print(driver.page_source)
    stores = random.choice(driver.find_elements(By.CLASS_NAME, "store-card"))
    
    store_text = stores.text.split("\n")
    
    fake_identity["state"] = random_state
    fake_identity["city"] = store_text[2].split(",")[0]
    fake_identity["zip"] = store_text[2].split(",")[1].split(" ")[2]
    fake_identity["address"] = store_text[1]
    
    
    time.sleep(2)
    return fake_identity
    
    
def find_store_on_yelp(driver, fake_identity):
    
    store_url = f"https://www.yelp.co.uk/search?find_desc=Tractor+Supply&find_loc={fake_identity['city']}%2C+{fake_identity['state']}"
        
    print("Selecting Store")
    driver.get(store_url)
    
    # Get all addresses and select the first one
    # return store_url
    
    # print all a elements with the name including "Tractor Supply Co" or "Tractor Supply"
    
    time.sleep(2)
    stores = driver.find_elements(By.PARTIAL_LINK_TEXT, 'Tractor Supply')
    if stores == []:
        print("No Stores Found")
        return
    
    
    for store in stores:
        print(store.get_attribute("href"))
    # print()
    
    time.sleep(200)
    