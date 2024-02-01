
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
bestseller_page = 'https://www.amazon.com/Best-Sellers/zgbs/'
# driver.get(web)
driver.get(bestseller_page)
# Books = "apple airpods"

product_name = []
product_images = []
top_seller_list = []

driver.maximize_window()

# search_box = WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.ID, 'twotabsearchtextbox'))
# )

# # search_button = driver.find_element(By.ID, 'nav-search-submit-button')
# search_button = WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.ID, 'nav-search-submit-button'))
# )
# search_button.click()

categories = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "_p13n-zg-nav-tree-all_style_zg-browse-item__1rdKf")]')))
for category in categories:
    name_category = category.find_element(
        By.XPATH, './/a[@href]')
    top_seller_list.append(name_category.text)


    

# products = WebDriverWait(driver, 10).until(
#     EC.presence_of_all_elements_located(
#         (By.XPATH, '//div[contains(@id, "gridItemRoot")]')))

# # Getting product title
# for product in products:
#     name = product.find_element(By.XPATH,
#                                 './/div[@class="_cDEzb_p13n-sc-css-line-clamp-1_1Fn1y"]')
#     product_name.append(name.text)

    #getting images for the product. 

# for product in products:
#     images = WebDriverWait(product, 10).until(
#         EC.presence_of_all_elements_located(
#             (By.XPATH, './/img[@class="a-dynamic-image p13n-sc-dynamic-image p13n-product-image"]'))

#     )

#     for image in images:
#         product_images.append(image.get_attribute("src"))


# print(product_name)
# print(product_images)
print(top_seller_list)

input("Press Enter to exit...")

# quitting the driver
driver.quit()
