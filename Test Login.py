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

@pytest.mark.parametrize("username, password, case_number", [
    ("Hungqb", "1", 1),
    ("nonexistent_user", "1", 2),
    ("Hungqb", "2", 3),
    ("", "1", 4),
    ("Hungqb", "", 5),
    ("", "", 6),
    ("special_chars!@#", "1", 7),
])
def test_login(driver, username, password, case_number):
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
        assert dashboard_element.is_displayed(), f"Case {case_number}: Đăng nhập thành công - Pass (Username: {username}, Password: {password})"
    except:
        error_messages_danger = driver.find_elements(By.XPATH,
                                                    "//div[contains(@class, 'alert alert-danger ng-star-inserted')]")
        error_messages_generic = driver.find_elements(By.XPATH,
                                                     "//div[contains(@class, 'ng-star-inserted')]")

        if error_messages_danger:
            print(
                f"Case {case_number}: Đăng nhập thất bại - Pass (Username: {username}, Password: {password}), có các thông báo lỗi sau:")
            for error_message in error_messages_danger:
                print(f"- {error_message.text}")
        elif error_messages_generic:
            print(
                f"Case {case_number}: Đăng nhập thất bại - Pass (Username: {username}, Password: {password}), có các thông báo lỗi sau:")
            for error_message in error_messages_generic:
                print(f"- {error_message.text}")
        else:
            pytest.fail(
                f"Case {case_number}: Đăng nhập thất bại - Fail (Username: {username}, Password: {password}), lỗi không xác định.")

def run_tests():
    # Chạy câu lệnh pytest để thực hiện test và tạo báo cáo HTML
    result = subprocess.run(['pytest', '--html=test_reports/report_Login.html', __file__], capture_output=True, text=True)

    # Hiển thị kết quả trên terminal
    print(result.stdout)
    print(result.stderr)

if __name__ == "__main__":
    run_tests()
