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
from .models import Best_Sellers_List
from .forms import CategoryForm


# create the list of categories
# if best seller list is empty get from model.

def home(request):
    best_seller_categories = Best_Sellers_List.objects.all()
    return render(request, 'top_products/home.html', {"best_seller_categories": best_seller_categories})


def scrape_category(request):
    return HttpResponse('Yeah, You did it!')


def products_stats(request):
    if request.method == 'POST':
        category_url = request.POST.get('selected_category_url')
        driver = webdriver.Chrome(service=ChromeService(
            ChromeDriverManager().install()))

        driver.get(category_url)
        product_name = []

        # get the top level element
        products = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, '//div[contains(@id, "gridItemRoot")]')))

        # Getting product title
        for product in products[:3]:
            name = product.find_element(By.XPATH,
                                        './/div[@class="_cDEzb_p13n-sc-css-line-clamp-3_g3dy1"]')
            # './/div[@class="._cDEzb_p13n-sc-css-line-clamp-2_EWgCb"]')
            product_name.append(name.text)
        driver.quit()
        return render(request, 'top_products/products_stats.html', {'products': product_name})
        # print(product_name)


def categories(request):

    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()))
    bestseller_page = 'https://www.amazon.com/Best-Sellers/zgbs/'
    driver.get(bestseller_page)
    top_sellers_list = {}
    link_category = None
    name_category = None
    categories = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "_p13n-zg-nav-tree-all_style_zg-browse-item__1rdKf")]')))
    for category in categories:
        category_html = category.find_element(
            By.XPATH, './/a[@href]')
        if category_html.text in best_seller_list:
            name_category = category_html.text
            link_category = category_html.get_attribute("href")

        if name_category and link_category is not None:
            top_sellers_list[name_category] = link_category
    print(top_sellers_list)
    return render(request, "top_products/home.html", {"top_sellers_list": top_sellers_list})


# grabs all of the clicked inner category items.

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
                        # './/div[@class="._cDEzb_p13n-sc-css-line-clamp-2_EWgCb"]')
                        product_name.append(name.text)
                # print(product_name)
                    except Exception as e:
                        print(f"Error extracting product name: {str(e)}")

                driver.quit()

                return JsonResponse({'product_name': product_name})
                # return render(request, 'top_products/products.html', {'product_name': product_name})
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

def products(request):
    things = ['bestbuy', 'nike', 'coffee']
    context = {'products': things}
    return render(request, "top_products/products.html", context)
