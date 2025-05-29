#https://www.geeksforgeeks.org/interacting-with-webpage-selenium-python/
#https://www.geeksforgeeks.org/python-web-scraping-tutorial/
#https://www.geeksforgeeks.org/selenium-testing-without-browser/
#https://www.selenium.dev/documentation/webdriver/getting_started/first_script/
#https://www.geeksforgeeks.org/find_element_by_xpath-driver-method-selenium-python/
#https://www.geeksforgeeks.org/python-tkinter-entry-widget/
#https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_excel.html & AI 29/05/2025

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException
import pandas as pd

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
    #calls a function that inspects elements of the web page and retrieves data from them to be analysed
    property_data = get_data(driver, website_config)

    #calls a subroutine that saves the data as a dataframe into an excel file
    data_file = save_data(property_data, travel_location)
    
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


#a subroutine that inspects elements of the web and retrieves data from them
def get_data(driver, website_config):
    #creates empty lists for each column heading of the dataframe (each different type of data of each property)
    average_rating = []
    number_of_ratings = [] 
    price_per_night = []

    #loops through the steps for the set number of pages
    for page in range(1, 4):
        #loops through the steps for collecting data for each property
        for result_index in range(1, 18):
            #gets the following data for the current property
            rating_value, rating_num = get_ratings_and_reviews(driver, result_index)
            price = get_price(driver, result_index)

            '''
            subroutine that causes the website to open a web page to a particular property to find more information
            property_driver = enter_property(driver, result_index, website_config)
            wifi = get_amenities(property_driver) #kitchen, pool, heating, tv
            '''

            #appends the collected data to lists of the data for each type of data for each property
            average_rating.append(rating_value)
            number_of_ratings.append(rating_num)
            price_per_night.append(price)

        #selects next page button to show more property listings
        next_page(driver)

    #stores the data collected from the Airbnb website stored in lists into a dictionary of lists ready to be converted to a dataframe
    properties = {
        "average_rating": average_rating,
        "number_of_ratings": number_of_ratings,
        "price_per_night": price_per_night,
    }
    return properties

def save_data(data, travel_location):
    #creates a dataframe out of the data retrieved that was stored in a dictionary of lists
    property_df = pd.DataFrame(data) #reference

    #generates a filename based off of the location that the user input
    filename = f"{travel_location}_properties.xlsx"
    #exports the dataframe to an excel file of the filename generated
    property_df.to_excel(filename, sheet_name=f"{travel_location}_properties", index=True)



#function that causes the program to wait until a specified element has been loaded on the web page before trying to access it to prevent an error
def get_element(driver, path):
    #creates a WebDriverWait
    wait = WebDriverWait(driver, 5)

    #form of error-handling - if element is not found, error is caught and moves onto the next element
    try:
        #finds the element on the web page but waits until it is located before trying to assign it to a variable (element)
        element = wait.until(expected_conditions.visibility_of_element_located((By.XPATH, path)))
    except TimeoutException:
        #timeout may occur if no element is found with this XPath and so no value is returned
        return ""
    #WebElement value is returned if found
    return element

#subroutine that takes the driver variable and loop index as parameters and uses them to get and return data about ratings and reviews
def get_ratings_and_reviews(driver, result_index):
    
    #the XPath for the element containing the average rating and number of reviews
    path = f"/html/body/div[5]/div/div/div[1]/div/div/div[2]/div[1]/main/div[2]/div/div[2]/div/div/div/div/div/div[{result_index}]/div/div[2]/div/div/div/div/div/div[2]/div[7]/span/span[3]"
    #the element containing the average rating and number of reviews is found and assigned after waiting for it to be located (calls function above)
    rating_element = get_element(driver, path)
    
    #gets the text value of the element using getattr and splits the string containing the average rating and number of reviews and assigns each part to a different variable
    string_rating_value, string_number_of_ratings = try_rating_review(rating_element)
    
    #checks if string_rating_value has a meaningful value
    if string_rating_value != "":
        #casts the average rating string to a float
        rating_value = float(string_rating_value)
    else:
        #if there is no value, rating_value is assigned no value to prevent error
        rating_value = string_rating_value
    
    #checks if string_number_of_ratings has a meaningful value
    if string_number_of_ratings != "":
        #removes the brackets from either side of the number of ratings string
        string_number_of_ratings = string_number_of_ratings.split("(")[1]
        string_number_of_ratings = string_number_of_ratings.split(")")[0]
        #casts the number of ratings string to an integer
        number_of_ratings = int(string_number_of_ratings)
    else:
        #if there is no value, number_of_ratings is assigned no value to prevent error
        number_of_ratings = string_number_of_ratings

    #returns the values so they can be stored
    return rating_value, number_of_ratings

