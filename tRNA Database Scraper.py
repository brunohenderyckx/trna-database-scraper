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
    
    # Creates empty lists to popualte with the scrape outputs
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
    for i in range(0,10000):
        try:
            # pulls the URLs from the table, to then access
            elem = driver.find_element_by_xpath('/html/body/div/div/section[1]/div/div/div/div/section/div[2]/div/div/div[2]/div[2]/table/tbody//tr[' + str(i) + ']/td[1]/a')
            links.append(elem.get_attribute('href'))

        except:
            continue

    # accesses every link stored in the list and extracts the information we want
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

# Creates a Selenium webdriver instance that we'll control later
driver = webdriver.Chrome('./chromedriver')

# Creates an empty pandas dataframe, that we'll populate after the scraping is completed
df = pd.DataFrame(columns=['link', 'up down', 'gen seq','predic mature'])

# Add the URLs you want to scrape to this list
urls = ['http://gtrnadb.ucsc.edu/GtRNAdb2/genomes/eukaryota/Schi_pomb_972h/Schi_pomb_972h-gene-list.html',
'http://gtrnadb.ucsc.edu/genomes/eukaryota/Scere3/Scere3-gene-list.html',
'http://gtrnadb.ucsc.edu/genomes/eukaryota/Dmela6/Dmela6-displayed-gene-list.html',
'http://gtrnadb.ucsc.edu/genomes/eukaryota/Athal10/Athal10-displayed-gene-list.html',
'http://gtrnadb.ucsc.edu/genomes/eukaryota/Mmusc10/Mmusc10-displayed-gene-list.html',
'http://gtrnadb.ucsc.edu/genomes/eukaryota/Hsapi19/Hsapi19-displayed-gene-list.html']

# Loops over the URLs you added and scrapes the information from them by executing the scrape_CER function
for url in urls:
    df = df.append(scrape_CER(url))

# Saves the scraped data to an excel file
df.to_excel('tRNA Database Scraper.xlsx')
