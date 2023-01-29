#####################################################################
import numpy as np
import pandas as pd
import streamlit as st
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from streamlit_lottie import st_lottie
import os

#Page configurations
st.set_page_config(
    page_title="Real Estate App",
    page_icon = "🔎",
)

def load_lottieurl(url: str):
    """
    Loads lottie json animation
    :param url:
    :return:
    """
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


def format_url(location, province, province_short):
    """
    Creates a url for webpage using given location and province
    :param location:
    :param province:
    :param province_short:
    :return:
    """
    location_url = location.lower().strip().replace(' ', '+').lower() #Url substring for location
    province_url = province_short[province].lower() #Url substring for province
    new_url = f"https://www.rew.ca/properties/search/results?initial_search_method=single_field&query={location_url}+{province_url}" #Formatted url
    return new_url


def seleniumDriver(url):
    """
    Creates chrome driver and beautiful soup object from selenium html
    :param url:
    :return:
    """
    #Create environment
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(service=Service(os.environ.get("CHROMEDRIVER_PATH")), options=chrome_options)
    #driver = webdriver.Chrome(r'D:/RealEstate App/Drivers/chromedriver.exe')
    driver.get(url)
    html = driver.page_source

    soup = BeautifulSoup(html, features="html.parser") #Beautiful Soup object

    return soup, driver

def fetch_data(url):
    """
    Scrapes real estate data from web page
    :param url:
    :return:
    """

    def remove_unit(value, units):
        """
        Removes units from data strings
        :param value:
        :param units:
        :return:
        """
        removed = value.translate({ord(i): None for i in units}) #Remove desired units given string of units
        return removed

    def calc_sf(ft):
        """
        Calculates square feet from dimensions given in feet
        :param ft:
        :return:
        """
        length, width = ft.split(' ft')[0].split(' x ') #Split foot dimensions
        square_footage = str((int(length) * int(width))) + ' sf' #Multiply foot dimensions
        return square_footage


    def middle(range):
        """
        Determines average of a given range (some values on real estate websites are given as a range rather than a set value)
        :param range:
        :return:
        """
        #Determine if the value is in square feet or feet
        if "sf" in range:
            unit = " sf"
        else:
            unit = " ft"
        num1, num2 = range.split(unit)[0].split(" - ") #Split the range into two values
        avg = str(round((int(num1) + int(num2)) / 2)) + unit #Determine the mean and round the final value
        return avg


    soup, driver = seleniumDriver(url)
    listings = soup.findAll('article', class_='displaypanel') #Scrape all listings

    #pg 24 error
    for listing in listings: # Iterate through listings
        try:
            price = remove_unit(listing.find('div', class_='displaypanel-price hidden-xs').text, ",$") #Scrape listing price
        except:
            price = "NA"
        try:
            address = listing.find('div', class_='displaypanel-section').text #Scrape listing address
        except:
            address = "NA"
        try:
            details = [listing.text for listing in listing.find('div', class_='displaypanel-section clearfix').findAll('li')] #Scrape listing details
        except:
            details = None
        try:
            type = listing.find('div', class_='displaypanel-info').text #Scrape listing property type
        except:
            type = "NA"
        try:
            if "+" in beds: #If beds is given in addition format, add the two values
                num1, num2 = beds.split(' + ')
                beds = str(int(num1) + int(num2))
            beds = details[0].replace(' bd', '')
        except:
            beds = "NA"
        try:
            if "+" in baths: #If baths is given in addition format, add the two values
                num1, num2 = beds.split(' + ')
                baths = str(int(num1) + int(num2))
            baths = details[1].replace(' ba', '')
        except:
            baths = "NA"
        try:
            if ' - ' in details[2]: #If area is given in range format, convert to the mean
                measurement = middle(details[2])
            else:
                measurement = details[2]

            if 'sf' in measurement: #If area is given in square feet, remove the unit
                area = remove_unit(measurement, " sf")
            elif 'ft' in measurement: #If area is given in feet, convert to square feet and remove the unit
                area = remove_unit(calc_sf(measurement), " sf")
        except:
            area = "NA"

        #Store listing information in a dictionary
        item = {
            'Price': price,
            'Address': address,
            'Type' : type,
            'Beds': beds,
            'Baths': baths,
            'Area': area,
        }

        items.append(item) #Append each listing dictionary to a list

        if (listings.index(listing) + 1) == len(listings): #If iteration is on the last listing of the page
            driver.close() #Close the driver
            try:
                if not soup.find('li', class_='paginator-next_page paginator-control').find('a'): #If paginator (next page selector) does not exist, return none
                    return None
                else: #If paginator exists, recursively call the fetch_data function
                    return fetch_data('https://www.rew.ca/' + (
                    soup.find('li', class_='paginator-next_page paginator-control').find('a')['href']))
            except: #If an error occurs, return none
                return None


# Title
st.title("Listings")

# User location input
user_location = st.text_input(label="Location", placeholder="City or Area, Province", max_chars=None, type="default",
                              label_visibility="visible")

#Abbreviations for Canadian provinces
province_short = {"Newfoundland and Labrador": "NL", "Prince Edward Island": "PE", "Nova Scotia": "NS",
                "New Brunswick": "NB", "Quebec": "QC", "Ontario": "ON", "Manitoba": "MB", "Saskatchewan": "SK",
                "Alberta": "AB", "British Columbia": "BC", "Yukon": "YK", "Northwest Territories": "NT",
                "Nunavut": "NU"}

items = [] #List to store listing dictionaries

# Derive province and area from user input
try:
    province = user_location.split(', ')[1] #Derive province
    location = user_location.split(', ')[0] #Derive location
    st.success('Searching for results') #Dispay searching for results message
    lottie_search_animation_url = "https://assets4.lottiefiles.com/packages/lf20_bxNLkdyLYm.json" #Lottie url
    lottie_search = load_lottieurl(lottie_search_animation_url) #Load lottie
    st_lottie(lottie_search, key='search') #Display lottie animation
except:
    st.info('Please enter a valid location in the form: **Area/City, Province**. Eg. Ottawa, Ontario.') #Info message of proper text input

fetch_data(format_url(location, province, province_short))

df = pd.DataFrame(items) #Create pandas dataframe from list of item dictionaries
df[['Area', 'Beds', 'Baths']] = df[['Area', 'Beds', 'Baths']].apply(pd.to_numeric, errors='coerce') #Convert all dataframe values to numeric type
st.session_state['df'] = df #Set session state to dataframe for accessing in DataAnalysis.py
st.info("Done! Navigate to the data analysis page to view analysis") #Display success message