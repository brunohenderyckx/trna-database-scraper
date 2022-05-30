from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import pandas as pd
import time


def scrape_CER(url):
    """
    Function that takes in a gtrnadb URL listing genes, looping over them and extracting key information (e.g. Upstream / Downstream Sequence)
    """
    # Opens Selenium webdriver
    driver.get(url)
    links = []
    cola = []
    colb = []
    colc = []
    cold = []

    time.sleep(2)

    select = Select(driver.find_element_by_xpath('/html/body/div/div/section[1]/div/div/div/div/section/div[2]/div/div/div[1]/div[1]/div/label/select'))
    select.select_by_visible_text('All')

    time.sleep(2)

    # for every gene on the page, get the links for scraping purposes
    for i in range(0,400):
        try:
            elem = driver.find_element_by_xpath('/html/body/div/div/section[1]/div/div/div/div/section/div[2]/div/div/div[2]/div[2]/table/tbody/tr[' + str(i) + ']/td[1]/a')
            links.append(elem.get_attribute('href'))

        except:
            continue

    for link in links:
        driver.get(link)
        cola.append(link)
        for i in range(1,15):
            try:
                if driver.find_element_by_xpath('/html/body/div/div/section[1]/div/div/div/div/section/div[2]/div/table/tbody/tr['+ str(i) + ']/td[1]').text == 'Upstream / Downstream Sequence':
                    colb_value = driver.find_element_by_xpath('/html/body/div/div/section[1]/div/div/div/div/section/div[2]/div/table/tbody/tr['+ str(i) + ']/td[2]').text
                    print("for",link,"index",i,"was found, value",colb_value)
            except:
                pass
        colb.append(colb_value)
        colc.append(driver.find_element_by_xpath('/html/body/div/div/section[1]/div/div/div/div/section/div[4]/div/table/tbody/tr[1]/td[2]/pre').text)
        cold.append(driver.find_element_by_xpath('/html/body/div/div/section[1]/div/div/div/div/section/div[4]/div/table/tbody/tr[3]/td[2]/pre').text)

    print("done")
    time.sleep(2)
    
    # Create a dataframe with all the scraped data
    df = pd.DataFrame()
    df['link']  = cola
    df['up down'] = colb
    df['gen seq'] = colc
    df['predic mature'] = cold

    # Return the dataframe to save as an excel
    return df

driver = webdriver.Chrome('./chromedriver')
df = pd.DataFrame(columns=['link', 'up down', 'gen seq','predic mature'])

# Add the URLs you want to scrape to this list
urls = ['http://gtrnadb.ucsc.edu/genomes/eukaryota/Scere3/Scere3-gene-list.html']

# Loops over the URLs you added and scrapes the information from them
for url in urls:
    df = df.append(scrape_CER(url))

# Saves the scraped data to an excel file
df.to_excel('Scere 3 example file.xlsx')
