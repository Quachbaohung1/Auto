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
    #Case 1: Đăng nhập thành công
    ("Hungqb", "1", 1),
    #Case 2: Nhập sai username
    ("nonexistent_user", "1", 2),
    #Case 3: Nhập sai password
    ("Hungqb", "2", 3),
    #Case 4: Không nhập username
    ("", "1", 4),
    #Case 5: Không nhập password
    ("Hungqb", "", 5),
    #Case 6: Bấm btn đăng nhập mà không nhập gì
    ("", "", 6),
    #Case 7: Nhập username là kí tự đặc biệt
    ("special_chars!@#", "1", 7),
    # Case 8: Kiểm tra hiển thị dấu chấm khi nhập password
    ("Hungqb", "hidden_password", 8),
])
def test_login(driver, username, password, case_number):
    url = "http://192.168.110.16:3081/#/login?returnUrl=%2F"
    driver.get(url)

    username_input = driver.find_element(By.XPATH, "//input[@id='exampleInputEmail']")
    password_input = driver.find_element(By.XPATH, "//input[@id='exampleInputPassword']")
    login_button = driver.find_element(By.XPATH, "//button[contains(text(),'Đăng nhập')]")

    username_input.send_keys(username)
    # Kiểm tra hiển thị dấu chấm khi nhập password
    if password in password:
        password_type = password_input.get_attribute("type")
        assert password_type == "password"

        # Thêm câu thông báo tương ứng
        if password_type == "password":
            print(f"Case {case_number}: Password hiển thị dưới dạng dấu chấm.")
        else:
            pytest.fail(f"Case {case_number}: Password không hiển thị dưới dạng dấu chấm.")
    password_input.send_keys(password)
    login_button.click()

    try:
        dashboard_element = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//h3[normalize-space()='Dashboard Page']"))
        )
        assert dashboard_element.is_displayed()
        print(f"Case {case_number}: Đăng nhập thành công - Pass (Username: {username}, Password: {password})")
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
