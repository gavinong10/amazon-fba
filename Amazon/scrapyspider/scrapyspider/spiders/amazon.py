# -*- coding: utf-8 -*-
import scrapy
from scrapy.utils.response import open_in_browser
from scrapy.http import FormRequest, Request

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
		yield Request("https://www.amazon.com/gp/site-directory/ref=nav_shopall_fullstore", self.nav_departments)

	def nav_departments(self, response):
		departments = response.xpath('//*[@class="fsdDeptTitle"]/text()').extract()
		# ['Amazon Video', 'Amazon Music', 'Appstore for Android', 'Prime Photos and Prints', 'Kindle E-readers & Books', 'Fire Tablets', 'Fire TV', 'Echo & Alexa', 'AmazonFresh', 'Books & Audible', 'Movies, Music & Games', 'Electronics & Computers', 'Home, Garden & Tools', 'Beauty, Health & Food', 'Toys, Kids & Baby', 'Clothing, Shoes & Jewelry', 'Handmade', 'Sports & Outdoors', 'Automotive & Industrial', 'Home Services', 'Credit & Payment Products']

		
		#printg(response.xpath('//*[@class="fsdDeptBox"]//a'))
		#fsdDeptTitle

	def show(self, response):
		open_in_browser(response)