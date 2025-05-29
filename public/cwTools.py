# Main V4
# Create a system where whenever the websites are refreshed it doesn't recreate every single article,
# instead it only appends the one that wasn't there before.
import gazpacho
from urllib.request import Request, urlopen
from datetime import datetime

posts_raw = {}

def update_risky_buisness(): 
    test_n = 0
    global posts_raw
    website_name, website_url = 'Risky Business', 'https://risky.biz/newsletters/'
     #↓ Create a gazpacho compatible object from the website's HTML
    website = gazpacho.Soup(gazpacho.get(website_url))
     #↓ Makes a list of all the articles, each object containing the contents within each consecutive tag named "article"
    articles_raw = website.find("article", mode="all")
    for article in articles_raw:
        print(test_n := test_n + 1)
        #NOTE Add logo with the website's href.
         #↓ Assign the title of the current article to a variable.
        post_title = article.find("a", mode="first").text
        #NOTE This way seems a lot more efficient and easier on the eyes compared to V1. Instead of looping through every post in the posts list, I only look for the one post I need.
         #↓ Check whether the current article is already within the posts list.
        if (website_name, post_title) in posts_raw:
            return website_name + " is up to date"
        else:
            posts_raw.update({
                (website_name, post_title) : {
                "website_url" : website_url,
                "article_url" : "https://risky.biz" + str(_:=article.find("a", mode="first"))[9:str(_).index('">')],
                "category" : (_:=article.find("h3", mode="all"))[0],
                "date" : datetime.strptime(_[1].text, "%B %d, %Y"), #NOTE Turn this into dateTime object for processing.
                "writer": article.find("strong", mode="first").text,
                "content" : [_.text for _ in article.find("div", {"class":"post-content-html"}, mode="all")[0].find("p", mode="all")]}})
    return f"Initial setup of {website_name} posts is completed!"

                    
def update_hacker_news():
    test_n = 0
    global posts_raw
    website_name, website_url = 'The Hacker News', 'https://thehackernews.com/'
     #↓ Create a gazpacho compatible object from the website's HTML.
    website = gazpacho.Soup(gazpacho.get(website_url))
     #↓ Makes a list of all the blogs, each object containing the contents within each consecutive tag named "div" with a class value of "body-post clear".
    blogs_raw = website.find("div", {"class":"body-post clear"}, mode="all")
    for blog in blogs_raw:
        print(test_n := test_n + 1)
        #NOTE Add logo with the website's href
         #↓ Assign the title of the current article to a variable.
        post_title = blog.find("h2", mode="first").text
         #↓ Check whether the current article is already within the posts list.
        if (website_name, post_title) in posts_raw:
            return website_name + " is up to date"
        else:
            posts_raw.update({
                (website_name, post_title) : {
                "website_url" : website_url,
                "article_url" : (_:=str(blog.find("a", {"class":"story-link"}, mode="first")))[28:_.index('">')],
                "category" : blog.find("span", {"class":"h-tags"}, mode="first"),
                "date" : datetime.strptime(blog.find("span", {"class":"h-datetime"}, mode="first").strip()[1:], "%b %d, %Y"),
                "writer" : "", # To get the writer, the article page would need to be accessed.
                #"image_url" : blog.find("div", {"class":"img-ratio"}, mode="first").find("img", mode="first").attrs["src"],
                "content" : [blog.find("div", {"class":"home-desc"}, mode="first").text]}})
    return f"Initial setup of {website_name} posts is completed!"
    #order the articles by date published


