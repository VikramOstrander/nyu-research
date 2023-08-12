# ------------
# scrapy healthgrades_spider
# refer to readme.txt for usage
# ------------

import scrapy
import re

class Spider(scrapy.Spider):
    name = "healthgrades_spider"

    # constructor to pass arguments and download url list
    def __init__(self, start=None, num=None, *args, **kwargs):

        # initialize the spider
        super(Spider, self).__init__(*args, **kwargs)
        index = int(start)
        num_urls = int(num)

        # download the urls from urls.csv
        urls = open("C:\\Users\\vikra\\NYU_2023\\data\\urls.csv", 'r')
        all_lines = urls.readlines()

        # select the correct subset of urls
        lines = []
        for i in range(index, min(index+num_urls, len(all_lines))):
            lines.append(all_lines[i].strip())
        self.start_urls = lines

    # parse and collect data from a url
    def parse(self, response):

        # filter out doctors with no ratings and redirects
        rating = response.xpath('//*[@id="premium-review-section"]/div/div[1]/div[1]/div/div/div/div/p/strong/text()').get()
        if rating is None:
            return()

        # scrape general doctor information: id, name, specialty
        id = response.url[response.url.rfind('-')+1:]
        name = response.css("h1::text").get()
        specialty = response.xpath('//*[@id="about-me-section"]/div[2]/section/div/ul/li/span/text()').get()

        # scrape and format number of reviews
        num_ratings = response.xpath('//*[@id="premium-review-section"]/div/div[1]/div[1]/div/div/div/div/div/p/text()').get()
        num_ratings = re.search(r'\d+', num_ratings).group(0)
        
        # scrape and format address information: location, zipcode
        location = response.css("address").get()
        location = location[re.search(r'>\d+', location).start()+1:re.search(r'\d<', location).start()+1]
        location = re.sub(r'<.*?>', '', location)
        zipcode = location[location.rfind(' ')+1:]

        # scrape and format textual reviews
        textual_reviews = []
        for review in response.css("div.l-single-comment-container"):
            review_rating = review.css("div.c-single-comment__summary").get()[109:110]
            review_text = review.css("div.c-single-comment__comment").get()
            review_text = re.sub(r'<.*?>', ' ', review_text)
            review_text = ' '.join(review_text.split())
            textual_reviews.append(f'{review_rating}: {review_text}')

        # output collected fields to be appended to doctors.csv
        yield {
            "ID": id,
            "Name": name,
            "Specialty": specialty,
            "Rating": rating,
            "Number of Ratings": num_ratings,
            "Location": location,
            "Zipcode": zipcode,
            "Textual Reviews": textual_reviews
        }
