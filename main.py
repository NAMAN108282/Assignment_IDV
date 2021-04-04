from selenium import webdriver
import time
import csv
from bs4 import BeautifulSoup

from selenium.common.exceptions import TimeoutException
chromedriver = "chromedriver.exe"
url = 'https://idv.gicouncil.in/'
driver=webdriver.Chrome(executable_path=chromedriver)

# csv file
with open('IDV.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    headers = ['VEHICLE TYPE','STATE','MONTH', 'YEAR','MAKE', 'MODEL', 'VARIANT', 'IDV_VALUE']
    writer.writerow(headers)

vehicle_type = 'Two Wheeler'
month = 'March'
year = '2021'

try:
    driver.set_page_load_timeout(100)
    driver.get(url)

    # drop down select for two wheeler
    wheel_dropdown = driver.find_element_by_xpath('//select[@id="vehicle-type"]')
    wheel_dropdown.find_element_by_xpath('.//option[text()="Two Wheeler"]' ).click()

    # drop down select for year 2021
    wheel_dropdown = driver.find_element_by_xpath('//select[@id="year"]')
    wheel_dropdown.find_element_by_xpath('.//option[text()="%s"]' %year).click()

    # find states list
    state_dropdown = driver.find_element_by_xpath('//select[@id="state"]')
    time.sleep(0.1)
    states = [state.text for state in state_dropdown.find_elements_by_tag_name('option')]
    states = states[1:]

    # drop down select for month
    wheel_dropdown = driver.find_element_by_xpath('//select[@id="month"]')
    wheel_dropdown.find_element_by_xpath('.//option[text()="%s"]' %month).click()

    # find makes list
    for state in states:
        state_dropdown.find_element_by_xpath('.//option[text()="%s"]' % state).click()
        time.sleep(0.1)
        make_dropdown = driver.find_element_by_xpath('//select[@id="make"]')
        makes = [make.text for make in make_dropdown.find_elements_by_tag_name('option')]
        makes = makes[1:]

        # find model list
        for make in makes:
            make_dropdown.find_element_by_xpath('.//option[text()="%s"]' % make).click()
            time.sleep(0.1)
            model_dropdown = driver.find_element_by_xpath('//select[@id="model"]')
            models = [model.text for model in model_dropdown.find_elements_by_tag_name('option')]
            models  = models [1:]

            # find variants list
            for model in models:
                model_dropdown.find_element_by_xpath('.//option[text()="%s"]' % model).click()
                time.sleep(0.1)
                variant_dropdown = driver.find_element_by_xpath('//select[@id="variant"]')
                variants = [variant.text for variant in variant_dropdown.find_elements_by_tag_name('option')]
                variants = variants[1:]

                # write each row in  IDV.csv File
                for variant in variants:
                    variant_dropdown.find_element_by_xpath('.//option[text()="%s"]' % variant).click()
                    time.sleep(0.1)
                    submit_button = driver.find_element_by_id("showPrice").click()
                    time.sleep(0.5)
                    price = driver.find_element_by_xpath('//*[@id ="price"]').text
                    
                    # write each data row 
                    with open('IDV.csv', 'a', newline='') as file:
                        writer = csv.writer(file)
                        each_row = [vehicle_type, state, month, year, make, model, variant, price]
                        writer.writerow(each_row)







except TimeoutException as ex:
    isrunning = 0
    print("Exception has been thrown. " + str(ex))
    driver.close()
