import time
import unittest
from unittest import TestCase

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select


def get_price(item: WebElement, browser):
    price = None
    dp_id = item.get_attribute("data-product-id")
    try:
        cur_price = item.find_element(By.ID, f"product-price-{dp_id}")
        price = float(cur_price.text[1:])
    except NoSuchElementException:
        from_price = browser.find_element(By.XPATH, f"//*[@id=\"from-{dp_id}\"]")
        price = float(from_price.text[1:])
    return price


def check_pair_order(ascending: bool, prev, next) -> bool:
    if prev < 0:
        return True
    if ascending:
        return prev <= next
    else:
        return prev >= next


def ensure_order(browser, ascending: bool):
    def get_element(ascending: bool):
        return browser.find_element(By.XPATH, f"//a[@class=\"{get_class_name(ascending)}\"]")

    def get_class_name(ascending: bool):
        return "action sorter-action sort-asc" if ascending else "action sorter-action sort-desc"

    def reverse_order():
        get_element(not ascending).click()
        time.sleep(3)

    web_elem = None
    try:
        web_elem = get_element(ascending)
    except NoSuchElementException:
        reverse_order()
        web_elem = get_element(ascending)
    return web_elem


def check_product_list_order(ordering: bool, browser):
    ensure_order(browser=browser, ascending=ordering)  # incapsulate
    product_list = browser.find_element(By.XPATH, "//div[@class='products wrapper grid products-grid']")
    items = product_list.find_elements(By.TAG_NAME, "li")
    #  check is the arrow right
    prev_price = -1  # price cannot be negative
    for item in items:
        price = get_price(item, browser)
        assert check_pair_order(ascending=ordering, prev=prev_price,
                                next=price), "Product list is not sorted properly"  # incapsulate
        prev_price = price
    return True


def scroll_into_view(browser, loc: WebElement):
    browser.execute_script("arguments[0].scrollIntoView();", loc)
    time.sleep(2)


class TestClass(TestCase):
    browser = None
    OPTIONS_LIST = ["Position", "Product Name", "Price", "New Arrivals"]

    def setUp(self):
        url = 'https://highlifeshop.com/speedbird-cafe'
        browser = webdriver.Firefox()
        browser.get(url)
        time.sleep(2)
        cookie_cls_btn = browser.find_element(By.XPATH,
                                              "//form[@id='amgdprcookie-form']//button[@title='ACCEPT COOKIES']")
        cookie_cls_btn.click()
        time.sleep(2)
        self.browser = browser

    # 1. Given I am in the product list for the first time the page is sorted by position
    def test_check_first_position(self):
        sorter_btn = self.browser.find_element(By.ID, "sorter")
        scroll_into_view(self.browser, sorter_btn)
        sorter_list = Select(sorter_btn)
        first_o = sorter_list.first_selected_option.text
        assert first_o == 'Position'

    # 2. Given I am in the product list when I click with my mouse the “sort by” dropdown control I can see there are
    # 4 options: Position, product name, price and new arrivals.
    def test_verify_drop_down_options(self):
        sorter = self.browser.find_element(By.XPATH, "//*[@id=\"sorter\"]")
        sorter.click()
        sorter_list = Select(sorter)
        option_list = [i.text for i in sorter_list.options]
        for o in option_list:
            assert o in self.OPTIONS_LIST

    # 3. Given I am in the product list and I click on the arrow up ↑ icon the list is sorted in descending order,
    # otherwise in ascending order.
    def test_verify_sorting_order(self):
        sorter_list = self.browser.find_element(By.XPATH, "//*[@id=\"sorter\"]")
        options = sorter_list.find_elements(By.TAG_NAME, "option")
        options[2].click()
        time.sleep(3)
        assert check_product_list_order(browser=self.browser, ordering=True)
        assert check_product_list_order(browser=self.browser, ordering=False)

    def tearDown(self):
        self.browser.close()


if __name__ == "__main__":
    unittest.main()
