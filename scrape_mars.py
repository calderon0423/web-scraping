#import dependencies 
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time 
import pandas as pd
import re
import time

def scrape_info():
    browser = Browser('chrome', executable_path='/usr/local/bin/chromedriver', headless=False)
    
    url = 'https://mars.nasa.gov/news/'
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser.visit(url)
    
    time.sleep(1)
    
    #scrape page into Soup 
    html = browser.html
    soup = bs(html, 'html.parser')
    
    #get the news title 
    news_title = soup.find('div', class_='list_text').a.text
    
    #get the news paragraphs
    news_p = soup.find('div', class_='article_teaser_body').text
        
    #visit jpl url 
    browser.visit(jpl_url)
    html = browser.html
    soup = bs(html, 'html.parser')
    
    #get latest image - hi-res 
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)

    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text('more info')

    html = browser.html
    soup = bs(html, 'html.parser')

    image = soup.find('figure', class_='lede')
    image_url = image.a['href']
    featured_image_url = f'https://jpl.nasa.gov{image_url}'
    
    #get latest tweet 
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)

    time.sleep(2)

    pattern = re.compile('InSight')

    html = browser.html
    soup = bs(html, 'html.parser')

    mars_weather = soup.find('span', text=pattern).text
    
    #table 
    facts_url = 'https://space-facts.com/mars/'
    table = pd.read_html(facts_url)
    df = table[0]
    df.columns = ['Description','Values']
    df.set_index('Description', inplace=True)
    df_html = df.to_html()
    
    #Mars Hemispheres 
    hemisphere_image_url = []
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)

    html = browser.html
    soup = bs(html, 'html.parser')

    #get the title 
    info = soup.find_all('div', class_='item')

    for hemisphere in info: 
        hemisphere_dict = {}
        hemisphere_dict['title'] = hemisphere.find('h3').text
        hemisphere_image_url.append(hemisphere_dict)
        browser.click_link_by_partial_text(hemisphere.find('h3').text)
        html = browser.html
        soup = bs(html, 'html.parser')
        url = soup.find('img', class_='wide-image')['src']
        hemisphere_dict['image_url'] = f'https://astrogeology.usgs.gov{url}'
        browser.visit(hemisphere_url)

        
    #store data in a dictionary
    mars_data= {
        'news_title': news_title,
        'news_paragraph': news_p,
        'featured_image_url': featured_image_url,
        'mars_weather': mars_weather,
        'mars_table': df_html,
        'mars_hemispheres': hemisphere_image_url
    }
        
        
    #close the browser
    browser.quit()
    
    return mars_data 