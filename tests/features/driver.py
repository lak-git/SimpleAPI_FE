from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_driver(headless:bool = False) -> webdriver.Chrome:
    """
    Return a webdriver instance.
    """
    options = Options()
    options.binary_location = r"/usr/bin/brave-browser"
    if headless: options.add_argument("--headless=new")
    options.add_experimental_option("detach", True)
    return webdriver.Chrome(options=options)