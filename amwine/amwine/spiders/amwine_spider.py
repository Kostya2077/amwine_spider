import scrapy
import math
from datetime import datetime

from amwine.constants.re_constants import RE
from amwine.constants.tags_constants import PRODUCT



class  AmwineSpider(scrapy.Spider):
    name = 'amwine'
    start_urls = ['https://amwine.ru/']
    min_products_count = 200

    def start_requests(self):
        list_url_categories = input().split()
        for url_category in list_url_categories:
            yield scrapy.Request(url_category, callback=self.parse_category_pages, )

    def parse_category_pages(self, response, **kwargs):
        if self.__check_products_count(response.body):
            for page in range(1, self.__get_pages_count((response.body))+1):
                yield scrapy.Request(response.url + f'?page={page}', callback=self.parse_page)

    def parse_page(self, response, **kwargs):
        data = self.__get_products_data(response.body)
        for product_link in self.__get_products_links(data):
            product_link = str(product_link[0])[3:-1]
            yield scrapy.Request(self.start_urls[0]+product_link, callback=self.parse)

    def parse(self, response, **kwargs):
        yield {
            "timestamp": datetime.timestamp(datetime.now()),
            "RPC": response.xpath(PRODUCT.XPATH_RPC).get(),
            "url": response.url,
            "title": self.__normal_form(response.xpath(PRODUCT.XPATH_TITLE).get()),
            "marketing_tags": [response.xpath(PRODUCT.XPATH_MARKETING_TAGS).get()],
            "brand": self.__normal_form(response.xpath(PRODUCT.XPATH_BRAND).get()) or "",
            "section": self.__get_section(response.url),
            "price_data": self.__get_price_data(response),
            "stock": self.__get_stock(response),
            "assets": self.__get_assets(response),
            "metadata": self.__get_metadata(response),
            "variants": 1,
        }

    # Проверка минимального количества товара
    def __check_products_count(self, body):
        count = int(RE.PRODUCTS_TOTAL_COUNT.search(body)[0])
        return count >= self.min_products_count

    # количетсво страниц по категории
    def __get_pages_count(self, body):
        products_total_count = float(RE.PRODUCTS_TOTAL_COUNT.search(body)[0])
        count_per_page = float(RE.PRODUCTS_COUNT_PER_PAGE.search(body)[0])
        result = math.ceil(products_total_count/count_per_page)
        return int(result)

    def __get_products_links(self, data):
        return RE.LINK_PAGE.finditer(data)

    def __get_products_data(self, body):
        return RE.DATA_PAGE.search(body)[0]

    def __get_section(self, url):
        return url.split('/')[4:6]

    def __get_price_data(self, response):
        price = self.__float(response.xpath(PRODUCT.XPATH_PRICE).get())
        old_price = self.__float(response.xpath(PRODUCT.XPATH_OLD_PRICE).get())
        if price and old_price:
            sale_tag = f"Скидка {100.0-(price/old_price)*100}%"
        else:
            sale_tag = ""
        return {
            "current": price,
            "original": old_price,
            "sale_tag": sale_tag
        }

    def __get_stock(self, response):
        result = response.xpath(PRODUCT.XPATH_STOCK).get()
        return {
            "in_stock": not ("нет в наличии" in result.lower()),
            "count": 0
        }

    def __get_assets(self, response):
        img_url = response.xpath(PRODUCT.XPATH_IMG_URL).get() or ""
        if img_url:
            img_url = self.start_urls[0]+img_url[1:]
        return {
            "main_image": img_url,
            "set_images": [],
            "view360": [],
            "video": []
        }

    def __get_metadata(self, response):
        article = response.xpath(PRODUCT.XPATH_ARTICLE).get() or ""
        if article:
            article = RE.ARTICLE.search(str(article))[0]
        result = {
            "__description": response.xpath(PRODUCT.XPATH_DESCRIPTION_0).get() or response.xpath(PRODUCT.XPATH_DESCRIPTION_1).get() or "",
            "АРТИКУЛ": article,
        }

        # на странице информация о товаре подаётся как "ключ" -> "значение",
        # но т.к. они в одинаковых блоках, мы чередуем
        # сначала ключ, потом значение, начиная с ключа (attribute_flag = True),
        # записывая название ключа в attribute_name
        attribute_name = ""
        attribute_flag = True
        for tag in response.xpath(PRODUCT.XPATH_ATTRIBUTES_PRODUCT):
            tag = (tag.get())
            for data in RE.TAG_TEXT.finditer(tag):
                data = self.__normal_form(data[0])
                if data:
                    if attribute_flag:
                        attribute_name = data.upper()
                    else:
                        result[attribute_name] = data
                    attribute_flag = not(attribute_flag)
        return result

    # избавление от длинных пробелов и экранированного символа "\n"
    def __normal_form(self, data):
        if data:
            data = data.replace('\n', '').strip()
            for sp in sorted(RE.CLEAR_LONG_SPACES.findall(data))[::-1]:
                data = data.replace(sp, ' ')
        return data

    def __float(self, data):
        if data:
            return float(data.replace(' ', ''))
        return 0.0
