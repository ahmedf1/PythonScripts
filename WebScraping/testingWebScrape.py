from selenium import webdriver
from selenium import *
from selenium.webdriver.common.keys import Keys
import time
import parameters
from parsel import Selector

driver =  webdriver.Chrome(r'C:\Users\fahmed\Desktop\chromedriver')

driver.get(r'https://www.linkedin.com/uas/login?trk=guest_homepage-basic_nav-header-signin')

username = driver.find_element_by_id('username')

username.send_keys(parameters.username)

password = driver.find_element_by_id('password')

password.send_keys(parameters.password)


log_in_button = driver.find_element_by_css_selector('button[type="submit"]')
print(log_in_button)
log_in_button.click()

driver.get(r'https://www.google.com')
time.sleep(10)

#driver.get(r'https://www.linkedin.com/feed/')

google_searchBar = driver.find_element_by_name('q')


google_searchBar.send_keys(parameters.search_query)

google_searchBar.send_keys(Keys.RETURN)

linkedin_urls = driver.find_elements_by_class_name('iUh30')

linkedin_urls = [url.text for url in linkedin_urls]

#print(linkedin_urls)

for url in linkedin_urls:
    driver.get(url)
    time.sleep(5)
    sel = Selector(text=driver.page_source)
    print('\n')
    # xpath to extract the text from the class containing the name
    name = sel.xpath('//*[starts-with(@class, "pv-top-card-section__name")]/text()').extract_first()

    if name:
        name = name.strip()
        print('Name: ' + name)


    # xpath to extract the text from the class containing the job title
    job_title = sel.xpath('//*[starts-with(@class, "pv-top-card-section__headline")]/text()').extract_first()

    if job_title:
        job_title = job_title.strip()
        print('Job Title: ' + job_title)


    # xpath to extract the text from the class containing the company
    company = sel.xpath('//*[starts-with(@class, "pv-top-card-v2-section__entity-name pv-top-card-v2-section__company-name")]/text()').extract_first()

    if company:
        company = company.strip()
        print('Company: ' + company)


    # xpath to extract the text from the class containing the college
    college = sel.xpath('//*[starts-with(@class, "pv-top-card-v2-section__entity-name pv-top-card-v2-section__school-name")]/text()').extract_first()

    if college:
        college = college.strip()
        print('College: ' + college)


    # xpath to extract the text from the class containing the location
    location = sel.xpath('//*[starts-with(@class, "pv-top-card-section__location")]/text()').extract_first()

    if location:
        location = location.strip()
        print('Location: ' + location)

    bio_expand = sel.xpath('//*[starts-with(@class, "pv-top-card-section__summary")]/text()').extract_first()
    print(bio_expand)

    bio = sel.xpath('//*[starts-with(@class, "lt-line-clamp__raw-line")]/text()').extract_first()
    if bio:
        bio = bio.strip()
        print("Bio: " + bio)

    
    # printing the output to the terminal
    print('URL: ' + url)
    print('\n')

driver.quit()

