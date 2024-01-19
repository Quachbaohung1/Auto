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
    add_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//i[@class='fa-solid fa-plus']"))
    )
    add_button.click()

    # Nhập thông tin nhà cung cấp
    id_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='col-3']//input[@class='form-control ng-untouched ng-pristine ng-valid']"))
    )
    id_input.send_keys(id)

    name_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='col-9']//input[@class='form-control ng-untouched ng-pristine ng-valid']"))
    )
    name_input.send_keys(name)

    address_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//textarea[@class='form-control ng-untouched ng-pristine ng-valid']"))
    )
    address_input.send_keys(address)

    phone_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='col col-sm-4']//input[@class='form-control ng-untouched ng-pristine ng-valid']"))
    )
    phone_input.send_keys(phone)

    # Sử dụng hàm chọn quốc gia ngẫu nhiên
    select_random_option(driver, "//ngx-select[@id='input-country']//div[@class='ngx-select__toggle btn form-control']")

    # Nhấp vào nút lưu
    save_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Lưu')]"))
    )
    save_button.click()

    #Nhấn vào nút Huỷ
    cancel_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='modal-dialog modal-lg']//button[@type='button'][contains(text(),'Huỷ')]"))
    )
    cancel_button.click()
def select_random_option(driver, combobox_xpath):
    combobox_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, combobox_xpath))
    )
    combobox_element.click()

    # Chờ cho danh sách quốc gia xuất hiện
    country_list = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//ul[@role='menu']"))
    )

    # Lấy danh sách tất cả các mục trong danh sách quốc gia
    options = country_list.find_elements(By.XPATH, "//div[@id='customer-detail-modal']//li[2]//a[1]")

    # Chọn một giá trị ngẫu nhiên từ danh sách
    random_option = random.choice(options)

    # Nhấn vào giá trị ngẫu nhiên để chọn
    random_option.click()

    # Chờ một khoảng thời gian (để bạn có thể kiểm tra kết quả)
    driver.implicitly_wait(5)

def check_search(driver, keyword):
    # Nhập từ khóa vào ô tìm kiếm
    search_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@type='search']"))
    )
    search_input.clear()
    search_input.send_keys(keyword)

    # Nhấn Enter để thực hiện tìm kiếm
    search_input.submit()

    # Chờ kết quả xuất hiện
    search_results = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//td[@class='sorting_1']"))
    )

    # Kiểm tra xem có kết quả nào xuất hiện không
    if len(search_results) > 0:
        print(f'Tìm kiếm cho "{keyword}" thành công - Pass')
    else:
        print(f'Tìm kiếm cho "{keyword}" thất bại - Fail')

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
    check_search(driver, "BH001")
    #delete_supplier(driver, "Supplier A")
    #edit_supplier(driver, "Supplier B", "New Address B")

    # Ví dụ: kiểm tra sự tồn tại của một yếu tố
    WebDriverWait(driver, 3).until(
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
