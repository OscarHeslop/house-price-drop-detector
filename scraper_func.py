
#use playright 
#type in croydon and submit 
#py -m pip install playwright
#can see what does in real time

website  = "https://www.rightmove.co.uk/property-for-sale/find.html?searchLocation=Croydon%2C+London&useLocationIdentifier=true&locationIdentifier=REGION%5E391&minPrice=50000&maxPrice=60000&minBedrooms=10&radius=0.0&_includeSSTC=on"

#py -m playwright install
#py -m playwright install chromium
from playwright.sync_api import sync_playwright

def open_browser():

    playwright = sync_playwright().start()

    browser = playwright.chromium.launch(
        headless=True
    )

    page = browser.new_page()

    page.goto(website)

    return page, browser

 


def press_accept_all(page):

    try:
        button = page.locator("#onetrust-accept-btn-handler")

        print("Found:", button.count())

        button.scroll_into_view_if_needed()

        button.wait_for(state="visible", timeout=10000)

        page.wait_for_timeout(500)

        button.click(force=True)

        print("Cookie accepted")

    except Exception as e:
        print("Cookie failed:", e)

    return True
def send_area_to_browser(home_page, area):

    search_box = home_page.locator(".dsrm_inputText.ta_userInput")

    search_box.click()
    search_box.fill(area)

    # wait for suggestions to appear
    home_page.wait_for_timeout(2000)

    # move to first suggestion
    search_box.press("ArrowDown")

    home_page.wait_for_timeout(1000)

    # select suggestion
    search_box.press("Enter")

    home_page.wait_for_timeout(3000)

    # submit search button
    home_page.keyboard.press("Enter")

    home_page.wait_for_timeout(2000)

def set_min_and_max_price(home_page):
    #find min button
    min_button = home_page.locator("#minPrice")
    max_button =home_page.locator("#maxPrice")

    min_button.select_option(str("Min Price"))
    max_button.select_option(str("Max Price"))
    #select option max

def set_min_and_max_beds(home_page):
    #find min button
    min_button = home_page.locator("#minBeds")
    max_button =home_page.locator("#maxBeds")

    min_button.select_option("Min Beds")
    max_button.select_option("Max Beds") #in built function


def go_to_house_card(home_page, browser, i):

    print("ENTERED FUNCTION")

    specific_house_link = home_page.locator(
        '[data-monitor-testid="propertyCard-img-link"]'
    ).nth(i)

    url = specific_house_link.get_attribute("href")

    print("URL IS:", url)

    house_page = browser.new_page()

    print("NEW PAGE CREATED")

    house_page.goto(
        "https://www.rightmove.co.uk" + url
    )

    print("GOTO FINISHED")

    return house_page, url
def get_house_details(house_page):    
    address = house_page.locator('[data-monitor-testid="streetAddress"]').inner_text()
    features = house_page.locator('[data-testid="keyFeatures"] li').all_inner_texts()
    price = house_page.locator('[name="propertyValue"]').input_value()

    return address, price, features

def get_house_price(house_page):

    if house_page.locator('[name="propertyValue"]').count() > 0:
        return house_page.locator('[name="propertyValue"]').input_value()

    elif house_page.locator('[aria-label^="Property:"]').count() > 0:
        price = house_page.locator('[aria-label^="Property:"]').get_attribute("aria-label")

        price = price.replace("Property:", "").strip()

        return price

    else:
        return None
def get_house_address(house_page):
    #address is same for both 
    address = house_page.locator(
    '[data-monitor-testid="streetAddress"]'
).inner_text()
    return address

def get_house_key_features(house_page):
    features = house_page.locator(
    '[data-testid="keyFeatures"] li'
).all_inner_texts()
    return features

    

#---------------------------------
#combining functions 

    
def get_house_id(url):
    id = url.split("/properties/")[1].split("#")[0]
    return id


import re

def get_house_postcode(house_page):
    try:
        text = house_page.locator(".LwI1MMzW63B2LqkYFkUu").first.inner_text()

        match = re.search(
            r"[A-Z]{1,2}\d[A-Z\d]?\s*\d[A-Z]{2}",
            text.upper()
        )

        return match.group(0) if match else None

    except Exception:
        return None

#---------------------------------process



