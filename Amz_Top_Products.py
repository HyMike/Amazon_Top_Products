
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome(service=ChromeService(
    ChromeDriverManager().install()))


# scrapping website
web = 'https://www.amazon.com/best-sellers-books-Amazon/zgbs/books/'
driver.get(web)
# Books = "apple airpods"

product_name = []
product_images = []

driver.maximize_window()

# search_box = WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.ID, 'twotabsearchtextbox'))
# )

# # search_button = driver.find_element(By.ID, 'nav-search-submit-button')
# search_button = WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.ID, 'nav-search-submit-button'))
# )
# search_button.click()


products = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located(
        (By.XPATH, '//div[contains(@id, "gridItemRoot")]')))

# Getting product title
for product in products:
    name = product.find_element(By.XPATH,
                                './/div[@class="_cDEzb_p13n-sc-css-line-clamp-1_1Fn1y"]')
    product_name.append(name.text)

# Getting images from product
# for product in products:
#     images = product.find_element(
#         By.XPATH, './/img[@class="a-dynamic-image p13n-sc-dynamic-image p13n-product-image"]').get_attribute("src")
#     product_images.append(images)

for product in products:
    images = WebDriverWait(product, 10).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, './/img[@class="a-dynamic-image p13n-sc-dynamic-image p13n-product-image"]'))

    )

    for image in images:
        product_images.append(image.get_attribute("src"))


# driver.implicitly_wait(10)
print(product_name)
print(product_images)

input("Press Enter to exit...")

# quitting the driver
driver.quit()
