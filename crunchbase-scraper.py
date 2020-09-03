from selenium import webdriver
from selenium.webdriver.firefox.webelement import FirefoxWebElement
from selenium.webdriver.firefox.webdriver import WebDriver


from selenium import webdriver

from selenium.webdriver.common.keys import Keys

import pandas as pd
import json
import re
from datetime import datetime
import pwn


if __name__ == "__main__":
    driver = webdriver.Firefox()


    """driver = webdriver.Chrome()
    driver.get("http://www.python.org")
    assert "Python" in driver.title
    elem = driver.find_element_by_name("q")
    elem.clear()
    elem.send_keys("pycon")
    elem.send_keys(Keys.RETURN)
    assert "No results found." not in driver.page_source
    driver.close() """

    neededIndustry = "fintech"
    data = pd.read_csv("crunchbase.csv")

    isNeededIndustry = data['Industries'].str.lower().str.contains(neededIndustry, na = False)
    fintechCompanies = data[isNeededIndustry]

    fintechCompaniesURLs = fintechCompanies["Organization Name URL"].to_list()
    fintechCompaniesFunding = fintechCompanies["Total Funding Amount Currency (in USD)"].to_list()
    URLAndFunding = []


    for index in range(len(fintechCompaniesURLs)):
        URLAndFunding.append((fintechCompaniesURLs[index], fintechCompaniesFunding[index]))


    # urls = ["https://www.crunchbase.com/organization/the-sage-group-plc", "https://www.crunchbase.com/organization/draper"]

    infos = []
    print(f"====\n{len(URLAndFunding)} {neededIndustry} companies found, scraping data now...\n====")


    for url, funding in URLAndFunding:
        # navigate to url
        driver.get(url)

        # content = driver.find_elements_by_xpath(
        #       '//span[@class="component--field-formatter field-type-money ng-star-inserted"]'
        #       )
        # content = driver.find_element_by_xpath('//tr[@class="ng-star-inserted"]//span[@class="component--field-formatter field-type-money ng-star-inserted"]')

        # get xpath with xpath finder
        org_name = driver.find_element_by_xpath('//span[@class="profile-name"]').text

        founded_date_div = driver.find_element_by_xpath('/html/body/chrome/div/mat-sidenav-container/mat-sidenav-content/div/ng-component/entity-v2/page-layout/div/div/div/page-centered-layout[3]/div/div/div[1]/row-card[1]/profile-section/section-card/mat-card/div[2]/div/fields-card[1]/ul/li[contains(string(), "Founded Date")]')

        founded_date = founded_date_div.find_element_by_xpath('field-formatter/span').text

        about_div = driver.find_element_by_xpath('/html/body/chrome/div/mat-sidenav-container/mat-sidenav-content/div/ng-component/entity-v2/page-layout/div/div/div/page-centered-layout[2]/div/row-card/div/div[1]/profile-section/section-card/mat-card/div[2]/div/fields-card/ul')
        employees_nb = about_div.find_element_by_css_selector("a[href*='num_employees_enum']").text

        # compute age of company
        year = re.search("[0-9]{4}", founded_date).group(0)
        year = int(year)
        #the age of the company
        filterDifference = 2
        thisYear = int(datetime.now().year)
        if thisYear - year >= filterDifference:
            infos.append({"Name": org_name, "Age (in years)": thisYear - year, "Founded date": founded_date, "Number of employees": employees_nb, 'Funding amount': funding, 'Crunchbase URL': url})

    print(f"{len(URLAndFunding) - len(infos)} companies filtered out, here are the data collected for the ones that match our filters:\n")
    print(json.dumps(infos, indent=2))
    driver.close()
