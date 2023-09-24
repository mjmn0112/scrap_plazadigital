import scrapy

class plazaspider(scrapy.Spider):
    name = 'plaza'
    start_urls = ['https://plazadigital.ir/product-category/laptop/']

    def parse(self, response):

        for products in response.xpath('//article[contains(@class, "product")]'):
            yield {
                'title': products.xpath('.//h2[contains(@class, "product-title")]/text()').get(),
                'price': products.xpath('.//bdi[contains(@class, "woocommerce-Price-amount")]/text()').get(),
                'link': products.xpath('.//a[@rel="bookmark"]/@href').get(),
                'pic_url': products.xpath('.//a[@rel="bookmark"]/img/@data-lazy-src').get(),
            }
            for product_link in products.xpath('.//a[@rel="bookmark"]/@href').getall():
                yield response.follow(product_link, callback=self.parse_product)
            
    def parse_product(self, response):
        # Extract the desired data from the product page
        data = {
        'title': response.xpath('//h1/text()').get(),
        'garanti': response.xpath('//label[contains(text(), "گارانتی")]/following-sibling::select/option[@selected="selected"]/text()').get(),
        'images' : response.xpath('//img/@src').extract_first(),
        'tabaghe bandi' : response.xpath('//li[contains(@class, "woocommerce-product-attributes-item--attribute_pa_tabaghe-bandi")]//div[@class="woocommerce-product-attributes-item__value"]/p/a/text()').getall(),
        
        }
        yield data
        

        
        
    #for going next page we can use the following code :
    #nextpage = response.xpath('.//a[@class="next page-numbers"]/@href').get()
    #if nextpage is not None:
    #    yield response.follow(nextpage, callback=self.parse)

