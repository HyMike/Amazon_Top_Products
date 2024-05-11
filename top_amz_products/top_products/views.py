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
from openai import OpenAI
import json
from pytrends.request import TrendReq
from serpapi import GoogleSearch

import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import io
import urllib
import base64
import os
from dotenv import load_dotenv


# create the list of categories
# if best seller list is empty get from model.


def home(request):
    best_seller_categories = Best_Sellers_List.objects.all()
    # pytrends

    # pytrends = TrendReq()
    # keywords = ['water']

    # pytrends.build_payload(keywords, timeframe='today 12-m')

    # trend_data = pytrends.interest_over_time()

    # trends_overtime = pytrends.interest_over_time()
    # print(trends_overtime)

    return render(request, 'top_products/home.html',
                  {"best_seller_categories": best_seller_categories, })


# matplot code:

def my_plot_view(trending_data):
    # Non-interactive graph

    matplotlib.use('Agg')

    images = []

    for product_name, query_data in trending_data.items():
        dates = query_data.get('date')
        values = query_data.get('value')

        # Check if both dates and values are present
        if dates is not None and values is not None:
            # Generate your data and plot here
            x = dates  # time
            y = values  # interest

        plt.figure(figsize=(10, 8))

        plt.plot(x, y)

        plt.xticks(rotation=45)
        plt.gca().set_xticks(x[::4])
        plt.ylim(0, 100)
        plt.show()

        plt.xlabel('Time')
        plt.ylabel('Interest Over Time')
        plt.title(product_name)
        # plt.legend(query_data['name'])

        # Adjust layout

        plt.tight_layout()

        # Save the plot to a BytesIO object
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        # Convert the plot to base64 encoding
        graphic = base64.b64encode(image_png)
        graphic = graphic.decode('utf-8')

        # Append the base64 encoded image to the list
        images.append(graphic)

        # Clear the plot for the next iteration
        plt.clf()

    return images


def format_content(title_list):
    # alter how many products will be returned from ChatGPT
    amount_product = 3
    client = OpenAI()

    # loop thru the product names to be enter to message content
    format_title_list = [f'"{title}"' for title in title_list]

    message_content = f"As a user, I need to simplify the product title so it can be effectively searched on Google Trends. Please remove any brand names and references to quantity from each of these {amount_product} product titles: \
    {', '.join(format_title_list)}. Return only {amount_product} simplified each product title with 2 to 5 words with no delimiters in a array"

    print("this is the message content: ", message_content)

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": message_content}
        ]
    )

    filtered_titles = completion.choices[0].message.content
    return filtered_titles


def products_trends(request):

    if request.method == 'POST':
        category_url = request.POST.get('selected_category_url')
        category_name = request.POST.get('selected_category_name')
        print(category_name)
        driver = webdriver.Chrome(service=ChromeService(
            ChromeDriverManager().install()))

        driver.get(category_url)
        product_names = []
        product_images = []

        # get the top level element
        products = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, '//div[contains(@id, "gridItemRoot")]')))

        # Getting product title
        for product in products[:3]:
            name = product.find_element(By.XPATH,
                                        './/div[@class="_cDEzb_p13n-sc-css-line-clamp-3_g3dy1"]')
            # './/div[@class="._cDEzb_p13n-sc-css-line-clamp-2_EWgCb"]')
            product_names.append(name.text)

        for product in products:
            images = WebDriverWait(product, 10).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, './/img[@class="a-dynamic-image p13n-sc-dynamic-image p13n-product-image"]'))

            )

        for image in images:
            product_images.append(image.get_attribute("src"))

        # returns list of 3 best sellers on Amazon from selected category that has been striped of title and package amounts to be searched
        # testing images

        formatted_content = json.loads(format_content(product_names))

        driver.quit()

        trending_data = get_trending_data(formatted_content)

        graphs = my_plot_view(trending_data)

        return render(request, 'top_products/products_trends.html',
                      {'products': formatted_content, 'graphs': graphs, 'category_name': category_name, })
        # return render(request, 'top_products/products_stats.html',
        # {"product_images": product_images})


def get_trending_data(amz_product_list):
    # serpAPI
    keywords = ",".join(amz_product_list)

    params = {
        "engine": "google_trends",
        "q": keywords,
        "data_type": "TIMESERIES",
        "api_key": os.getenv("SERPAPI_KEY")
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    interest_over_time = results["interest_over_time"]
    dict_data = extract_data(interest_over_time)
    return dict_data

# extract data to dictionary key being time vs value == the value

# create a default dictionary that can be populated
# use the formatted content and their order to populate the title for each
# of the graph.


def extract_data(interest_over_time):
    # Initialize an empty dictionary to hold the extracted data
    extracted_data = {}

    # Loop through each entry in the 'timeline_data'
    for entry in interest_over_time['timeline_data']:
        date = entry['date']
        values = entry['values']

        # Loop through each value entry
        for value_entry in values:
            query = value_entry['query']
            value = int(value_entry['value'])
            extracted_value = int(value_entry['extracted_value'])

            # If the query is not in the extracted_data dictionary, create a
            # new entry
            if query not in extracted_data:
                extracted_data[query] = {'date': [],
                                         'value': [], 'extracted_value': []}

            # Append data for each query
            extracted_data[query]['date'].append(date)
            extracted_data[query]['value'].append(value)
            extracted_data[query]['extracted_value'].append(extracted_value)
            # extracted_data[query]['name'].append(query)

    # Print the extracted data
    return extracted_data