def update_security_week():
    test_n = 0
    global posts_raw
    website_name, website_url = 'Security Week', "https://www.securityweek.com/"
     #↓ Create a gazpacho compatible object from the website's HTML, I had go take extra steps in order to avoid getting the "403 Forbidden" error since the website rightfully blocked the default user used by gazpacho. Rightfully because I did sent like 11 requests all at once every time I ran the code.
    website = gazpacho.Soup(str(urlopen(Request(website_url, headers={'User-Agent':'Mozilla/5.0'})).read()))
     #↓ Makes a list of all the news posts, each object containing the contents within each consecutive tag named "section" with a class value of "zox-art-wrap zoxrel zox-art-small".
    news_raw = website.find("section", {"class":"zox-art-wrap zoxrel zox-art-small"}, mode="all")
    for news in news_raw:
        print(test_n := test_n + 1)
        if test_n >= 12:
            break
        #NOTE Add logo with the website's href
         #↓ Assign the title of the current article to a variable.
        post_title = news.find("h2", mode="first").text
         #↓ Check whether the current article is already within the posts list.
        
        if (website_name, post_title) in posts_raw:
            return website_name + " is up to date"
        else:
            posts_raw.update({
                (website_name, post_title) : {
                "website_url" : website_url,
                "article_url" : (_:=news.find("a", mode="first").attrs["href"]),
                "category" : (_:=gazpacho.Soup(str(urlopen(Request(_, headers={'User-Agent':'Mozilla/5.0'})).read())).find("header", {"class":"zox-post-head-wrap left zoxrel zox100"}, mode="first")).find("span", {"class":"zox-post-cat"}, mode="first"),
                "date" : datetime.strptime(_.find("time", {"class":"post-date updated"}, mode="first").text.replace('\\n', '').replace('\\t', ''), "%B %d, %Y"),
                "writer" : _.find("span", {"class":"zox-author-name vcard fn author"}, mode="first").text,
                #"image_url" : _.find("img", mode="first").attrs["src"] if (_:=_.find("div", {"class":"zox-post-img left zoxrel zoxlh0"}, mode="first")) else None,
                "content" : [(news.find("p", {"class":"zox-s-graph"}, mode="first").text).replace('\\r', '').replace('\\n', '').replace('\\t', ''), "%B %d, %Y"]}})
    return f"Initial setup of {website_name} posts is completed!"


def update_bleeping_computer(): 
    test_n = 0
    global posts_raw
    website_name, website_url = 'BleepingComputer', 'https://www.bleepingcomputer.com/'
     #↓ Create a gazpacho compatible object from the website's HTML
    website = gazpacho.Soup(gazpacho.get(website_url))
     #↓ Makes a list of all the articles, each object containing the contents within each consecutive tag named "article"
    articles_raw = website.find("div", {"class":"bc_latest_news"}, mode="first").find("li", mode="all")
    for article in articles_raw:
         #↓ Checks whether the current article has a category at all, or whether its part of the "Deals" category, in either case it means that it's an ad.
        if (post_category:=article.find("span", mode="first")) == None or post_category.text == "Deals": 
            continue
        print(test_n := test_n + 1)
        #NOTE Add logo with the website's href.
         #↓ Assign the title of the current article to a variable.
        post_title = article.find("h4", mode="first").find("a", mode="first").text
         #↓ Check whether the current article is already within the posts list.
        if (website_name, post_title) in posts_raw:
            return website_name + " is up to date"
        else:
            posts_raw.update({
                (website_name, post_title) : {
                "website_url" : website_url,
                "article_url" : str(_:=(article.find("h4", mode="first").find("a", mode="first")))[9:str(_).index('">')],
                "category" : post_category.text,
                "date" : datetime.strptime((_:=article.find("ul")).find("li", {"class":"bc_news_date"}, mode="first").text, "%B %d, %Y"),
                "writer": _.find("li", {"class":"bc_news_author"}, mode="first").text,
                #"image_url" : str(_:=article.find("img", mode="first"))[10:str(_).index('" alt')],
                "content" : [article.find("p", mode="first").text]}})
    return f"Initial setup of {website_name} posts is completed!"


URLS = {'Risky Business' : update_risky_buisness,
            'The Hacker News' : update_hacker_news,
            #'Security Week' : update_security_week,
            'BleepingComputer' : update_bleeping_computer}
    
def update_posts():
    global URLS
    for url in URLS:
        print(URLS[url]())
    return sorted(posts_raw.items(), key=lambda post: post[1]["date"], reverse=True)
