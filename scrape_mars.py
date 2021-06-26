import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
from datetime import datetime
import os
import time

# Link to Chrome Browser
executable_path = {'executable_path':"C:\Program Files\Google\Chrome\Application\chromedriver.exe"}
browser = Browser("chrome", **executable_path, headless=False)

#News Scraper
def mars_news(browser):
    #open browser
    url = "https://redplanetscience.com/"
    browser.visit(url)
    #using bs to scrape html
    html = browser.html
    soup = bs(html,"html.parser")

    try:
        news_title = soup.find("div",class_="content_title").text
        news_p = soup.find("div", class_="article_teaser_body").text

    except AttributeError:
        return None, None
    return news_title, news_p

### JPL Mars Space Images - Featured Image
def mars_image(browser):
# Page to visit
    url = "https://spaceimages-mars.com/"
    browser.visit(url)

    #using bs to scrape html
    html = browser.html
    soup = bs(html,"html.parser")

    try:
        featured_image_url = soup.find("a" ,target="_blank", class_="showimg fancybox-thumbs")["href"]
    except AttributeError:
        return None
    return featured_image_url

def mars_facts(browser):
        #Mars Facts
    fact_url = "https://galaxyfacts-mars.com"
    try:
        table = pd.read_html(fact_url)
        fact_df1 = pd.DataFrame(table[0])
        fact_df2 = pd.DataFrame(table[1])
        fact_df = pd.merge(fact_df1,fact_df2,how='outer').drop(columns=[2]).drop(0).rename(columns={0:'Measurement',1:'Value'}).reset_index(drop=True)
        html_table = fact_df.to_html()

    except AttributeError:
        return None
    return html_table(classes="table table-striped")

def hemisphere(browser):
    hemisphere_url = "https://marshemispheres.com/"
    browser.visit(hemisphere_url)

    hemisphere_image_urls = []

    #scraping loop

    links = browser.find_by_css("a.product-item h3")
    for item in range(len(links)):
        hemisphere = {}

        browser.find_by_css("a.product-item h3")[item].click()
        picture = browser.links.find_by_text("Sample").first
        hemisphere["img_url"] = picture["href"]
        hemisphere["title"] = browser.find_by_css("h2.title").text
        hemisphere_image_urls.append(hemisphere)
        browser.back()

    return hemisphere_image_urls

# Main Web Scraping Bot
def scrape_all():
    executable_path = {"executable_path": "C:\Program Files\Google\Chrome\Application\chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless=False)
    news_title, news_p = mars_news(browser)
    featured_image_url = mars_image(browser)
    facts = mars_facts(browser)
    hemisphere_image_urls = hemisphere(browser)

    data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": featured_image_url,
        "facts": facts,
        "hemispheres": hemisphere_image_urls,
    }
    browser.quit()
    return data

if __name__ == "__main__":
    print(scrape_all())
