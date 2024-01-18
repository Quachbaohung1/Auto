import time
import random
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
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

def add_supplier(driver, id, name, address, phone):
    # Nhấp vào nút thêm nhà cung cấp
    add_button = driver.find_element(By.XPATH, "//i[@class='fa-solid fa-plus']")
    add_button.click()

    # Nhập thông tin nhà cung cấp
    id_input = driver.find_element(By.XPATH, "//div[@class='col-3']")
    time.sleep(2)
    name_input = driver.find_element(By.XPATH, "//div[@class='col-9']")
    time.sleep(2)
    address_input = driver.find_element(By.XPATH, "//span[contains(text(),'Địa chỉ')]")
    time.sleep(2)
    phone_input = driver.find_element(By.XPATH, "//input[@class='form-control ng-untouched ng-pristine ng-valid']")
    time.sleep(2)
    combobox_element = driver.find_element(By.XPATH, "//div[@class='ngx-select__toggle btn form-control']")
    time.sleep(2)
    # Nhấn vào input để mở danh sách quốc gia
    combobox_element.click()
    # Chờ cho danh sách quốc gia xuất hiện
    country_list = WebDriverWait(driver, 3).until(
        EC.visibility_of_element_located((By.XPATH, "//ul[@role='menu']"))
    )
    # Sử dụng Select để tương tác với combobox
    select = Select(country_list)
    # Lấy danh sách tất cả các giá trị trong combobox
    all_options = select.options
    # Chọn một giá trị ngẫu nhiên từ danh sách
    random_option = random.choice(all_options)
    # Chọn giá trị trong combobox
    select.select_by_value(random_option.get_attribute("value"))
    # Chờ một khoảng thời gian (để bạn có thể kiểm tra kết quả)
    driver.implicitly_wait(5)

    id_input.send_keys(id)
    name_input.send_keys(name)
    address_input.send_keys(address)
    phone_input.send_keys(phone)

    # Nhấp vào nút lưu
    save_button = driver.find_element(By.XPATH, "//button[contains(text(),'Lưu')]")
    save_button.click()

#def delete_supplier(driver, supplier_name):
    # Chọn nhà cung cấp từ danh sách
    #supplier_checkbox = driver.find_element(By.XPATH, f"//td[contains(text(),'{supplier_name}')]/preceding-sibling::td/input")
    #supplier_checkbox.click()

    # Nhấp vào nút xoá
    #delete_button = driver.find_element(By.XPATH, "//button[contains(text(),'Xoá')]")
    #delete_button.click()

    # Xác nhận xoá
    #confirm_delete_button = driver.find_element(By.XPATH, "//button[contains(text(),'Xác nhận xoá')]")
    #confirm_delete_button.click()

#def edit_supplier(driver, supplier_name, new_address):
    # Chọn nhà cung cấp từ danh sách
    #supplier_checkbox = driver.find_element(By.XPATH, f"//td[contains(text(),'{supplier_name}')]/preceding-sibling::td/input")
    #supplier_checkbox.click()

    # Nhấp vào nút sửa
    #edit_button = driver.find_element(By.XPATH, "//button[contains(text(),'Sửa')]")
    #edit_button.click()

    # Sửa thông tin
    #address_input = driver.find_element(By.XPATH, "//input[@id='address']")
    #address_input.clear()
    #address_input.send_keys(new_address)

    # Nhấp vào nút lưu
    #save_button = driver.find_element(By.XPATH, "//button[contains(text(),'Lưu')]")
    #save_button.click()

def NCC(driver):
    # Nhấp vào menu Danh mục trên dashboard
    category_menu = driver.find_element(By.XPATH, "//a[@id='category']")
    category_menu.click()

    # Nhấp vào menu Nhà cung cấp trên dashboard
    supplier_menu = driver.find_element(By.XPATH, "//a[@id='customer-page']")
    supplier_menu.click()

    # Chờ đến khi trang Nhà cung cấp hiển thị
    WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.XPATH, "//h6[contains(text(),'DANH SÁCH NHÀ CUNG CẤP')]"))
    )

    # Thực hiện các thao tác khác trên trang Nhà cung cấp
    add_supplier(driver, "BH001", "Supplier A", "Address A", "123456789")
    #delete_supplier(driver, "Supplier A")
    #edit_supplier(driver, "Supplier B", "New Address B")

    # Ví dụ: kiểm tra sự tồn tại của một yếu tố
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//th[normalize-space()='Tên Nhà cung cấp']"))
    )

def test_login_and_NCC(driver):
    login(driver, "Hungqb", "1")
    NCC(driver)

def run_tests():
    # Chạy câu lệnh pytest để thực hiện test và tạo báo cáo HTML
    result = subprocess.run(['pytest', '--html=test_reports/report_NCC.html', __file__], capture_output=True, text=True)

    # Hiển thị kết quả trên terminal
    print(result.stdout)
    print(result.stderr)

if __name__ == "__main__":
    run_tests()
