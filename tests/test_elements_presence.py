from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def is_element_present(browser, how, what):
    try:
        browser.find_element(how, what)
    except NoSuchElementException:
        return False
    return True


def wait_title(title, browser, timeout=3):
    try:
        WebDriverWait(browser, timeout).until(EC.title_is(title))
    except TimeoutException:
        raise AssertionError(f"Expected title is {title}, but title is {browser.title}")


def test_main_page_elements(browser, url):
    browser.get(url=url)
    wait_title("Your Store", browser)
    assert is_element_present(browser, By.ID, "logo"), (
        "logo element should be on main page"
    )
    assert is_element_present(browser, By.ID, "menu"), "menu should be on main page"
    assert is_element_present(browser, By.CSS_SELECTOR, "#carousel-banner-0.slide"), (
        "carousel (upper) should be on main page"
    )
    assert is_element_present(browser, By.CSS_SELECTOR, "#carousel-banner-1.slide"), (
        "carousel (lower) should be on main page"
    )
    assert is_element_present(browser, By.CSS_SELECTOR, ".product-thumb"), (
        "product should be on main page"
    )


def test_catalog_desktops_elements(browser, url):
    catalog_url = url + "catalog/desktops"
    browser.get(url=catalog_url)

    wait_title("Desktops", browser)

    active_menu_item = browser.find_element(By.CSS_SELECTOR, ".list-group-item.active")
    assert "Desktops" in active_menu_item.text, "Desktops menu item should be active"

    assert is_element_present(browser, By.ID, "compare-total"), (
        "compare bar should be on main page"
    )
    assert is_element_present(browser, By.CSS_SELECTOR, ".product-thumb"), (
        "product should be on main page"
    )
    assert is_element_present(browser, By.CSS_SELECTOR, ".col-sm-6.text-start"), (
        "'Showing...' element should be on main page"
    )

    assert is_element_present(browser, By.CSS_SELECTOR, ".col-sm-6.text-end"), (
        "'Pages' element should be on main page"
    )
    assert is_element_present(browser, By.ID, "input-sort"), "Sorting"

    assert is_element_present(browser, By.ID, "input-limit"), "Limits for page"


def test_product_elements(browser, url):
    catalog_url = url + "product/tablet/samsung-galaxy-tab-10-1"
    browser.get(url=catalog_url)

    wait_title("Samsung Galaxy Tab 10.1", browser)

    assert is_element_present(browser, By.CSS_SELECTOR, ".image.magnific-popup"), (
        "'Photos...' element should be on main page"
    )
    assert is_element_present(
        browser, By.CSS_SELECTOR, "button[title='Add to Wish List']"
    ), "Presence of 'Add to Wish List'"
    assert is_element_present(
        browser, By.CSS_SELECTOR, "button[title='Compare this Product']"
    ), "Presence of 'Compare this Product'"
    assert is_element_present(browser, By.ID, "button-cart"), "Add to cart button"
    assert is_element_present(browser, By.ID, "input-quantity"), "Quantity"


def test_administration_elements(browser, url):
    catalog_url = url + "administration"
    browser.get(url=catalog_url)

    wait_title("Administration", browser)

    assert is_element_present(browser, By.ID, "input-username"), "User name input field"
    assert is_element_present(browser, By.ID, "input-password"), "Password input field"
    assert is_element_present(browser, By.CSS_SELECTOR, ".btn.btn-primary"), (
        "Login button"
    )
    assert is_element_present(
        browser, By.CSS_SELECTOR, 'a[href="https://www.opencart.com"]'
    ), "Link to OpenCard site"
    assert is_element_present(browser, By.CSS_SELECTOR, ".card-header"), (
        "Header of login page"
    )


def test_registration_elements(browser, url):
    catalog_url = url + "/index.php?route=account/register"
    browser.get(url=catalog_url)

    wait_title("Register Account", browser)

    assert is_element_present(browser, By.ID, "input-firstname"), (
        "first name input field"
    )
    assert is_element_present(browser, By.ID, "input-lastname"), "last name input field"
    assert is_element_present(browser, By.ID, "input-email"), "email input field"

    assert is_element_present(browser, By.ID, "input-password"), "password input field"
    assert is_element_present(browser, By.CSS_SELECTOR, ".btn.btn-primary"), (
        "Submit button"
    )
