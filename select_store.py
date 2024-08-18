# from .main import fake_identity
import time

def select_store(driver, zip):
    store_url = f"https://www.tractorsupply.com/tsc/store-locator?zipCode={zip}"
    
    print("Selecting Store")
    driver.get(store_url)
    
    # Get all addresses and select the first one
    
    time.sleep(2)
    
    
def find_store_on_yelp(driver, zip):
    
    store_url = f"https://www.yelp.com/search?find_desc=Tractor+Supply+Co&find_loc={zip}"
        
    print("Selecting Store")
    driver.get(store_url)
    
    # Get all addresses and select the first one
    
    time.sleep(2)
    