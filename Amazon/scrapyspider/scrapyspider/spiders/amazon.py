# -*- coding: utf-8 -*-
import scrapy
from scrapy.utils.response import open_in_browser
from scrapy.http import FormRequest, Request
import sqlite3
import os
from .AmazonUtil.preprocess_sd import wrangle_title


def printg(*args):
    print('\n\n\n\n')
    print(*args)
    print('\n\n\n\n')

class AmazonSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = ["amazon.com"]
    start_urls = ['https://amazon.com/gp/navigation/redirector.html/ref=sign-in-redirect?ie=UTF8&associationHandle=usflex&currentPageURL=https%3A%2F%2Fwww.amazon.com%2Fgp%2Fcss%2Fhomepage.html%3Ffrom%3Dhz%26ref_%3Dnav_ya_signin&pageType=YourAccount&yshURL=https%3A%2F%2Fwww.amazon.com%2Fgp%2Fyourstore%2Fhome%3Fie%3DUTF8%26ref_%3Dnav_ya_signin']

    def parse(self, response):
        signin_form = response.xpath('//form[@name="signIn"]')
        hidden_field_names = signin_form.xpath('.//*[@type="hidden"]/@name').extract()
        hidden_field_values = signin_form.xpath('.//*[@type="hidden"]/@value').extract()

        hidden_agg = dict(zip(hidden_field_names, hidden_field_values))

        formdata = hidden_agg.update({
                "email": "gavinong10@gmail.com",
                "password": ""
                })
        return FormRequest.from_response(response, formdata=hidden_agg, callback=self.scrape_home)

    def scrape_home(self, response):
        yield Request("https://www.amazon.com", self.search_slickdeals_items)
        #yield Request("https://www.amazon.com/gp/site-directory/ref=nav_shopall_fullstore", self.nav_departments)

    def search_slickdeals_items(self, response):
        # Open database        
        CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
        SLICKDEALS_DB = os.path.join(CURRENT_DIR, '../../../../slickdeals_gmail/database/slickdeals.db')
        conn = sqlite3.connect(SLICKDEALS_DB)
        cursor = conn.execute('''select * from email_deals''')

        sd_titles = []
        for row in cursor:
            sd_titles.append(row[2])
        conn.close()

        for sd_title in sd_titles:
            sd_title = wrangle_title(sd_title)
            yield FormRequest.from_response(response, formname="site-search", formdata={"field-keywords": sd_title}, callback=self.retrieve_slickdeal_item_on_amazon)

    def retrieve_slickdeal_item_on_amazon(self, response):
        try:
            results = response.xpath('//*[@id="atfResults"]')[0]
        except:
            print("No data for item")
            return
        
        results.xpath('.//li')
        for result in results:
            title ".//h2/@data-attribute"
            average_review
            number_of_reviews
            price
            prime
            more_buying_choices

        return self.show(response)
        #atfResults

    def nav_departments(self, response):
        departments = response.xpath('//*[@class="fsdDeptTitle"]/text()').extract()
        # ['Amazon Video', 'Amazon Music', 'Appstore for Android', 'Prime Photos and Prints', 'Kindle E-readers & Books', 'Fire Tablets', 'Fire TV', 'Echo & Alexa', 'AmazonFresh', 'Books & Audible', 'Movies, Music & Games', 'Electronics & Computers', 'Home, Garden & Tools', 'Beauty, Health & Food', 'Toys, Kids & Baby', 'Clothing, Shoes & Jewelry', 'Handmade', 'Sports & Outdoors', 'Automotive & Industrial', 'Home Services', 'Credit & Payment Products']


        #printg(response.xpath('//*[@class="fsdDeptBox"]//a'))
        #fsdDeptTitle

    def show(self, response):
        open_in_browser(response)