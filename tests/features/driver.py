from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service



def get_driver(headless:bool = False) -> webdriver.Chrome:
    """
    Return a webdriver instance.
    """
    options = Options()
    service = Service(executable_path="/usr/bin/chromedriver")
    options.binary_location = r"/usr/bin/chromium-browser"

    if headless: options.add_argument("--headless=new")

    options.add_experimental_option("detach", True)
    return webdriver.Chrome(service=service, options=options)