def try_rating_review(rating_element):

    try:
        #gets the text value of the element found
        rating_element_value = getattr(rating_element, "text") #(GeeksForGeeks, 2025)
    except AttributeError:
        #some properties may not have a rating value if there are less than 3 reviews
        rating_element_value = ""

    #attempts to split the text into 2 strings (1 for average rating, 1 for number of reviews) - in some cases this is not possible, such as when the rating is replaced with "New" on the website
    try:
        rating, num_review = rating_element_value.split(" ")
    except ValueError:
        #a ValueError is caught and empty values returned
        return "", ""
    
    return rating, num_review

#function that gets the price per night of property with index result_index using the web driver and returns this price
def get_price(driver, result_index):
    #the XPath for the element containing the price per night
    path = f"/html/body/div[5]/div/div/div[1]/div/div/div[2]/div[1]/main/div[2]/div/div[2]/div/div/div/div/div/div[{result_index}]/div/div[2]/div/div/div/div/div/div[2]/div[6]/div[2]/div/div/span[1]"
    #calls a function to get the element after waiting for it to be loaded
    price_element = get_element(driver, path)

    #gets the price text value of the price_element
    string_price_value = getattr(price_element, "text")
    #removes the extra chars of the string until just the number of the price in £ remains
    string_price_value = string_price_value.split(" ")[0]
    string_price_value = string_price_value.split("£")[1]
    #casts the string price value to a float
    price_value = float(string_price_value)

    return price_value

'''
def get_cancellation_policy(driver, result_index):
    #the XPath for the element containing the cancellation policy
    path = f"/html/body/div[5]/div/div/div[1]/div/div/div[2]/div[1]/main/div[2]/div/div[2]/div/div/div/div/div/div[{result_index}]/div/div[2]/div/div/div/div/div/div[2]/div[4]/span/span[2]/span"
    #gets the element containing the cancellation policy after waiting for it to load
    policy_element = get_element(driver, path)

    #checks if the cancellation policy element exists for the property
    if policy_element != "":
        #gets the text value of the cancellation policy using getattr function
        policy_value = getattr(policy_element, "text")
        #determines the cancellation policy and returns the appropriate value
        if policy_value == "Free cancellation": 
            return "yes"
        else: 
            return "no"
    else:
        return "no"
'''

def enter_property(driver, result_index, website_config):
    #the path for the current property element as a whole (element that is clicked on to view all property details)
    path = f"/html/body/div[5]/div/div/div[1]/div/div/div[2]/div[1]/main/div[2]/div/div[2]/div/div/div/div/div/div[{result_index}]/div/div[2]/div/div/div/div/a"
    #gets element from path above
    property_element = get_element(driver, path)
    #gets the URL of the current property information page
    property_url = property_element.get_attribute("href")

    #sets up another web driver for the current property
    property_driver = webdriver.Edge(options=website_config)
    #navigates to the URL found above of the current property
    property_driver.get(property_url)
    return property_driver

'''
def get_amenities(property_driver):
    path = "/html/body/div[5]/div/div/div[1]/div/div/div[1]/div/div/div/div[1]/main/div/div[1]/div[3]/div/div[1]/div/div[6]/div/div[2]/section/div[3]/button"
    amenities_button = get_element(property_driver, path)
    
    amenities_element = get_element(property_driver, path) 
    amenities = getattr(amenities_element, "text")
    if "wifi" in amenities.lower():
        wifi = "yes"
    else:
        wifi = "no"

    return wifi
'''

def next_page(driver):
    #the full XPath of the next page button
    element_path = "/html/body/div[5]/div/div/div[1]/div/div/div[2]/div[1]/main/div[2]/div/div[3]/div/div/div/nav/div/a[5]"
    #gets the element of the next page button and assigns it to a variable
    next_page_button = get_element(driver, element_path)
    #simulates a click on the next page button to cause the next page to be displayed
    next_page_button.click()

main()
