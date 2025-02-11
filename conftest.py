import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

default_url = "http://192.168.100.20:8081/"


def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome", help="browser for tests")
    parser.addoption("--url", default=default_url)


@pytest.fixture
def browser(request):
    browser_name = request.config.getoption("browser")
    driver = None
    if browser_name in ["chrome", "ch"]:
        driver = webdriver.Chrome()
    elif browser_name in ["firefox", "ff"]:
        driver = webdriver.Firefox()
    elif browser_name in ["yandex", "ya"]:
        service = Service(
            executable_path=os.path.expanduser("~/Otus/drivers/yandexdriver.exe")
        )
        options = webdriver.ChromeOptions()
        options.binary_location = os.path.expanduser(
            "~/AppData/Local/Yandex/YandexBrowser/Application/browser.exe"
        )
        driver = webdriver.Chrome(service=service, options=options)

    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def url(request):
    return request.config.getoption("--url")
