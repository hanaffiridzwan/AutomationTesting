from robot.api.deco import keyword
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

class testcase_keywords():

    @keyword("user open the ${data1} and search ${data2}")
    def get_the_data(self, data1, data2):
        driver = webdriver.Chrome()
        self.search_data = data2
        self.web = data1
        if data1 == "Amazon":
            url = 'https://www.amazon.com/s?k={0}&r     ef=nb_sb_noss_2&page={1}'
        else:
            url = 'https://www.ebay.com.my/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw={0}&_sacat=0&page={1}'
        all_price_records = []
        all_description_records = []
        all_link_records = []
        for page in range(1, 3):
            driver.get(url.format(data2, page))
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            if data1 == "Amazon":
                results = soup.find_all('div', {'data-component-type': 's-search-result'})
            else:
                results = soup.find_all('li', {'class': 's-item'})
                print("results", results)
            for item in results:
                price_record = self.get_price_data(item, data1)
                print("price_record", price_record)
                description_record = self.get_description_data(item, data1)
                link_record = self.get_link_data(item, data1)
                if price_record:
                    all_price_records.append(price_record)
                if description_record:
                    all_description_records.append(description_record)
                if link_record:
                    all_link_records.append(link_record)
        self.all_price_records = all_price_records
        self.all_description_records = all_description_records
        self.all_link_records = all_link_records
        return all_price_records, all_description_records, all_link_records
        driver.close()

    @keyword("user save the record for Amazon")
    def save_record1(self):
        search_data = self.search_data
        price = self.all_price_records
        print("price", price)
        description = self.all_description_records
        print("description", description)
        link = self.all_link_records
        data_record1 = pd.DataFrame(zip(description, price, link), columns=["ItemName", "Price", "Link"])
        data_record1["Platform"] = "Amazon"
        data_record1 = data_record1[data_record1["ItemName"].str.contains(search_data) == True]
        data_record1 = data_record1[data_record1["Link"].str.contains("http") == True]
        print("data_record1", data_record1)
        self.data_record1 = data_record1
        data_record1.to_excel("amazondataoutput.xlsx")

    @keyword("user save the record for eBay")
    def save_record2(self):
        search_data = self.search_data
        price = self.all_price_records
        print("price", price)
        description = self.all_description_records
        print("description", description)
        link = self.all_link_records
        data_record2 = pd.DataFrame(zip(description, price, link), columns=["ItemName", "Price", "Link"])
        data_record2["Platform"] = "eBay"
        data_record2 = data_record2[data_record2["ItemName"].str.contains(search_data) == True]
        data_record2 = data_record2[data_record2["Link"].str.contains("http") == True]
        print("data_record2", data_record2)
        self.data_record2 = data_record2
        data_record2.to_excel("ebaydataoutput.xlsx")

    @keyword("combine the data")
    def combine_the_data(self):
        data_amazon = self.data_record1
        data_ebay = self.data_record2
        all_data = pd.concat([data_amazon, data_ebay], ignore_index=True)
        all_data = all_data.sort_values('Price', ascending=False)
        pd.set_option("display.max_rows", None, "display.max_columns", None)
        print("all_data", all_data)
        all_data.to_excel("output.xlsx")

    def get_price_data(self, data, search_data):
        """""trying to fetch the price data from the web"""
        if search_data == "Amazon":
            try:
                price_tree = data.find('span', 'a-price')
                print("price_tree", price_tree)
                price = price_tree.find('span', 'a-offscreen').text
                if price[0] == '$':
                    price = price[1:6]
                else:
                    price = '0'
                print("price", price)
            except AttributeError:
                price = '0'
            result_of_price = price
        else:
            try:
                price_tree = data.find('div', 's-item__info clearfix')
                print("price_tree", price_tree)
                price_without_format = price_tree.find('span', 's-item__price').text.replace(',', '')
                price = price_without_format[3:11]
                print("price", price)

            except AttributeError:
                price = '0'
            result_of_price = price
        return result_of_price

    def get_description_data(self, data, search_data):
        """""Trying to fetch the description data from the web"""
        if search_data == "Amazon":
            try:
                tree_navigation = data.h2.a
                description = tree_navigation.text.strip()
                print("description", description)
            except AttributeError:
                description = "no data"
        else:
            try:
                description = data.find('h3', 's-item__title').text
                print("description", description)
            except AttributeError:
                description = "no data"
        return description

    def get_link_data(self, data, search_data):
        """""Trying to fetch the link data from the web"""
        if search_data == "Amazon":
            try:
                link_parent = data.find('a')
                link = link_parent.attrs['href']
                print("link", link)
            except AttributeError:
                link = "no data"
        else:
            try:
                # link_head1 = data.find('div', 's-item__info clearfix')
                link_parent = data.find('a')
                # print("link_parent", link_parent)
                link = link_parent.attrs['href']
                print("link", link)
            except AttributeError:
                link = "no data"
        return link
















