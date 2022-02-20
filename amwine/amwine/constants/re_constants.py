import re


class RE:
    DATA_PAGE = re.compile(b'(?<=window[.]products = )(?:.(?!}];))+')
    PRODUCTS_TOTAL_COUNT = re.compile(b'(?<=window[.]productsTotalCount = )\d+')
    PRODUCTS_COUNT_PER_PAGE = re.compile(b'(?<=window[.]productsPerServerPage = )\d+')
    LINK_PAGE = re.compile(b'(?<=\'link\':\')[^\']+')
    ARTICLE = re.compile('(?<=: ).+')

    # example "<span> Hello world!!! </span>" -> result = " Hello world!!!"
    TAG_TEXT = re.compile('(?<=>)(?:(?:.|\n)(?!<))+')

    CLEAR_LONG_SPACES = re.compile('[ ]{2,}')

