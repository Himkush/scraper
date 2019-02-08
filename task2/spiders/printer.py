# -*- coding: utf-8 -*-
import scrapy
import lxml


class PrinterSpider(scrapy.Spider):
    name = 'printer'
    allowed_domains = ['www.cartridgesave.co.uk']
    start_urls = [   "https://www.cartridgesave.co.uk/toner-cartridges/Sharp.html"
     # "https://www.cartridgesave.co.uk/toner-cartridges/Brother.html",
    # "https://www.cartridgesave.co.uk/toner-cartridges/Canon.html",
    # "https://www.cartridgesave.co.uk/toner-cartridges/Dell.html",
    # "https://www.cartridgesave.co.uk/toner-cartridges/Epson.html",
    # "https://www.cartridgesave.co.uk/toner-cartridges/HP.html",
    # "https://www.cartridgesave.co.uk/toner-cartridges/Konica-Minolta.html",
    # "https://www.cartridgesave.co.uk/toner-cartridges/Kyocera.html",
    # "https://www.cartridgesave.co.uk/toner-cartridges/Lexmark.html",
    # "https://www.cartridgesave.co.uk/toner-cartridges/Oki.html",
    # "https://www.cartridgesave.co.uk/toner-cartridges/Ricoh.html",
    # "https://www.cartridgesave.co.uk/toner-cartridges/Samsung.html",
    # "https://www.cartridgesave.co.uk/toner-cartridges/Xerox.html",
    # "https://www.cartridgesave.co.uk/toner-cartridges/Apple.html",
    # "https://www.cartridgesave.co.uk/toner-cartridges/IBM.html",
    # "https://www.cartridgesave.co.uk/toner-cartridges/Muratec.html",
    # "https://www.cartridgesave.co.uk/toner-cartridges/Olivetti.html",
    # "https://www.cartridgesave.co.uk/toner-cartridges/Panasonic.html",
    # "https://www.cartridgesave.co.uk/toner-cartridges/Philips.html",
    # "https://www.cartridgesave.co.uk/toner-cartridges/Sagem.html",
    # "https://www.cartridgesave.co.uk/toner-cartridges/Sharp.html",
    # "https://www.cartridgesave.co.uk/toner-cartridges/TallyGenicom.html",
    # "https://www.cartridgesave.co.uk/toner-cartridges/Toshiba.html"
    ]

    def parse(self, response):
    	titles = response.xpath('//h2[@class="inks"]/text()').extract()
    	for title in titles:
    		urls = response.xpath('//h2[@class="inks" and contains(text(),"{}")]/following-sibling::ul/li/a/@href'.format(title)).extract()
    		print(len(urls))
    		for url in urls:
    			yield scrapy.Request(url, callback=self.parse_toner, meta = {'title': title, 'url': response.url})

    def parse_toner(self, response):
    	desc = response.xpath('//p[@class="guaranteed"]/text()').extract()
    	temp = response.xpath('//p[@class="guaranteed"]/strong/text()').extract_first()
    	description = desc[0]+temp+desc[1]
    	header_title = response.xpath('//div[@class="category-header-title"]/h1/text()').extract_first()
    	p_title = response.xpath('//title/text()').extract_first()
    	meta_description = response.xpath('//meta[@name="description"]').extract_first()
    	meta_keywords = response.xpath('//meta[@name="keywords"]').extract_first()
    	meta_title = response.xpath('//title').extract_first()
    	# bottom_temp = response.xpath('//div[@class="details article"]').extract_first()
    	bottom_temp = response.xpath('//div[@class="details article"]/h3/following-sibling::p/text()').extract()
    	review = response.xpath('//div[@id="review"]/h3/span/text()').extract_first()
    	verdict =  response.xpath('//div[@class="verdict"]/span/strong/text()').extract_first()
    	article = response.xpath('//div[@class="summary article"]/p/text()').extract_first()
    	image =  response.xpath('//div[@class="category-header-image hide_on_mobile"]/a/img/@src').extract_first()
    	title = response.meta.get('title')
    	c_name = response.url[:-5]
    	t1 = 'https://www.cartridgesave.co.uk/toner-cartridges/'
    	temp_url = response.meta.get('url')
    	print(temp_url)
    	c_name = c_name.replace(temp_url[:-5],'')
    	manu = temp_url.replace(t1,'')[:-5]
    	try:
    		bottom_data_description= review+'\n'+verdict+'\n'+article+'\n'+'Design'+'\n'+bottom_temp[0]+'\n'+ 'Advantages'+'\n'+bottom_temp[1]+'\n'+'Disadvantage'+'\n'+bottom_temp[2]
    	except:
    		bottom_data_description = ''
    	p_title = p_title.split(',')
    	result = {
    	'Manafacturer': manu,
    	'Printer Category': title.replace('Toner Cartridges',''),
    	'Category Name': c_name[1:],
    	'Category Title': p_title[0],
    	'Page Title': header_title,
    	'Toner Top Description': description,
    	'Toner Bottom Description': bottom_data_description,
    	'Category meta': meta_description,
    	'Meta Title': meta_title,
    	'Meta keywords': meta_keywords,
        'Image url': image
    	}

    	yield result
