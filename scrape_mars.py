#!/usr/bin/env python
# coding: utf-8

# # Web Scraping Homework - Mission to Mars
# 
# In this assignment, you will build a web application that scrapes various websites for data related to the Mission to Mars and displays the information in a single HTML page. The following outlines what you need to do.
# 
# ### Before You Begin
# 
# 1. Create a new repository for this project called `web-scraping-challenge`. **Do not add this homework to an existing repository**.
# 
# 2. Clone the new repository to your computer.
# 
# 3. Inside your local git repository, create a directory for the web scraping challenge. Use a folder name to correspond to the challenge: **Missions_to_Mars**.
# 
# 4. Add your notebook files to this folder as well as your flask app.
# 
# 5. Push the above changes to GitHub or GitLab.
# 
# ## Step 1 - Scraping
# 
# Complete your initial scraping using Jupyter Notebook, BeautifulSoup, Pandas, and Requests/Splinter.
# 
# * Create a Jupyter Notebook file called `mission_to_mars.ipynb` and use this to complete all of your scraping and analysis tasks. The following outlines what you need to scrape.

# In[1]:


import pandas as pd
import requests
import time
import pymongo
from splinter import Browser
from bs4 import BeautifulSoup as bs


# ### NASA Mars News
# 
# * Scrape the [NASA Mars News Site](https://mars.nasa.gov/news/) and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.
# 
# ```python
# # Example:
# news_title = "NASA's Next Mars Mission to Investigate Interior of Red Planet"
# 
# news_p = "Preparation of NASA's next spacecraft to Mars, InSight, has ramped up this summer, on course for launch next May from Vandenberg Air Force Base in central California -- the first interplanetary launch in history from America's West Coast."
# ```

# In[2]:


def Mars_News():

    # Define variables
    url = 'https://mars.nasa.gov/news/'

    '''The NASA website cannot be reqested correctly using requests.get()'''
    # # Retrieve page with the requests module
    # response = requests.get(url)
    # # Create BeautifulSoup object; parse with 'lxml'
    # soup = bs(response.text, 'html.parser')

    # Bring in the Chrome Driver
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    # Connect to the url
    browser.visit(url)
    time.sleep(3)

    # Open the website in Chrome
    html = browser.html
    soup = bs(html, 'html.parser')

    # find all the news
    news_list = soup.find_all('li', class_ = 'slide')

    # find the Mars article title
    news_title = news_list[0].find_all('div', class_ = 'content_title')
    news_title = str(news_title).split('>')[2]
    news_title = news_title.replace('</a', '') #Clean the clsoing </a> tag

    # find the paragraph
    news_p = news_list[0].find_all('div', class_ = 'article_teaser_body')
    news_p = str(news_p).split('>')[1]
    news_p = news_p.replace('</div', '')
    
    # Close the browser
    browser.quit()
    
    return news_title, news_p


# ### JPL Mars Space Images - Featured Image
# 
# * Visit the url for JPL Featured Space Image [here](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).
# 
# * Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called `featured_image_url`.
# 
# * Make sure to find the image url to the full size `.jpg` image.
# 
# * Make sure to save a complete url string for this image.
# 
# ```python
# # Example:
# featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA16225_hires.jpg'
# ```

# In[3]:


def Mars_Featured_Image():
    # JPL URL
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    # Bring in the Chrome Driver
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    # Connect to the url
    browser.visit(jpl_url)
    time.sleep(3)

    # Open the website in Chrome
    html = browser.html
    soup = bs(html, 'html.parser')

    # find featured image url 
    locate_img = soup.find_all('div', class_ = 'carousel_items')
    locate_img = str(locate_img).split("url(")[1].split(');')[0]
    locate_img = locate_img.replace("'", "")
    featured_image_url = 'https://www.jpl.nasa.gov' + locate_img
    
    # Close the browser
    browser.quit()
    
    return featured_image_url


# ### Mars Weather
# 
# * Visit the Mars Weather twitter account [here](https://twitter.com/marswxreport?lang=en) and scrape the latest Mars weather tweet from the page. Save the tweet text for the weather report as a variable called `mars_weather`.
# * **Note: Be sure you are not signed in to twitter, or scraping may become more difficult.**
# * **Note: Twitter frequently changes how information is presented on their website. If you are having difficulty getting the correct html tag data, consider researching Regular Expression Patterns and how they can be used in combination with the .find() method.**
# 
# 
# ```python
# # Example:
# mars_weather = 'Sol 1801 (Aug 30, 2017), Sunny, high -21C/-5F, low -80C/-112F, pressure at 8.82 hPa, daylight 06:09-17:55'
# ```

