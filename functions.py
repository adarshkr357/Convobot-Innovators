from bs4 import BeautifulSoup
import urllib.request as ur
import requests
import time
import urllib.parse
import html

def decode_text(text):
    decoded_text = urllib.parse.unquote(text)
    decoded_text = html.unescape(decoded_text)
    decoded_text = decoded_text.replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&apos;', "'").replace('&amp;', '&')
    return decoded_text


def get_keyword(query):
    while True:
        try:
            content_http_request_block = requests.post(
                "https://tools.socialbee.com/api/ai/chat/completion",
                headers={
                    "authority": "tools.socialbee.com",
                    "accept": "application/json, text/plain, */*",
                    "accept-language": "en-US,en;q=0.7",
                    "content-type": "application/json",
                    "origin": "https://tools.socialbee.com",
                    "referer": "https://tools.socialbee.com/ai-post-generator",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
                },
                json={
                    "messages": [
                        {
                            "content": f"{query}. This is a shopping user's input. Give me the keyword that needs to be searched according to user's input. Only tell the keyword nothing else.",
                            "role": "user"
                        }
                    ],
                    "n": 1,
                    "model": "gpt-3.5-turbo",
                    "temperature": 0.9
                }
            )
            content_http_request_block.raise_for_status()
            break
        except requests.exceptions.RequestException as err:
            print(f"Exception occurred: {err}")
            time.sleep(2)

    content_block_response = content_http_request_block.json()

    if "'role': 'assistant', 'content': '" not in str(content_block_response):
        return False

    return content_block_response["choices"][0]["message"]["content"]


def get_amazon(product, number_of_results=1):
    
    req = ur.Request(f"https://www.amazon.in/s?k={product}")

    webpage = ur.urlopen(req)

    soup = BeautifulSoup(webpage, "html.parser")

    product_name = soup.find_all("span", {"class":"a-size-base-plus a-color-base a-text-normal"}, limit=number_of_results)
    product_price = soup.find_all("span", {"class":"a-price-whole"}, limit=number_of_results)
    product_rating = soup.find_all("span", {"class":"a-icon-alt"}, limit=number_of_results)
    image_link = soup.find_all("img", {"class":"s-image"}, limit=number_of_results)

    for i in range(number_of_results):
        product_name[i] = product_name[i].text
        product_price[i] = product_price[i].text
        product_rating[i] = product_rating[i].text
        image_link[i] = image_link[i].get("src")

    return ["Amazon", image_link[0], decode_text(product_name[0]), product_rating[0].replace(' out of 5 stars', ''), product_price[0]]


def get_snapdeal(product, number_of_results=1):

    req = ur.Request(f"https://www.snapdeal.com/search?keyword={product}")
    webpage = ur.urlopen(req)

    soup = BeautifulSoup(webpage, "html.parser")
     
    product_name = soup.find_all("p", {"class":"product-title"}, limit=number_of_results)
    product_price = soup.find_all("span", {"class":"lfloat product-price"}, limit=number_of_results)
    product_rating = soup.find_all("div", {"class":"clearfix rating av-rating"}, limit=number_of_results)
    image_link = soup.find_all("img", {"class":"product-image"}, limit=number_of_results)

    for i in range(number_of_results):
        product_name[i] = product_name[i].get("title")
        product_price[i] = product_price[i].get("display-price")
        product_rating[i] = float(str(product_rating[i]).split("width:")[-1].split("%")[0]) / 20
        image_link[i] = image_link[i].get("src")

    return ["Snapdeal", image_link[0], decode_text(product_name[0]), float("{:.2f}".format(product_rating[0])), product_price[0]]
