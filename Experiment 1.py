from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Launch Chrome
driver = webdriver.Chrome()
driver.maximize_window()

wait = WebDriverWait(driver, 20)

# Open OrangeHRM
driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")

# =====================================================
# Test Case 1 : Login
# =====================================================
print("===== TEST CASE 1 : LOGIN =====")

try:
    username = wait.until(
        EC.visibility_of_element_located((By.NAME, "username"))
    )
    username.send_keys("Admin")

    password = driver.find_element(By.NAME, "password")
    password.send_keys("admin123")

    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    wait.until(EC.visibility_of_element_located((By.XPATH, "//h6[text()='Dashboard']")))

    print("Login Successful")

except Exception as e:
    print("Login Failed")
    print(e)

time.sleep(2)

# =====================================================
# Test Case 2 : Search
# =====================================================
print("\n===== TEST CASE 2 : SEARCH =====")

try:
    search = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//input[@placeholder='Search']")
        )
    )

    search.send_keys("Admin")
    time.sleep(2)

    search.send_keys(Keys.ENTER)
    time.sleep(2)

    print("Search Test Passed")

except Exception as e:
    print("Search Test Failed")
    print(e)

# Clear Search
try:
    search.clear()
except:
    pass

time.sleep(2)

# =====================================================
# Test Case 3 : Admin Module
# =====================================================
print("\n===== TEST CASE 3 : ADMIN =====")

try:
    admin = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//span[text()='Admin']")
        )
    )

    admin.click()

    wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//h6[text()='User Management']")
        )
    )

    print("Admin Page Opened Successfully")

except Exception as e:
    print("Admin Test Failed")
    print(e)

time.sleep(2)

# =====================================================
# Test Case 4 : Dashboard
# =====================================================
print("\n===== TEST CASE 4 : DASHBOARD =====")

try:
    dashboard = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//span[text()='Dashboard']")
        )
    )

    dashboard.click()

    wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//h6[text()='Dashboard']")
        )
    )

    print("Dashboard Opened Successfully")

except Exception as e:
    print("Dashboard Test Failed")
    print(e)

time.sleep(2)

# =====================================================
# Test Case 5 : Profile
# =====================================================
print("\n===== TEST CASE 5 : PROFILE =====")

try:
    profile = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//span[@class='oxd-userdropdown-tab']")
        )
    )

    profile.click()

    time.sleep(2)

    print("Profile Menu Opened Successfully")

except Exception as e:
    print("Profile Test Failed")
    print(e)

time.sleep(2)

# =====================================================
# Test Case 6 : Logout
# =====================================================
print("\n===== TEST CASE 6 : LOGOUT =====")

try:
    logout = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//a[text()='Logout']")
        )
    )

    logout.click()

    wait.until(
        EC.visibility_of_element_located((By.NAME, "username"))
    )

    print("Logout Successful")

except Exception as e:
    print("Logout Test Failed")
    print(e)

input("\nPress Enter to Close Browser...")

driver.quit()