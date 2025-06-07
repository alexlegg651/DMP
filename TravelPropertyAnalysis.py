from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():

    # #gets details about the planned travel from the user
    # travel_location = user_input()

    # #allows application of certain options for how the web browser will function
    # website_config = Options()

    # #prevents the web browser from automatically closing at the end of execution
    # website_config.add_experimental_option("detach", True)

    # #prevents the web browser GUI from appearing to the user
    # website_config.add_argument("--headless") #(Meshi, 2020)

    # #website_config.add_experimental_option("excludeSwitches", ["enable-logging"])
    # #website_config.add_argument("--disable-gpu")
    # #website_config.add_argument("--no-sandbox")

    # #sets up webdriver and opens an empty Edge window and assigns this to the 'driver' webdriver variable
    # driver = webdriver.Edge(options=website_config) #(Selenium, 2025)
    # #navigates to the stated URL in the Edge window
    # driver.get("https://www.airbnb.co.uk")
    # search_for_properties(driver, travel_location)
    # #calls a function that inspects elements of the web page and retrieves data from them to be analysed
    # property_data = get_data(driver, website_config)

    property_data = {
        "name": ["barry", "cork", "essex"],
        "average_rating": [1, 2, 3],
        "number_of_reviews": [4, 5, 6],
        "price_per_night": [7, 8, 9]
    }
    travel_location = "new sheet"

    #declares the filename to be used to store all the property data about different locations
    filename = "property_data.xlsx"
    #calls a function that saves the data as a dataframe into an excel file and returns the name of the sheet it is stored in
    data_sheet = save_data(property_data, travel_location, filename)
    #calls a function reads the contents of the file containing the data into a dataframe
    property_df = load_data(filename, data_sheet)
    property_df = load_data(data_file)
    #calls a subroutine to provide analysis of the loaded property data
    analyse_data(property_df, travel_location)
    
def user_input():
    #gets input from the user of the destination for their planned travel
    destination = str(input("Please enter a destination: "))

    #returns the location as a string
    return destination

def search_for_properties(driver, location):

    #finds the destination search element by its element ID (found by manually inspecting the element)
    dest_search_element = driver.find_element(by=By.ID, value="bigsearch-query-location-input") #(GeeksForGeeks, 2024a)

    #due to interaction with element, the page goes through changes so must wait before attempting to interact with the element again to prevent interaction with element while it is still stale
    wait = WebDriverWait(driver, 5)
    dest_search_element = wait.until(expected_conditions.visibility_of_element_located((By.ID, "bigsearch-query-location-input"))) #(Microsoft Copilot, 2025)

    #enters the location into the search element found on the web page
    dest_search_element.send_keys(location)

    #finds the search button element using its XPATH instead of ID (doesn't have an ID) - XPATH syntax found through use of Microsoft Copilot AI
    search_button_element = driver.find_element(by=By.XPATH, value="//*[contains(@data-testid, 'structured-search-input-search-button')]") #(GeeksForGeeks, 2024b)
    
    #executes the "click" functionality on the button element found above
    search_button_element.click()


#a subroutine that inspects elements of the web and retrieves data from them
def get_data(driver, website_config):
    #creates empty lists for each column heading of the dataframe (each different type of data of each property)
    name = []
    average_rating = []
    number_of_ratings = [] 
    price_per_night = []

    #loops through the steps for the set number of pages
    for page in range(1, 3):
        #loops through the steps for collecting data for each property
        for result_index in range(1, 18):
            #gets the following data for the current property
            name_value = get_property_name(driver, result_index)
            rating_value, rating_num = get_ratings_and_reviews(driver, result_index)
            price = get_price(driver, result_index)

            #appends the collected data to lists of the data for each type of data for each property
            name.append(name_value)
            average_rating.append(rating_value)
            number_of_ratings.append(rating_num)
            price_per_night.append(price)

        #selects next page button to show more property listings
        next_page(driver)

    #stores the data collected from the Airbnb website stored in lists into a dictionary of lists ready to be converted to a dataframe
    properties = {
        "name": name,
        "average_rating": average_rating,
        "number_of_ratings": number_of_ratings,
        "price_per_night": price_per_night,
    }
    return properties

def save_data(data, travel_location, filename):
    #creates a dataframe out of the data retrieved that was stored in a dictionary of lists
    property_df = pd.DataFrame(data) #(pandas, n.d. -b)

    #declares a new string variable filename_location
    sheet_name = ""
    #iterates through the travel_location string (input by user)
    for char in travel_location:
        #replaces any spaces with "_" in the travel_location so the filename has no spaces
        if char == " ":
            sheet_name += "_"
        #if char is not a space, concatenates char to the string as normal
        else:
            sheet_name += char
    sheet_name += "_properties"

    #exports the dataframe to an excel file of the filename generated - stores the data for each new location in a new sheet in the 1 excel file
    with pd.ExcelWriter(filename, engine="openpyxl", mode="a", if_sheet_exists="replace") as data_writer:
        #saves the data in a new excel sheet with name sheet_name - all property data stored in the same Excel file in separate sheets
        property_df.to_excel(data_writer, sheet_name=sheet_name, index=False)
    return sheet_name

def load_data(filename, data_sheet):
    df = pd.read_excel(filename, sheet_name=data_sheet)
    return df

