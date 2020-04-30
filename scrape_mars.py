#dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import requests
import pandas as pd

#intialize the chrome browser.
def init_browser():
        executable_path = {'executable_path':'/usr/local/bin/chromedriver'}
        return Browser('chrome', **executable_path, headless=False)

#define the scraping class. 
def scrape():

        browser = init_browser()

        nasa_mars_news_url = "https://mars.nasa.gov/news/"
        nasa_mars_image_url = "https://www.jpl.nasa.gov/spaceimages/"
        nasa_mars_weather_url = "https://twitter.com/marswxreport?lang=en"
        nasa_mars_facts_url = "https://space-facts.com/mars/"
        nasa_mars_hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"


#mars news response and create soup object to store the response. 
        nasa_mars_news_response = requests.get(nasa_mars_news_url)
        news_soup = BeautifulSoup(nasa_mars_news_response.text, 'html.parser')


        news_results = news_soup.find_all(class_="slide")
        news_titles = []
        news_paras = []
#within the response class, find all links that contains the news title and paras. 
        for result in news_results:
   
                links = result.find_all('a')
                title = links[1].text
                paragraphs = result.find(class_="rollover_description_inner").text
    
                news_titles.append(title)
                news_paras.append(paragraphs)

#use splinter to visit the image url. 
        url = nasa_mars_image_url
        browser.visit(url)

        html = browser.html
        image_soup = BeautifulSoup(html, 'html.parser')
#find all the image within the carousel class. 
        image_results = image_soup.find_all(class_="carousel_items")

        for result in image_results:
#loop to find all the image links. 
                article = result.find('article', class_="carousel_item")
                article_link = article['style']
                featured_image = article['style'].lstrip('background-image: url(')
                featured_image = featured_image.rstrip(');')

#remove unwanted spaces and get the complete image link. 
                featured_image = featured_image.replace("'", "")
                featured_image_url = 'https://www.jpl.nasa.gov'+featured_image

        nasa_mars_weather_response = requests.get(nasa_mars_weather_url)
        weather_soup = BeautifulSoup(nasa_mars_weather_response.text, 'html.parser')

#weather response and store the weather tweets in a list. 
        weather_results = weather_soup.find_all(class_="content")
        weather_tweets = []

        for result in weather_results:
    
                tweets = result.find('p',class_="TweetTextSize").text
                weather_tweets.append(tweets)
#show the first tweet. 
                mars_weather = weather_tweets[0]
#get the mars facts and put them in a dictionary. 
        mars_facts = pd.read_html(nasa_mars_facts_url)
        mars_facts

        fact_keys = list(mars_facts[0][0])
        fact_values = list(mars_facts[0][1])

        fact_dict = dict((fact_keys[x], fact_values[x]) for x in range (0,len(fact_keys)))
#create a dataframe. 
        mars_fact_data = pd.DataFrame(fact_dict, index=[0])
        mars_fact_data

#set the base url and list to hold the data. 
        hemisphere_url= 'https://astrogeology.usgs.gov'
        hemisphere_list = []
        hemisphere_response = requests.get(nasa_mars_hemisphere_url)
#create soup object for the response. 
        hemisphere_soup = BeautifulSoup(hemisphere_response.text, 'html.parser')

        results = hemisphere_soup.find_all(class_='item')
#loop through to find the links and specific link within the links. 
        for result in results:

        
                links = result.find('a')

                link=links['href']
#add ech link to the list.
                hemisphere_list.append(hemisphere_url+link)

        browser.visit(nasa_mars_hemisphere_url)
#for all the 4 url image links, click each image url as it is processed. 
        hemispheres_image_urls = []
        titles_list = []
        for x in range(0, 4):

          browser.visit(hemisphere_list[x])


          html = browser.html
          soup = BeautifulSoup(html, 'html.parser')

          images = soup.find(class_='downloads')

          image = images.find('a')
          image_url= image['href']

          hemispheres_image_urls.append(image_url)

          titles = soup.find('h2', class_='title')
          title=titles.text
          title=title.strip('Enhanced')
          titles_list.append(title)
#create a dictionary to store the image title and url.
        hemisphere_dict = {"Title":titles_list,
                  "URL":hemispheres_image_urls}
#create a dictionary to hold all the data we scraped. 
        scraped_data = {'Title': titles_list,
                'URL': hemispheres_image_urls,
                'Weather': mars_weather,
                'Featured Image': featured_image_url,
                'News Title': news_titles,
                'News Body': news_paras
               }
        return scraped_data




