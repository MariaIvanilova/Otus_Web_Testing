from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time


def wait_title(title, browser, timeout=3):
    try:
        WebDriverWait(browser, timeout).until(EC.title_is(title))
    except TimeoutException:
        raise AssertionError(f"Expected title is {title}, but title is {browser.title}")


def wait_element(browser, who, timeout=1, how=By.CSS_SELECTOR):
    try:
        return WebDriverWait(browser, timeout).until(
            EC.visibility_of_element_located((how, who))
        )
    except TimeoutException:
        browser.save_screenshot(f"{browser.session_id}.png")
        raise AssertionError(f"Didn't wait for: {who}")


def is_element_present(browser, how, what):
    try:
        browser.find_element(how, what)
    except NoSuchElementException:
        return False
    return True


def test_administration_login(browser, url):
    catalog_url = url + "administration"
    browser.get(url=catalog_url)

    wait_title("Administration", browser)

    browser.find_element(By.ID, "input-username").send_keys("user")
    browser.find_element(By.ID, "input-password").send_keys("bitnami")
    browser.find_element(By.CSS_SELECTOR, ".btn.btn-primary").click()

    wait_title("Dashboard", browser)

    assert is_element_present(browser, By.ID, "nav-logout")
    browser.find_element(By.ID, "nav-logout").click()


def test_add_item_to_cart(browser, url):
    browser.get(url)
    wait_title("Your Store", browser)

    item_name = browser.find_element(
        By.CSS_SELECTOR, ".content>div[class='description']>h4>a"
    ).text
    button_add = browser.find_element(By.CSS_SELECTOR, ".content>form>div>button")
    shopping_cart = browser.find_element(By.CSS_SELECTOR, "a[title='Shopping Cart']")

    browser.execute_script(
        "arguments[0].scrollIntoView(true);", button_add
    )  # scroll to "add to cart" button

    time.sleep(1)  # waiting scrolling  - это срабатывает
    # WebDriverWait(browser, 5).until(EC.element_to_be_clickable(button_add))  # это не срабатывает
    button_add.click()

    browser.execute_script("window.scrollTo(0, 0)")  # scroll to up
    time.sleep(5)  # sleep for scrolling and disappearing  alert window

    # WebDriverWait(browser, 10).until(EC.element_to_be_clickable(shopping_cart))   # это не работает

    shopping_cart.click()
    assert (
        item_name
        == browser.find_element(By.CSS_SELECTOR, ".text-start.text-wrap>a").text
    )


def test_main_changing_currency(browser, url):
    browser.get(url)
    wait_title("Your Store", browser)

    price_first = browser.find_element(By.CSS_SELECTOR, ".price-new").text
    currency = browser.find_element(
        By.CSS_SELECTOR, "form>.dropdown>a>.d-none.d-md-inline"
    )
    currency.click()
    browser.find_element(By.CSS_SELECTOR, "a[href='EUR']").click()
    price_second = browser.find_element(By.CSS_SELECTOR, ".price-new").text
    assert price_first != price_second, (
        f"price should be changed, initial price {price_first}, price after changing {price_second}"
    )


def test_catalog_desktops_changing_currency(browser, url):
    catalog_url = url + "catalog/desktops"
    browser.get(url=catalog_url)

    wait_title("Desktops", browser)

    price_first = browser.find_element(By.CSS_SELECTOR, ".price-new").text
    currency = browser.find_element(
        By.CSS_SELECTOR, "form>.dropdown>a>.d-none.d-md-inline"
    )
    currency.click()
    browser.find_element(By.CSS_SELECTOR, "a[href='EUR']").click()
    price_second = browser.find_element(By.CSS_SELECTOR, ".price-new").text
    assert price_first != price_second, (
        f"price should be changed, initial price {price_first}, price after changing {price_second}"
    )
