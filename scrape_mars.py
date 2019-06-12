# Import modules
import pandas as pd
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
import requests
from selenium import webdriver

# Inititialize browser
def init_browser():
    executable_path = {'executable_path':'chromedriver.exe'}
    return Browser('chrome',**executable_path, headless = True)

# Creating dictionary with scraped data
mars_dict = {}

# Scrape News 
def scrape_mars_news():
    try:
        # Initialize browser
        browser = init_browser()

        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)

        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        news_t = soup.find('div', class_='content_title').find('a').text
        news_p = soup.find('div', class_='article_teaser_body').text

        mars_dict['news_t'] = news_t
        mars_dict['news_p'] = news_p

        return mars_dict

    finally: 
        browser.quit()

# Scrape Featured Image
def scrape_mars_feat_image():
    try:
        # Initialize browser
        browser = init_browser()

        img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(img_url)

        img_html = browser.html
        soup = BeautifulSoup(img_html, 'html.parser')

        img_results = soup.find_all('a', class_='button fancybox')

        for result in img_results:   
            featured_image_url = 'https://www.jpl.nasa.gov' + result['data-fancybox-href']
    
        mars_dict['featured_image_url'] = featured_image_url

        return mars_dict
    
    finally:
        browser.quit()

# Scrape Twitter
def scrape_mars_weather():

    try:
        # Initialize browser
        browser = init_browser()

        weather_url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(weather_url)

        weather_html = browser.html
        soup = BeautifulSoup(weather_html, 'html.parser')

        weather_results = soup.find_all('div', class_='js-tweet-text-container')

        for weather_result in weather_results:
            mars_weather = weather_result.find('p', class_='TweetTextSize').text
            print(mars_weather)
            break

        mars_dict['mars_weather'] = mars_weather

        return mars_dict

    finally:
        browser.quit()

# Scrape Mars Facts
def scrape_mars_facts():
    facts_url = 'https://space-facts.com/mars/'

    tables = pd.read_html(facts_url)

    df = tables[0]
    df.rows = ['Equatorial Diameter', 'Polar Diameter', 'Mass', 'Moons', 
              'Orbit Distance', 'Orbit Period', 'Surface Temperature', 'First Record', 
              'Recorded By']

    df.columns = ['Fact', 'Value']
    df.set_index('Fact', inplace = True)
    
    html_table = df.to_html()
    html_table

    html_table.replace('\n', '')

    # Add HTML code for dataframe to dictionary
    mars_dict['mars_facts'] = html_table

    return mars_dict

# Scrape Mars Hemispheres
def scrape_mars_hemispheres():

    try: 
        # Initialize browser
        browser = init_browser()

        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)

        hemispheres_html = browser.html
        soup = BeautifulSoup(hemispheres_html, 'html.parser')

        # Iterate through allhemispheres
        hem_list = ['Cerberus','Schiaparelli', 'Syrtis Major', 'Valles Marineris']

        hemisphere_image_urls =[]
        
        for hem in hem_list:
            browser.click_link_by_partial_text(hem)
            title = browser.find_by_tag('h2').text
            img_url= (browser.find_by_xpath('//*[@id="wide-image"]/img')['src'])
            hemisphere_image_urls.append({"title":title,"img_url":img_url})
            browser.visit(hemispheres_url)

        mars_dict['hemisphere_image_urls'] = hemisphere_image_urls

        return mars_dict
    
    finally: 
        browser.quit()