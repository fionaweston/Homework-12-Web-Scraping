#!/usr/bin/env python
    
# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests
import time
    
    
def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)
    
    
def scrape():
    
    browser = init_browser()
    mars_data = {}

    # Visit Nasa news url through splinter module
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    
    # Retrieve the latest element that contains news title and news_paragraph
    news_title = news_soup.find('div', class_='content_title').text
    news_p = news_soup.find('div', class_='article_teaser_body').text
    
    # Save scraped data to dictionary
    mars_data['news_title'] = news_title
    mars_data['news_p'] = news_p
    
    
    # Visit Mars Space Images through splinter module
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    
    browser.visit(image_url)
    browser.click_link_by_partial_text('FULL IMAGE')
    
    # HTML Object 
    html_image = browser.html
    
    # Parse HTML with Beautiful Soup
    image_soup = BeautifulSoup(html_image, 'html.parser')
    
    # Retrieve background-image url from style tag 
    featured_image_url  = image_soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
    
    # Website Url 
    site_url = 'https://www.jpl.nasa.gov'
    
    # Concatenate website url with scrapped route
    featured_image_url = site_url + featured_image_url

    # Save scraped data to dictionary
    mars_data['featured_image_url'] = featured_image_url
    
    # Visit Mars Weather through splinter module
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    
    weather_html = browser.html
    weather_soup = BeautifulSoup(weather_html, 'html.parser')
    tweets = weather_soup.find('ol', class_='stream-items')
    weather = tweets.find('p', class_="tweet-text").text
    weather = weather.split(' ',1)[1]
    weather = weather.rsplit(' ',1)[0]

    # Save scraped data to dictionary
    mars_data['weather'] = weather
    
    
    # Visit Mars Facts through splinter module
    facts_url = 'https://space-facts.com/mars/'
    facts = pd.read_html(facts_url)
    facts_df = facts[0]
    facts_df.columns = ["Parameter", "Values"]
    
    # Convert data frame to HTML table
    facts_html_table = facts_df.to_html()
    facts_html_table = facts_html_table.replace("\n", "")
    
    # Save scraped data to dictionary
    mars_data['facts_html_table'] = facts_html_table
    
    
    # Visit Mars Hemispheres through splinter module
    hemispheres_base_url = 'https://astrogeology.usgs.gov'
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    
    hemisphere_image_urls = []
    
    # Get title and image for Ceberus
    browser.visit(hemispheres_url)
    
    browser.find_by_xpath( "//*[@id='product-section']/div[2]/div[1]/a/img").click()
    browser.find_by_xpath( "//*[@id='wide-image-toggle']").click()
    
    img_html = browser.html
    img_soup = BeautifulSoup(img_html, 'html.parser')
    img_url = img_soup.find('img', class_='wide-image')['src']
    img_url = hemispheres_base_url + img_url
    img_title = img_soup.find('h2', class_ = 'title').text
    
    hemisphere_image_urls.append({"title" : img_title, "img_url" : img_url})
    
    # Get title and image for Schiaparelli
    browser.visit(hemispheres_url)
    
    browser.find_by_xpath( "//*[@id='product-section']/div[2]/div[2]/a/img").click()
    browser.find_by_xpath( "//*[@id='wide-image-toggle']").click()
    
    img_html = browser.html
    img_soup = BeautifulSoup(img_html, 'html.parser')
    img_url = img_soup.find('img', class_='wide-image')['src']
    img_url = hemispheres_base_url + img_url
    img_title = img_soup.find('h2', class_ = 'title').text
    
    hemisphere_image_urls.append({"title" : img_title, "img_url" : img_url})
    
    # Get title and image for Syrtis
    browser.visit(hemispheres_url)
    
    browser.find_by_xpath( "//*[@id='product-section']/div[2]/div[3]/a/img").click()
    browser.find_by_xpath( "//*[@id='wide-image-toggle']").click()
    
    img_html = browser.html
    img_soup = BeautifulSoup(img_html, 'html.parser')
    img_url = img_soup.find('img', class_='wide-image')['src']
    img_url = hemispheres_base_url + img_url
    img_title = img_soup.find('h2', class_ = 'title').text
    
    hemisphere_image_urls.append({"title" : img_title, "img_url" : img_url})
    
    # Get title and image for Valles Marineris
    browser.visit(hemispheres_url)
    
    browser.find_by_xpath( "//*[@id='product-section']/div[2]/div[4]/a/img").click()
    browser.find_by_xpath( "//*[@id='wide-image-toggle']").click()
    
    img_html = browser.html
    img_soup = BeautifulSoup(img_html, 'html.parser')
    img_url = img_soup.find('img', class_='wide-image')['src']
    img_url = hemispheres_base_url + img_url
    img_title = img_soup.find('h2', class_ = 'title').text
    
    hemisphere_image_urls.append({"title" : img_title, "img_url" : img_url})
    
    
    mars_data['hemisphere_image_urls'] = hemisphere_image_urls

    return mars_data

