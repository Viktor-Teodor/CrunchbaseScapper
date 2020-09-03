import csv
import os

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from datetime import datetime
from selenium.webdriver.support.wait import WebDriverWait


def logIntoCrunchBase(driver, str):
    driver.get(str)

    # We find the log in button and click on it so we can use the account
    logInButton = driver.find_element_by_xpath("//*[contains(text(), 'Log In')]")
    logInButton.click()

    # Fill the email form
    emailAddressForm = driver.find_element_by_name("email")
    emailAddressForm.clear()

    # DO NOT LEAVE THOSE CREDENTIALS HERE
    emailAddressForm.send_keys("venturedevelopment@r3.com")

    # Fill the password
    passwordForm = driver.find_element_by_name("password")
    passwordForm.clear()

    # DO NOT LEAVE THIS HERE
    passwordForm.send_keys("January2020")

    # Submit the form
    passwordForm.send_keys(Keys.RETURN)

def getCompanyWebsite(driver):
    text = []

    link = findElement(driver,"//a[contains(@class, 'component--field-formatter layout-row layout-align-start-end link-accent ng-star-inserted')]")
    text = link.text

    return text

def getCompanyFunding(driver):
    text = None

    link = findElement(driver, "//span[contains(@class, 'component--field-formatter field-type-money ng-star-inserted')]")
    text = link.text

    return text

def getCompanyEmail(driver):
    text = None

    try:
        link = driver.find_elements_by_xpath("//span[contains(@class, 'ng-star-inserted')]")
    except StaleElementReferenceException:
        link = driver.find_elements_by_xpath("//span[contains(@class, 'ng-star-inserted')]")

    for email in link:
        if str(email.text).__contains__("@"):
            text = email.text

    return text

def getFounders(driver):
    text = []

    try:
        founders = driver.find_elements_by_xpath("//a[contains(@class, 'link-accent ng-star-inserted')]")
    except StaleElementReferenceException:
        founders = driver.find_elements_by_xpath("//a[contains(@class, 'link-accent ng-star-inserted')]")

    for founder in founders:
        if str(founder.get_attribute("href")).__contains__("person"):
            print(founder.get_attribute("href"))
            text.append(founder.get_attribute("href"))


    return text

def getName(driver):

    link =findElement(driver, "//span[contains(@class, 'profile-name')]")
    text = link.text

    return text

def getLinkedin(driver):

    try:
        name = findElement(driver, "//a[contains(@class, 'component--field-formatter layout-row layout-align-start-end link-accent ng-star-inserted')]")
        text = name.get_attribute("href")

    except (NoSuchElementException, TimeoutException, AttributeError) as e:
        text = None

    return text

def findElement(driver, criteria):

    result = None

    try:
        result = WebDriverWait(driver, 3).until(EC.element_to_be_clickable(
            (By.XPATH, criteria)))

    except StaleElementReferenceException:
        result = WebDriverWait(driver, 3).until(EC.element_to_be_clickable(
            (By.XPATH,criteria)))
    except TimeoutException:
        result = None

    return result

def doStuff(description, headquarters, industry):
    driver = webdriver.Chrome()

    logIntoCrunchBase(driver, "https://www.crunchbase.com")

    # Go to the search page
    searchPage = findElement(driver, "//theme-icon[contains(@themeid, 'company')]")
    searchPage.click()

    # Download the search results as CSV and load it in pandas
    downloadButton = findElement(driver, "//*[contains(text(), 'Export to CSV')]")
    downloadButton.click()

    # In case the modal that asks if you want to download only 1000 results appears
    # try:
    downloadResultsCSVModal = findElement(driver,
                                          "//button[@class='mat-focus-indicator cb-text-transform-upper mat-raised-button mat-button-base mat-primary']")
    downloadResultsCSVModal.click()

    # except:
    #    print("Downloaded the results")

    x = datetime.now()

    sleep(1)
    nameOfFile = r"C:\Users\Victor Stoian\Downloads\companies-" + str(x.month) + "-" + str(x.day) + "-" + str(
        x.year) + '.csv'
    data = pd.read_csv(nameOfFile)

    foundersDriver = webdriver.Chrome()

    savedData = {
        "Company Website": [],
        "Company Funding": [],
        "Company Email": [],
        "Company Founders": []
    }

    for crunchBaseURL in data['Organization Name URL'].iloc[0:5]:
        # Go to the crunchbase page of every company
        driver.get(crunchBaseURL)

        # Get the company website
        website = getCompanyWebsite(driver)

        # Get the funding
        funds = getCompanyFunding(driver)

        # Get email
        email = getCompanyEmail(driver)

        print("Got here")

        # Get founder(s)
        founders = getFounders(driver)

        print("got out of there")
        print(founders)

        foundersDetails = {
            "Founder Name": [],
            "Founder LinkedIn profile": []
        }

        sleep(2)

        for founder in founders:
            foundersDriver.get(founder)

            # Get name
            foundersDetails["Founder Name"].append(getName(foundersDriver))

            # Get Linkedin
            foundersDetails["Founder LinkedIn profile"].append(getLinkedin(foundersDriver))

        savedData["Company Website"].append(website)
        savedData["Company Email"].append(email)
        savedData["Company Funding"].append(funds)
        savedData["Company Founders"].append(foundersDetails)

    if os.path.isfile('app/static/data.csv'):
        os.remove('app/static/data.csv')

    df = pd.DataFrame.from_dict(savedData)
    df.to_csv('app/static/data.csv', index=False, header=True)

    # we delete the auxiliary file when we don't need it anymore
    os.remove(nameOfFile)


    #print("Enter the description of the companies you want to search for, separated by commas and no spaces, or leave it blank")

    #descriptionKeywords = str(input()).split(", ")

    #print("Enter the headquarters location or leave it blank")

    #headquartersLocation = str(input())

    #print("Enter the industry of the companies you want to search for, separated by commas and no spaces, or leave it blank")

    #industry = str(input()).split(", ")


