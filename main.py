import re

from selenium import webdriver
from selenium.webdriver.firefox.webelement import FirefoxWebElement
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from datetime import datetime

if __name__ == "__main__":

    driver = webdriver.Firefox()

    neededIndustry = "fintech"
    data = pd.read_csv("crunchbase.csv")

    isNeededIndustry = data['Industries'].str.lower().str.contains(neededIndustry, na=False)

    fintechCompanies = data[isNeededIndustry]
    fintechCompaniesURLs = fintechCompanies["Organization Name URL"].to_list()
    fintechCompaniesFunding = fintechCompanies["Total Funding Amount Currency (in USD)"].to_list()

    URLAndFunding = []

    for index in range(len(fintechCompaniesURLs)):
        URLAndFunding.append((fintechCompaniesURLs[index], fintechCompaniesFunding[index]))

    year = re.search("[0-9]{4}", "ceva 1245").group(0)
    year = int(year)

    #the age of the company
    filterDifference = 2

    thisYear = int(datetime.now().year)

    print(thisYear - year >= filterDifference)
