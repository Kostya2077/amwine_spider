

class PRODUCT:
    XPATH_RPC = "//div[@class='catalog-element-info js-catalog-item js-catalog-item-detail']/@data-id"
    XPATH_TITLE = "//div[@class='catalog-element-info__title']/h1/text()"
    XPATH_MARKETING_TAGS = "//div[@class='catalog-element-info__price catalog-element-info__price_detail ']/span/span/span/text()"
    XPATH_PRICE = "//span[contains(text(),'₽')]/../text()"
    XPATH_OLD_PRICE = "//span[@class='old_price_span']/text()"
    XPATH_STOCK = "//div[@class='catalog-element-info__shops-right']/a/text()"
    XPATH_IMG_URL = "//div[@class='catalog-element-info__picture']/img/@src"
    XPATH_DESCRIPTION_0 = "//div[contains(text(), ('Описание'))]/../p/text()"
    XPATH_DESCRIPTION_1 = "//div[contains(text(), ('О напитке'))]/../p/text()"
    XPATH_ARTICLE = "//span[contains(text(), 'Артикул')]/text()"
    XPATH_ATTRIBUTES_PRODUCT = "//div[@class='about-wine__param']/span"
    XPATH_BRAND = "//span[contains(text(), 'Бренд')]/../span[2]/a/text()"



