import requests as rq
import re
import json
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time


class ProductParser:
    """ Class Parser of product pages from OZON.ru, WildBerries.ru, YandexMarket.ru """

    def _ozon_parse(self, url: str) -> dict:
        """ Parser for product page from OZON """
        res = {}
        # Name and Price are taken from the start url
        driver = webdriver.Chrome('../../chromedriver.exe')
        driver.get(url)
        try:
            elem = driver.find_element(by=By.XPATH, value='//h1[contains(@class, "ym5")]')
        except NoSuchElementException:
            elem = None
        res['prod_name'] = elem.text if elem else 'undefined'
        try:
            elem = driver.find_element(by=By.XPATH, value='//span[contains(@class, "m3x")]')
        except NoSuchElementException:
            elem = None
        res['price'] = float(re.sub('[^\d.]*', '', elem.text)) if elem else 'undefined'
        driver.quit()
        # features take from API JSON
        item_list = url.split('/')
        i = item_list.index('product')
        item = '/'.join(item_list[i:-1])
        url_details = f'https://www.ozon.by/api/composer-api.bx/page/json/v2?url=/{item}/?layout_container=' \
                      f'pdpPage2column&layout_page_index=2'
        # too complicated structure, pop only features
        resp = rq.get(url_details).json().pop('widgetStates')
        key = [k for k in resp.keys() if k.startswith('webCharacteristics')]
        res['features'] = json.loads(resp[key[0]])
        return res

    def _wb_parse(self, url: str) -> dict:
        """ Parser for product page from WildBerries """
        res = {}
        # Price is taken from the start url
        driver = webdriver.Chrome('../../chromedriver.exe')
        driver.get(url)
        try:
            elem = driver.find_element(by=By.XPATH, value='//span[contains(@class, "price-block__price")]')
        except NoSuchElementException:
            elem = None
        res['price'] = float(re.sub('[^\d.]*', '', elem.text)) if elem else 'undefined'
        driver.quit()
        # Features and Name are taken from JSON
        item = url.split('/')[-2]
        url_details = f'https://wbx-content-v2.wbstatic.net/ru/{item}.json'
        try:
            resp = rq.get(url_details)
            res.update(**resp.json())
        except json.JSONDecodeError as e:
            return e
        res['prod_name'] = res.pop('imt_name')
        return res

    def _ym_parse(self, url: str) -> dict:
        """ Parser for product page from Yandex.Market """
        res = {}
        driver = webdriver.Chrome('../../chromedriver.exe')
        driver.get(url)
        # captcha, may be more than once
        while True:
            try:
                elem = driver.find_element(by=By.CLASS_NAME, value='CheckboxCaptcha-Button')
            except NoSuchElementException:
                break
            if elem:
                elem.submit()
                time.sleep(15)  # wait for manual enter captcha
            else:
                break
        # Name of Product
        try:
            elem = driver.find_element(by=By.TAG_NAME, value='h1')
        except NoSuchElementException:
            elem = None
        res['prod_name'] = elem.text if elem else 'undefined'
        # Price
        try:
            elem = driver.find_element(by=By.XPATH, value='//span[@data-auto="mainPrice"]/span[1]')
        except NoSuchElementException:
            elem = None
        res['price'] = float(''.join(elem.text.split(' '))) if elem else 'undefined'
        # Features
        elem = driver.find_elements(by=By.CLASS_NAME, value='_2oLGf')
        if elem:
            for el in elem:
                k = el.find_element(by=By.CLASS_NAME, value='_2trXG')
                v = el.find_element(by=By.CLASS_NAME, value='_3M0mF')
                res[k.text] = v.text
        driver.quit()
        return res

    def _get_parser(self, domain: str):
        """ Select a parser for the url """
        if 'ozon' in domain:
            return self._ozon_parse
        elif 'wildberries.' in domain:
            return self._wb_parse
        elif 'yandex.' in domain:
            return self._ym_parse

    def parse(self, url: str) -> dict:
        """ Method gets URL with product and returns dict with params """
        parser = self._get_parser(url.split('/')[2])  # domain address
        product_info = parser(url)

        # dictionary with details of the product
        # for k, v in product_info.items():
        #     print(f'{k}: {v}')
        return product_info
