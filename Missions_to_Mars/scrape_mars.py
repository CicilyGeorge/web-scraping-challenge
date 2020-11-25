# Dependencies
###
import pandas as pd
import requests
from pprint import pprint
import re

from bs4 import BeautifulSoup
from splinter import Browser
from selenium import webdriver


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    try:
        browser = init_browser()
        # create surf_data dict that we can insert into mongo
        mars_data = {}
        mars_data['loaded'] = False

        ##################################################
        #Using splinter extracting the Latest News
        ##################################################

        #Visit Nasa's JPL Mars Space url using splinter
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)

        #create HTML object
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        # Retrieve the latest news title and news paragraph
        news_title = soup.find('ul', class_='item_list')\
                        .find('div', class_='content_title')\
                        .find('a').text

        news_p  = soup.find('ul', class_='item_list').find('div', class_='article_teaser_body').text

        # add our news_title to mars data with a key of news_title
        mars_data["news_title"] = news_title
        mars_data["news_p"] = news_p


        ##################################################
        # Using splinter Extracting the latest featured Image url
        ##################################################

        #Visit Nasa's JPL Mars Space url using splinter
        jpl_url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(jpl_url)

        #create HTML object
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        #get image url from the soup object.
        featured_image_url = soup.find('div', class_='carousel_items')\
                                .find('article').attrs['style'][23:-3]
        #get base Nasa jpl link
        base_url = 'https://www.jpl.nasa.gov'

        #Create one full image url link
        featured_image_url = base_url + featured_image_url

        # add our featured_image_url to mars data with a key of featured_image_url
        mars_data["featured_image_url"] = featured_image_url


        ##################################################
        # Using splinter Extracting the Mars facts table
        ##################################################
        url = 'https://space-facts.com/mars/'
        tables = pd.read_html(url)
        df = tables[0]
        df.columns = ['Feature', 'Value']
        df.set_index('Feature', inplace=True)
        # Converting dataframe to html using pandas to_html()
        html_table = df.to_html()

        # Removing thead from the html code
        html_table = re.sub('<thead.+?</thead>','',html_table,flags=re.DOTALL)
        # Removing unnecessary newlines
        html_table = html_table.replace('\n', '')

        # add our html_table to mars data with a key of mars_facts
        mars_data["mars_facts"] = html_table


        ##################################################
        # Using splinter Extracting the latest featured Image url
        ##################################################

        #Visit Nasa's JPL Mars Space url using splinter
        hemisphere_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemisphere_url)

        #create HTML object
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        #get image url from the soup object.
        results = soup.find_all('div', class_='description')

        #get base Nasa mars hemisphere link
        base_url = 'https://astrogeology.usgs.gov'

        # An empty list to hold a dictionary of Hemisphere image title and url 
        hemisphere_image_urls = []
        # Loop through returned results
        for result in results:
            # try:
            # Retrieve the Hemisphere title
            title = result.find('h3').text[:-9]
            link = base_url + result.a['href']
            # Visit each Hemisphere page with link
            browser.visit(link)
            page = browser.html
            img_soup = BeautifulSoup(page, 'html.parser')
            img_url = img_soup.find('div', class_='downloads').find('a').attrs['href']
                
            img_dict = {'title':title, 'img_url':img_url}
            hemisphere_image_urls.append(img_dict)
                
            # except AttributeError as e:
            #     print(e)

        # add our hemisphere_image_urls list of dicts to mars_data dict
        mars_data["hemisphere_image_urls"] = hemisphere_image_urls


        browser.quit()
        mars_data['loaded'] = True
    except AttributeError as e:
            print(e)
    except:
        print(e)
    return mars_data




