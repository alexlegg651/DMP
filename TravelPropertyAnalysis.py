#https://www.geeksforgeeks.org/interacting-with-webpage-selenium-python/
#https://www.geeksforgeeks.org/python-web-scraping-tutorial/
#https://www.geeksforgeeks.org/selenium-testing-without-browser/
#https://www.selenium.dev/documentation/webdriver/getting_started/first_script/
#https://www.geeksforgeeks.org/find_element_by_xpath-driver-method-selenium-python/
#https://www.geeksforgeeks.org/python-tkinter-entry-widget/

'''
Take user input of location to stay
Web scrape AirBnb with search of this location
Get characteristics of top properties
    -Ratings (available from AirBnb list)
    -Prices (available from AirBnb list)
    -Amenities
    -Number of guests
    -Free cancellation? (available from AirBnb list)
    -Number of reviews (available from AirBnb list)
Create dataframe from collected data
Analyse and create graphs
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

def main():

    #gets details about the planned travel from the user
    travel_location = user_input()

    #allows application of certain options for how the web browser will function
    website_config = Options()

    #prevents the web browser from automatically closing at the end of execution
    website_config.add_experimental_option("detach", True)

    #prevents the web browser GUI from appearing to the user
    #website_config.add_argument("--headless")

    #website_config.add_experimental_option("excludeSwitches", ["enable-logging"])
    #website_config.add_argument("--disable-gpu")
    #website_config.add_argument("--no-sandbox")

    #sets up webdriver and opens an empty Edge window and assigns this to the 'driver' webdriver variable
    driver = webdriver.Edge(options=website_config) #(Selenium, 2025)
    #navigates to the stated URL in the Edge window
    driver.get("https://www.airbnb.co.uk")
    search_for_properties(driver, travel_location)
    #calls a subroutine that inspects elements of the web page and retrieves data from them to be analysed
    get_data(driver)
    
def user_input():
    #gets input from the user of the destination for their planned travel
    destination = str(input("Please enter a destination: "))

    #returns the location as a string
    return destination

def search_for_properties(driver, location):

    #finds the destination search element by its element ID (found by manually inspecting the element)
    dest_search_element = driver.find_element(by=By.ID, value="bigsearch-query-location-input")

    #due to interaction with element, the page goes through changes so must wait before attempting to interact with the element again to prevent interaction with element while it is still stale
    wait = WebDriverWait(driver, 5)
    dest_search_element = wait.until(expected_conditions.visibility_of_element_located((By.ID, "bigsearch-query-location-input")))

    #enters the location into the search element found on the web page
    dest_search_element.send_keys(location)

    #finds the search button element using its XPATH instead of ID (doesn't have an ID) - XPATH syntax found through use of Microsoft Copilot AI
    search_button_element = driver.find_element(by=By.XPATH, value="//*[contains(@data-testid, 'structured-search-input-search-button')]")
    
    #executes the "click" functionality on the button element found above
    search_button_element.click()

#a subroutine that inspects elements of the web page and retrieves data from them
def get_data(driver):
    properties = []

    for page in range(1, 4):
        for result_index in range(1, 18):
            rating_element = driver.find_element(by=By.XPATH, value=f"/html/body/div[5]/div/div/div[1]/div/div/div[2]/div[1]/main/div[2]/div/div[2]/div/div/div/div/div/div[{result_index}]/div/div[2]/div/div/div/div/div/div[2]/div[7]/span/span[3]")
            rating_value = float(getattr(rating_element, "text").split(" ")[0]) #(GeeksForGeeks, 2025)
            #VERSION CONTROL, PROJECT MANAGEMENT, REFERENCES TO WEBSITE & AI USAGE
        #select next page
main()