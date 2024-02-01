from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# everything that is needed for selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json


# Create your views here.


# def index(request):
#     # return HttpResponse("hello, I am working!")
#     context = {
#         "iphone": 'this is my iphone 13 pro max!',
#         "tudor": 'I have a tudor black bay 58!'
#     }
#     return render(request, "top_products/home.html", context)


def categories(request):
    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()))
    # driver.maximize_window()
    bestseller_page = 'https://www.amazon.com/Best-Sellers/zgbs/'
    driver.get(bestseller_page)
    top_sellers_list = {}
    categories = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "_p13n-zg-nav-tree-all_style_zg-browse-item__1rdKf")]')))
    for category in categories:
        category_html = category.find_element(
            By.XPATH, './/a[@href]')
        link_category = category_html.get_attribute("href")
        name_category = category_html.text
        # top_sellers_list[name_category] = 1
        top_sellers_list[name_category] = link_category
    # print(top_sellers_list)
    return render(request, "top_products/home.html", {"top_sellers_list": top_sellers_list})


# def innerCategories(request):
def scraping_data(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'POST':
        url = request.POST.get("url")
        if url:
            try:
                driver = webdriver.Chrome(service=ChromeService(
                    ChromeDriverManager().install()))

                driver.get(url)
                product_name = []

                # get the top level element
                products = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, '//div[contains(@id, "gridItemRoot")]')))

                # Getting product title
                for product in products:
                    try:
                        name = product.find_element(By.XPATH,
                                                    './/div[@class="_cDEzb_p13n-sc-css-line-clamp-3_g3dy1"]')
                        product_name.append(name.text)
                # print(product_name)
                    except Exception as e:
                        print(f"Error extracting product name: {str(e)}")

                driver.quit()

                return JsonResponse({'product_name': product_name})

            except Exception as e:
                print(f"Error during scraping: {str(e)}")
                return JsonResponse({'error': str(e)}, status=500)

        return JsonResponse({'error1': 'Invalid request'}, status=400)

    return JsonResponse({'error2': 'Invalid request'}, status=400)

    # getting images for the product.

# for product in products:
#     images = WebDriverWait(product, 10).until(
#         EC.presence_of_all_elements_located(
#             (By.XPATH, './/img[@class="a-dynamic-image p13n-sc-dynamic-image p13n-product-image"]'))

#     )

#     for image in images:
#         product_images.append(image.get_attribute("src"))


# # the div class that i need to get the title
# # class="_cDEzb_p13n-sc-css-line-clamp-3_g3dy1"
