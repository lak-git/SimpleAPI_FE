from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


BASE_URL = "http://127.0.0.1:5500"
WAIT_TIME = 15


def test_PFE01(driver):
    """
    Test Case: Verify pins are fetched and displayed when the page loads\n
    Expected Result: Pins are displayed in a grid matching the DB entries
    """
    driver.get(BASE_URL)

    pins = WebDriverWait(driver, WAIT_TIME).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "pin-card"))
    )

    assert len(pins) == 2, "Expected 2 pins to be displayed on the page"


def test_PFE02(driver):
    """
    Test Case: Verify clicking a pin opens the modal with correct details\n
    Expected Result: Modal opens showing the pin's title and description
    """
    driver.get(BASE_URL)

    pin = WebDriverWait(driver, WAIT_TIME).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "pin-card"))
    )
    pin.click()
    modal_title = WebDriverWait(driver, WAIT_TIME).until(
        EC.visibility_of_element_located((By.ID, "modal-title"))
    ).text

    modal_description = driver.find_element(By.XPATH, '//*[@id="modal-body"]/p[2]').text

    assert modal_title == "My Ubuntu Hyprland Setup", "Modal title does not match expected value"
    assert (
        modal_description == "This is my Ubuntu 24.06 with JaKooLit Hyprland"
    ), "Modal description does not match expected value"


def test_PFE03(driver):
    """
    Test Case: Verify the modal can be closed using the close button\n
    Expected Result: Modal disappears from view when the close button is clicked
    """
    driver.get(BASE_URL)

    pin = WebDriverWait(driver, WAIT_TIME).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "pin-card"))
    )
    pin.click()

    close_button = WebDriverWait(driver, WAIT_TIME).until(
        EC.element_to_be_clickable((By.ID, "close-modal-btn"))
    )
    close_button.click()

    WebDriverWait(driver, WAIT_TIME).until(
        EC.invisibility_of_element_located((By.ID, "pin-modal"))
    )

    assert not driver.find_element(By.ID, "pin-modal").is_displayed(), "Modal should be closed but is still present"


def test_PFE04(driver):
    """
    Test Case: Verify clicking the dark background closes the modal\n
    Expected Result: Modal completely disappears from view when clicking outside the content box
    """
    driver.get(BASE_URL)

    pin = WebDriverWait(driver, WAIT_TIME).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "pin-card"))
    )
    pin.click()

    overlay = WebDriverWait(driver, WAIT_TIME).until(
        EC.element_to_be_clickable((By.ID, "pin-modal"))
    )
    driver.execute_script("arguments[0].click();", overlay)

    WebDriverWait(driver, WAIT_TIME).until(
        EC.invisibility_of_element_located((By.ID, "pin-modal"))
    )

    assert not driver.find_element(By.ID, "pin-modal").is_displayed(), "Modal should be hidden but is still visible"


def test_PFE05(driver):
    """
    Test Case: Verify searching filters the pins correctly using the button\n
    Expected Result: Only pins containing "Fedora" in the title are displayed after search
    """
    driver.get(BASE_URL)

    search_input = WebDriverWait(driver, WAIT_TIME).until(
        EC.presence_of_element_located((By.ID, "filter-input"))
    )
    search_input.send_keys("Fedora")

    search_button = driver.find_element(By.ID, "search-btn")
    search_button.click()

    filtered_pins = WebDriverWait(driver, WAIT_TIME).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "pin-card"))
    )

    assert len(filtered_pins) == 1, "Expected only 1 pin to be displayed after filtering"


def test_PFE06(driver):
    """
    Test Case: Verify pressing Enter inside the input triggers the search\n
    Expected Result: Only pins containing "Fedora" in the title are displayed after pressing Enter
    """
    driver.get(BASE_URL)

    search_input = WebDriverWait(driver, WAIT_TIME).until(
        EC.presence_of_element_located((By.ID, "filter-input"))
    )
    search_input.send_keys("Fedora")
    search_input.send_keys("\n")

    filtered_pins = WebDriverWait(driver, WAIT_TIME).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "pin-card"))
    )

    assert len(filtered_pins) == 1, "Expected only 1 pin to be displayed after filtering with Enter key"


def test_PFE07(driver):
    """
    Test Case: Verify the Clear button resets the search and shows all pins\n
    Expected Result: Search bar text empties and all original pins are fetched and displayed after clicking Clear
    """
    driver.get(BASE_URL)

    search_input = WebDriverWait(driver, WAIT_TIME).until(
        EC.presence_of_element_located((By.ID, "filter-input"))
    )
    search_input.send_keys("Fedora")

    search_button = driver.find_element(By.ID, "search-btn")
    search_button.click()

    clear_button = WebDriverWait(driver, WAIT_TIME).until(
        EC.element_to_be_clickable((By.ID, "clear-btn"))
    )
    clear_button.click()

    all_pins = WebDriverWait(driver, WAIT_TIME).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "pin-card"))
    )

    assert len(all_pins) == 2, "Expected all pins to be displayed after clearing the search filter"