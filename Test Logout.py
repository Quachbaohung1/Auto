import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
import subprocess

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def login(driver, username, password):
    url = "http://192.168.110.16:3081/#/login?returnUrl=%2F"
    driver.get(url)

    username_input = driver.find_element(By.XPATH, "//input[@id='exampleInputEmail']")
    password_input = driver.find_element(By.XPATH, "//input[@id='exampleInputPassword']")
    login_button = driver.find_element(By.XPATH, "//button[contains(text(),'Đăng nhập')]")

    username_input.send_keys(username)
    password_input.send_keys(password)
    login_button.click()

    try:
        dashboard_element = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//h3[normalize-space()='Dashboard Page']"))
        )
        assert dashboard_element.is_displayed(), f"Đăng nhập thành công - Pass (Username: {username}, Password: {password})"
    except Exception as e:
        pytest.fail(f"Đăng nhập thất bại - {e}")

def logout(driver):
    try:
        info_user = driver.find_element(By.XPATH, "//img[@class='img-profile rounded-circle']")
        info_user.click()

        logout_button = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(),'Đăng xuất')]"))
        )
        logout_button.click()

        login_page_element = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Đăng nhập')]"))
        )
        assert login_page_element.is_displayed(), "Đăng xuất thành công - Pass"

        time.sleep(2)

    except Exception as e:
        pytest.fail(f"Đăng xuất thất bại - {e}")

def test_login_and_logout(driver):
    login(driver, "Hungqb", "1")
    logout(driver)

def run_tests():
    # Chạy câu lệnh pytest để thực hiện test và tạo báo cáo HTML
    result = subprocess.run(['pytest', '--html=test_reports/report_Logout.html', __file__], capture_output=True, text=True)

    # Hiển thị kết quả trên terminal
    print(result.stdout)
    print(result.stderr)

if __name__ == "__main__":
    run_tests()