# In[4]:


def Mars_Weather():

    # Mars Weather Twitter url
    weather_url = 'https://twitter.com/marswxreport?lang=en'

    # Bring in the Chrome Driver
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    # Connect to the url
    browser.visit(weather_url)
    time.sleep(3)

    # Open the website in Chrome
    html = browser.html
    soup = bs(html, 'html.parser')

    # find Mars Weather 
    all_tweets = soup.find_all('div', class_ = 'css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0')
    mars_weather = str(all_tweets[0]).split('>')[2].replace('\n', ' ').replace('</span', '')
    
    # Close the browser
    browser.quit()

    return mars_weather


# ### Mars Facts
# 
# * Visit the Mars Facts webpage [here](https://space-facts.com/mars/) and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
# 
# * Use Pandas to convert the data to a HTML table string.

# In[14]:


def Mars_Facts():

    # Mars Facts URL
    facts_url = 'https://space-facts.com/mars/'

    # Read all tables from the website
    tables = pd.read_html(facts_url)

    # find the fact table
    facts = tables[0]

    # Rename column names
    facts = facts.rename(columns = {0:'Description', 1:'Value'})

    # Save the table as HTML
    facts.to_html('facts.html', index = False)
    
    # read the HTML file back in
    with open('facts.html', 'r') as f:
        mars_facts = f.read()
        
    # Remove all the \n
    mars_facts = mars_facts.replace('\n', '')

    return mars_facts


# ### Mars Hemispheres
# 
# * Visit the USGS Astrogeology site [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) to obtain high resolution images for each of Mar's hemispheres.
# 
# * You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
# 
# * Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys `img_url` and `title`.
# 
# * Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.
# 
# ```python
# # Example:
# hemisphere_image_urls = [
#     {"title": "Valles Marineris Hemisphere", "img_url": "..."},
#     {"title": "Cerberus Hemisphere", "img_url": "..."},
#     {"title": "Schiaparelli Hemisphere", "img_url": "..."},
#     {"title": "Syrtis Major Hemisphere", "img_url": "..."},
# ]
# ```

# In[6]:


def Mars_Hemi():

    USGS_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    hemisphere_image_urls = []

    # Bring in the Chrome Driver
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    # Connect to the url
    browser.visit(USGS_url)
    time.sleep(3)

    # Open the website in Chrome
    html = browser.html
    soup = bs(html, 'html.parser')

    # find all the links
    links = soup.find_all('div', class_ = 'item')

    sub_page_links = []
    for link in links:
        #sub_page_url = 'https://astrogeology.usgs.gov' + str(link).split('href="')[1].split('"><')[0]
        sub_page_link = str(link).split('h3')[1].replace('>', '').replace('</', '')
        sub_page_links.append(sub_page_link)

    img_url_list = []
    for link in sub_page_links:
        browser.click_link_by_partial_text(link)
        time.sleep(2)

        # find the img url
        html = browser.html
        soup = bs(html, 'html.parser')
        img_url = soup.find_all('li')
        img_url = str(img_url).split('<li><a href="')[1].split('"')[0]

        img_url_list.append(img_url)

        # Go Back
        browser.back()

    # create hemisphere_image_urls
    hemisphere_image_urls = []

    for i in range(0, len(sub_page_links)):
        temp_dict = {}

        temp_dict['title'] = sub_page_links[i]
        temp_dict['img_url'] = img_url_list[i]

        hemisphere_image_urls.append(temp_dict)
        
    # Close the browser
    browser.quit()
    
    return hemisphere_image_urls


# In[7]:


def scrape():
    print("Start scraping Mars News...")
    news_title, news_p = Mars_News()
    print("Completed")
    
    print("Start scraping Mars featured image...")
    featured_image_url = Mars_Featured_Image()
    print('Completed')
    
    print("Start scraping Mars weather...")
    mars_weather = Mars_Weather()
    print("Completed")
    
    print("Start scraping Mars facts...")  
    mars_facts = Mars_Facts()
    print("Completed")
    
    print("Start scraping Mars Hemispheres...")
    hemisphere_image_urls = Mars_Hemi()
    print("Completed")
    
    # Put everything into a dictionary
    
    results_dict = {
        'news_title' : news_title,
        'news_p'     : news_p,
        'featured_image_url' : featured_image_url,
        'mars_weather' : mars_weather,
        'mars_facts'   : mars_facts,
        'hemisphere_image_urls' : hemisphere_image_urls
    }
    
    return results_dict


# In[8]:


# results = scrape()


# In[ ]:




