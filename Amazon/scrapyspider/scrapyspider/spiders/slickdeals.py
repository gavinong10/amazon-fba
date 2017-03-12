# -*- coding: utf-8 -*-
import scrapy
from scrapy.utils.response import open_in_browser
from scrapy.http import FormRequest, Request

def printg(*args):
	print('\n\n\n\n')
	print(*args)
	print('\n\n\n\n')

class SlickDealsSpider(scrapy.Spider):
	name = "slickdeals"
	allowed_domains = ["slickdeals.net"]
	start_urls = ['https://slickdeals.net/forums/login.php']

	def parse(self, response):
		signin_form = response.xpath('//form[@id="loginform"]')
		hidden_field_names = signin_form.xpath('.//*[@type="hidden"]/@name').extract()
		hidden_field_values = signin_form.xpath('.//*[@type="hidden"]/@value').extract()

		hidden_agg = dict(zip(hidden_field_names, hidden_field_values))

		formdata = hidden_agg.update({
				"vb_login_username": "teamgavtay@gmail.com",
				"vb_login_password": "teamgavtay123!",
				"vb_login_md5password":"94e93ce2c4baa1ca48972acbfe662504",
				"vb_login_md5password_utf":"94e93ce2c4baa1ca48972acbfe662504"
				})
		printg(hidden_agg)
		return FormRequest.from_response(response, formdata=hidden_agg, callback=self.show)

	def scrape_home(self, response):
		yield Request("https://www.amazon.com/gp/site-directory/ref=nav_shopall_fullstore", self.show)

	def show(self, response):
		open_in_browser(response)

'''
<div class="subPaneInfo">
                    <strong class="title">Browse Categories</strong>
                    <ul>
                      <li><a href="/deals/games/" data-link="nav:Games">Video Games</a></li>
                      <li><a href="/deals/tv/" data-link="nav:HDTV">TV</a></li>
                      <li><a href="/deals/computers/" data-link="nav:Computers">Computers</a></li>
                      <li><a href="/deals/money/" data-link="nav:Finance">Finance</a></li>
                      <li><a href="/deals/home/" data-link="nav:Home">Home</a></li>
                      <li><a href="/deals/apparel/" data-link="nav:Apparel">Apparel</a></li>
                      <li><a href="/deals/tech/" data-link="nav:Electronics">Tech</a></li>
                    </ul>
                    <ul>
                      <li><a href="/deals/photo/" data-link="nav:Photo">Cameras</a></li>
                      <li><a href="/deals/auto/" data-link="nav:Automotive">Autos</a></li>
                      <li><a href="/deals/beauty/" data-link="nav:Health &amp; Beauty">Health &amp; Beauty</a></li>
                      <li><a href="/deals/children/" data-link="nav:Children">Children</a></li>
                      <li><a href="/deals/entertainment/" data-link="nav:Entertainment">Entertainment</a></li>
                      <li><a href="/deals/travel/" data-link="nav:Travel">Travel</a></li>
                      <li><a href="/deals/pets/" data-link="nav:Pets">Pets</a></li>
                    </ul>
                    <ul>
                      <li><a href="/deals/phone/" data-link="nav:Phones">Phones</a></li>
                      <li><a href="/deals/grocery/" data-link="nav:Groceries">Grocery</a></li>
                      <li><a href="/deals/sport/" data-link="nav:Sporting Goods">Sporting Goods</a></li>
                      <li><a href="/deals/books-magazines/" data-link="nav:Books &amp; Magazines">Books &amp; Magazines</a></li>
                      <li><a href="/deals/bags/" data-link="nav:Bags &amp; Luggage">Bags &amp; Luggage</a></li>
                      <li><a href="/deals/office/" data-link="nav:Office &amp; School Supplies">Office &amp; School Supplies</a></li>
                      <li><a href="/deals/ps4-games/" data-link="nav:PS4">PS4</a></li>
                    </ul>
                    <ul>
                      <li><a href="/deals/xbox-one-games/" data-link="nav:Xbox One">Xbox One</a></li>
                      <li><a href="/deals/ssd/" data-link="nav:SSD">SSD</a></li>
                      <li><a href="/deals/tools/" data-link="nav:Tools">Tools</a></li>
                      <li><a href="/deals/credit-card/" data-link="nav:Credit Cards">Credit Cards</a></li>
                      <li><a href="/deals/cellphone/" data-link="nav:Cellphones">Cellphones</a></li>
                      <li><a href="/deals/laptop/" data-link="nav:Laptops">Laptops</a></li>
                      <li><a href="/deal-categories/" data-link="nav:View All Categories" class="viewAllLink">View All Categories</a></li>
                    </ul>
                  </div>
                  '''