#subroutine that initialises different visualisations of the data provided
def analyse_data(property_df, travel_location):
    #data munging - fills in null values (empty values) with 0
    property_df.fillna(0, inplace=True)

    #prints basic statistical values from the dataframe to the user
    print(property_df.describe())

    #sets up 3 areas in a single window for individual graphs to be displayed using matplotlib library
    figure, graph = plt.subplots(1, 3, figsize=(16, 4)) #(Bing Writer, 2025)

    #calls various functions to create and return various graphs
    graph[0] = rating_bar(property_df, travel_location, graph[0])
    graph[1] = price_bar(property_df, travel_location, graph[1])
    graph[2] = rating_num_pie(property_df, travel_location, graph[2])

    plt.tight_layout()

    plt.show()

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

#function that takes the driver variable and loop index as parameters then uses them to get the name of the current property and return it
def get_property_name(driver, result_index):

    #the XPath of the element containing the name of the property
    path = f"/html/body/div[5]/div/div/div[1]/div/div/div[2]/div[1]/main/div[2]/div/div[2]/div/div/div/div/div/div[{result_index}]/div/div[2]/div/div/div/div/div/div[2]/div[3]/span"

    #uses a loop that continues trying to find the element if it is not initially found
    name_element = ''
    attempts = 0
    while attempts < 3 and name_element == '':
        #the element containing the name value of the property is found and assigned to a variable after waiting for it to be located (calls function to do this)
        name_element = get_element(driver, path)
        attempts += 1
        
    if name_element != '':
        #gets the text value of the name element using the getattr Python function
        name_value = getattr(name_element, "text")

    #cuts the property name down to a finite number of characters to ensure it is readable in hte visualisations but still useful
    short_name = ""
    for char in range(0, len(name_value)):
        if char < 16:
            short_name += name_value[char]
    short_name += "..."

    #returns the name value of the property so it can be stored
    return short_name

#function that takes the driver variable and loop index as parameters and uses them to get and return data about ratings and reviews
def get_ratings_and_reviews(driver, result_index):
    
    #the XPath for the element containing the average rating and number of reviews
    path = f"/html/body/div[5]/div/div/div[1]/div/div/div[2]/div[1]/main/div[2]/div/div[2]/div/div/div/div/div/div[{result_index}]/div/div[2]/div/div/div/div/div/div[2]/div[7]/span/span[3]"
    #the element containing the average rating and number of reviews is found and assigned after waiting for it to be located (calls function above)
    rating_element = get_element(driver, path)
    
    #calls a function to get the text value of the element if it exists and splits the string containing the average rating and number of reviews and assigns each part to a different variable
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

    #removes any characters that are not numerical digits that the string_price_value could contain
    formatted_price_value = ""
    for char in string_price_value:
        #if current character is , or £ then these are not appended to the final formatted price value so this can be converted to a float
        if char != "," and char != "£":
            formatted_price_value += char

    #casts the string price value to a float
    price_value = float(formatted_price_value)

    return price_value

def next_page(driver):
    #the full XPath of the next page button
    element_path = "/html/body/div[5]/div/div/div[1]/div/div/div[2]/div[1]/main/div[2]/div/div[3]/div/div/div/nav/div/a[5]"
    #gets the element of the next page button and assigns it to a variable
    next_page_button = get_element(driver, element_path)
    #simulates a click on the next page button to cause the next page to be displayed
    next_page_button.click()


def rating_bar(property_df, travel_location, graph):
    #gets the data from column 0 and assigns it to a list variable
    properties = property_df.iloc[:, 0] #(pandas, n.d. -a)
    #gets the data from the column called "average_rating" and assigns it to the ratings variable as a list
    ratings = property_df["average_rating"]

    #converts the lists of data to numpy arrays so they can be used to generate visualisations
    x = np.array(properties)
    y = np.array(ratings)
    #uses the numpy arrays to plot a bar chart
    graph.bar(x, y, color="red")

    #sets various visual features for the bar chart
    graph.set_title(f"Average ratings of each property in {travel_location}")
    graph.set_xlabel("Property")
    graph.set_ylabel("Average rating")
    graph.set_xticks(x, labels=properties, rotation=270) #(GeeksForGeeks, 2022)

    #returns the bar chart
    return graph

def price_bar(property_df, travel_location, graph):
    #gets the data from column 0 and assigns it to a list variable
    properties = property_df.iloc[:, 0]
    #gets the data from the column called "price_per_night" and assigns it to the ratings variable as a list
    prices = property_df["price_per_night"]

    #converts the lists of data to numpy arrays so they can be used to generate visualisations
    x = np.array(properties)
    y = np.array(prices)

    #uses the numpy arrays to plot a bar chart
    graph.bar(x, y, color="green")
    #sets various visual features for the bar chart
    graph.set_title(f"Prices of properties in {travel_location}")
    graph.set_xlabel("Property")
    graph.set_xticks(x, labels=properties, rotation=270)
    graph.set_ylabel("Price per night (£)")
    #returns the bar chart
    return graph


def rating_num_pie(property_df, travel_location, graph):

    slice_num = 10

    #gets the data from column 0 and assigns it to a list variable
    properties = property_df.iloc[0:slice_num+1, 0]
    #gets the data from the column called "number_of_ratings" and assigns it to the ratings variable as a list
    rating_counts = property_df.loc[0:slice_num, "number_of_ratings"]

    #creates a numpy array for the number of ratings
    x = np.array(rating_counts)

    #creates an empty list to store the labels
    label = []
    #iterates through each property and appends a tuple of the property index and number of ratings to the label list
    for i in range(0, len(properties)):
        label.append((properties[i], rating_counts[i]))

    #creates a pie chart from this data
    graph.pie(x, labels=label)
    graph.set_title("Number of reviews of each property")
    
    return graph

main()
