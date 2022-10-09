from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent


## Marcando o Tempo de de execução

init = time.perf_counter()

web = "https://www.zattini.com.br/masculino"
path = "C:/Users/henri/Desktop/chromedriver/chromedriver.exe"

options = Options()

# Alterado UserAgent para evitar bloqueio
ua = UserAgent()
userAgent = ua.random
options.add_argument(f"user-agent={userAgent}")
options.add_argument("--headless")

# Definindo caminho do driver
driver = webdriver.Chrome(path, chrome_options=options)
driver.get(web)
driver.maximize_window()


product_name = []
product_link = []
product_list_price = []
product_final_price = []
product_discount_rate = []


while True:
    # Selecionando todos os produtos da paginas
    products = driver.find_elements(By.XPATH, '//div[@class="wrapper"]//a')
    for product in products:
        product_name.append(product.get_attribute("href"))
        product_link.append(product.get_attribute("title"))
        product_list_price.append(product.get_attribute("data-list-price"))
        product_final_price.append(product.get_attribute("data-final-price"))
        product_discount_rate.append(product.get_attribute("data-discount-percentage"))

    next_page = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                '//div[@class="pagination"]//a[@class="ns-icon ns-icon-arrow-right last next"]',
            )
        )
    )
    driver.execute_script("arguments[0].scrollIntoView();", next_page)
    next_page_link = next_page.get_attribute("href")
    if next_page_link:
        driver.get(next_page_link)
        print(f"Link da pagina Atual{next_page_link}")
    else:
        break

df_dafiti = pd.DataFrame(
    {
        "name": product_name,
        "link": product_link,
        "final_price": product_final_price,
        "list_price": product_list_price,
        "discount-percentage": product_discount_rate,
    }
)
df_dafiti.to_csv("books_pagination.csv")
driver.quit()

end = time.perf_counter()
time_exec = end - init
print(time_exec)
