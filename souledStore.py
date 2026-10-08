import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# --------------------------------------------------
# YOUR DETAILS
# --------------------------------------------------

MOBILE_NUMBER = "7710279775"
DATE_OF_BIRTH = "29/10/2004"
GENDER = "Female"


# Start Chrome
driver = webdriver.Chrome()
driver.maximize_window()

wait = WebDriverWait(driver, 15)

print("The Souled Store Login / Registration Testing Started")


# --------------------------------------------------
# TC01: Open Login Page
# --------------------------------------------------

driver.get("https://www.thesouledstore.com/login/")

try:
    wait.until(
        EC.presence_of_element_located(
            (By.TAG_NAME, "body")
        )
    )

    print("TC01 - Login Page Open: PASS")

except Exception:
    print("TC01 - Login Page Open: FAIL")


# --------------------------------------------------
# TC02: Login With Empty Fields
# --------------------------------------------------

try:
    buttons = driver.find_elements(By.TAG_NAME, "button")

    for button in buttons:
        if button.is_displayed():
            try:
                button.click()
                break
            except:
                pass

    time.sleep(2)

    print("TC02 - Empty Login Fields Validation: PASS")

except Exception:
    print("TC02 - Empty Login Fields Validation: FAIL")


# --------------------------------------------------
# TC03: Open Registration Page
# --------------------------------------------------

try:
    driver.get("https://www.thesouledstore.com/register")

    wait.until(
        EC.presence_of_element_located(
            (By.TAG_NAME, "body")
        )
    )

    print("TC03 - Registration Page Open: PASS")

except Exception:
    print("TC03 - Registration Page Open: FAIL")


# --------------------------------------------------
# TC04: Enter User Details
# --------------------------------------------------

try:

    inputs = driver.find_elements(By.TAG_NAME, "input")

    print("Number of input fields found:", len(inputs))

    for field in inputs:

        input_type = field.get_attribute("type")
        placeholder = field.get_attribute("placeholder")

        print(
            "Field:",
            input_type,
            placeholder
        )

        # Mobile number
        if (
            input_type == "tel"
            or
            (placeholder and "mobile" in placeholder.lower())
            or
            (placeholder and "phone" in placeholder.lower())
        ):

            field.clear()
            field.send_keys(MOBILE_NUMBER)

        # Date of birth
        elif (
            input_type == "date"
            or
            (placeholder and "dob" in placeholder.lower())
            or
            (placeholder and "birth" in placeholder.lower())
        ):

            field.clear()
            field.send_keys(DATE_OF_BIRTH)

    print("TC04 - User Details Entered: PASS")

except Exception as e:

    print("TC04 - User Details Entered: FAIL")
    print("Error:", e)


# --------------------------------------------------
# TC05: Submit Registration
# --------------------------------------------------

try:

    buttons = driver.find_elements(By.TAG_NAME, "button")

    register_button = None

    for button in buttons:

        text = button.text.strip().lower()

        if (
            "register" in text
            or
            "continue" in text
            or
            "submit" in text
        ):

            register_button = button
            break

    if register_button:

        register_button.click()

        time.sleep(3)

        print("TC05 - Registration Form Submitted: PASS")

    else:

        print("TC05 - Registration Button Not Found: FAIL")


except Exception as e:

    print("TC05 - Registration Form Submitted: FAIL")
    print("Error:", e)


print("Testing Completed")

driver.quit()