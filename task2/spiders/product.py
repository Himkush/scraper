# -*- coding: utf-8 -*-
import scrapy


class ProductSpider(scrapy.Spider):
    name = 'product'
    allowed_domains = ['www.cartridgesave.co.uk']
    start_urls = [ 
      # 'https://www.cartridgesave.co.uk/toner-cartridges/IBM.html',
     "https://www.cartridgesave.co.uk/toner-cartridges/Brother.html",
    "https://www.cartridgesave.co.uk/toner-cartridges/Canon.html",
    "https://www.cartridgesave.co.uk/toner-cartridges/Dell.html",
    "https://www.cartridgesave.co.uk/toner-cartridges/Epson.html",
    "https://www.cartridgesave.co.uk/toner-cartridges/HP.html",
    "https://www.cartridgesave.co.uk/toner-cartridges/Konica-Minolta.html",
    "https://www.cartridgesave.co.uk/toner-cartridges/Kyocera.html",
    "https://www.cartridgesave.co.uk/toner-cartridges/Lexmark.html",
    "https://www.cartridgesave.co.uk/toner-cartridges/Oki.html",
    "https://www.cartridgesave.co.uk/toner-cartridges/Ricoh.html",
    "https://www.cartridgesave.co.uk/toner-cartridges/Samsung.html",
    "https://www.cartridgesave.co.uk/toner-cartridges/Xerox.html",
    "https://www.cartridgesave.co.uk/toner-cartridges/Apple.html",
    "https://www.cartridgesave.co.uk/toner-cartridges/IBM.html",
    "https://www.cartridgesave.co.uk/toner-cartridges/Muratec.html",
    "https://www.cartridgesave.co.uk/toner-cartridges/Olivetti.html",
    "https://www.cartridgesave.co.uk/toner-cartridges/Panasonic.html",
    "https://www.cartridgesave.co.uk/toner-cartridges/Philips.html",
    "https://www.cartridgesave.co.uk/toner-cartridges/Sagem.html",
    "https://www.cartridgesave.co.uk/toner-cartridges/Sharp.html",
    "https://www.cartridgesave.co.uk/toner-cartridges/TallyGenicom.html",
    "https://www.cartridgesave.co.uk/toner-cartridges/Toshiba.html",
    ]

    def parse(self, response):
    	titles = response.xpath('//h2[@class="inks"]/text()').extract()
    	for title in titles:
    		urls = response.xpath('//h2[@class="inks" and contains(text(),"{}")]/following-sibling::ul/li/a/@href'.format(title)).extract()
    		for url in urls: 
    			yield scrapy.Request(url, callback=self.parse_toner, meta = {'title': title})

    def parse_toner(self, response):
    	product_urls = response.xpath('//div[@class="product-item-inner"]/strong[@class="product name product-item-name"]/a[@class="product-item-link"]/@href').extract()
    	header_title = response.xpath('//div[@class="category-header-title"]/h1/text()').extract_first()
    	# p_title = response.xpath('//div[@class="product-item-inner"]/strong[@class="product name product-item-name"]/a[@class="product-item-link"]/text()').extract_first()
    	for p_url in product_urls:

    		yield scrapy.Request(p_url, callback=self.parse_product, dont_filter=True, meta = {'title': header_title})

    def parse_product(self, response):
    	title = response.meta.get('title')
    	p_name = response.xpath('//div[@class="page-title-wrapper product"]/h1[@class="page-title"]/span/text()').extract_first()
    	meta_title = response.xpath('//title/text()').extract_first()
    	meta_desc = response.xpath('//meta[@name="description"]/@content').extract_first()
    	meta_keywords = response.xpath('//meta[@name="keywords"]/@content').extract_first()
    	price_exc =  response.xpath('//div[@class="product-info-price"]//span[@class="price-wrapper price-excluding-tax"]/@data-price-amount').extract_first()
    	price_inc = response.xpath('//div[@class="product-info-price"]//span[@class="price-wrapper price-including-tax"]/@data-price-amount').extract_first()
    	manu = response.xpath('//div[@class="product-data-container"]//table//td[@data-th="Manufacturer Part No."]/text()').extract_first()
    	duty = response.xpath('//div[@class="product-data-container"]//table//td[@data-th="Duty Cycle"]/text()').extract_first()
    	brand =  response.xpath('//div[@class="product-data-container"]//table//td[@data-th="Brand"]/text()').extract_first()
    	colour = response.xpath('//div[@class="product-data-container"]//table//td[@data-th="Colour"]/text()').extract_first()
    	p_type =  response.xpath('//div[@class="product-data-container"]//table//td[@data-th="Product Type"]/text()').extract()
    	similar_products =  response.xpath('//div[@class="compatible_printers"]/ul/li/a/text()').extract()
    	similar_products_str = ''
    	product_description = response.xpath('//div[@id="information"]/div[@class="info-section product-description"]/div[@itemprop="description"]//text()').extract()
    	# product_para =  response.xpath('//div[@id="information"]/div[@class="info-section product-description"]/div[@itemprop="description"]/p/text()').extract()
    	# product_heading3 =  response.xpath('//div[@id="information"]/div[@class="info-section product-description"]/div[@itemprop="description"]/h3/text()').extract_first()
    	# product_description = ''
    	product_description = ''.join(product_description)
   
    	all_list = response.xpath('//div[@class="quick-info-container"]//ul[@class="ci-list"]/li//text()').extract()
    	contains =''
    	replaces = ''
    	pack_of = ''
    	for a1 in all_list:
    		temp3 = a1.strip()
    		if temp3.startswith('Contains'):
    			contains = temp3
    		elif temp3.startswith('Replaces'):
    			replaces = temp3
    		elif temp3.startswith('Pack of'):
    			pack_of = temp3
    		else:
    			pass
    	if price_inc==None:
    		price_inc = ''
    	else:
    		price_inc = price_inc[1:]

    	for i in similar_products:
    		similar_products_str = similar_products_str + i + " "
    	# response.xpath('//div[@class="quick-info-container"]//ul[@class="ci-list"]/li/text()').extract()
    	yield {
    	'Category': title.replace('Toner Cartridges',''),
    	'Product Name': p_name,
    	'Price inc vat': price_inc, 
    	'Price exc vat': price_exc,
    	'Contains': contains,
    	'Replaces': replaces,
    	'Pack of': pack_of,
    	'Manufacturer Part No.:': manu,
    	'Duty Cycle:': duty,
    	'Brand:': brand,
    	'Colour:': colour,
    	'Product Type': p_type[0],
    	'Product Type 2': p_type[1],
    	'To see a full list of products that work in your printer, click on the model name below:':similar_products_str,
    	'Product Description': product_description,
    	'Meta keywords': meta_keywords,
    	'Meta Title': meta_title,
    	'Meta Description': meta_desc,
    	'url': response.url
    	}