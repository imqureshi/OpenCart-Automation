import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from pynput.mouse import Button, Controller
import keyboard
import time
driver = webdriver.Chrome()
act = ActionChains(driver)
dfs = pd.read_excel('Enter the path to excel file')
mouse = Controller()


def auth():
    username = driver.find_element_by_id('input-username')
    password = driver.find_element_by_id('input-password')
    content = driver.find_element_by_class_name('btn-primary')
    username.send_keys('Enter Username')  # Enter Admin Panel UserName
    password.send_keys('Enter Password')  # Enter Admin Panel Password
    content.click()


def gen(product, tags):
    product_form = driver.find_element_by_id('input-name1')
    meta_form = driver.find_element_by_id('input-meta-title1')
    tags_form = driver.find_element_by_id('input-tag1')
    meta_tags_form = driver.find_element_by_id('input-meta-keyword1')

    # filling the general form
    product_form.send_keys(product)
    meta_form.send_keys(product)
    tags_form.send_keys(tags)
    meta_tags_form.send_keys(tags)


def data(model, sku, price, Quan):
    # opening data
    data_link = driver.find_element_by_link_text('Data')
    data_link.click()

    # selecting form
    model_form = driver.find_element_by_id('input-model')
    sku_form = driver.find_element_by_id('input-sku')
    price_form = driver.find_element_by_id('input-price')
    quantity_form = driver.find_element_by_id('input-quantity')

    # filling the data form
    model_form.send_keys(model)
    sku_form.send_keys(sku)
    price_form.send_keys(price)
    quantity_form.send_keys(Quan)

# Adding releated products to each item according to its catagory


def link(sub, sku):
    # opening links
    links_link = driver.find_element_by_link_text('Links')
    links_link.click()
    category_form = driver.find_element_by_name('category')
    rel_form = driver.find_element_by_id('input-related')

    # filling form
    category_form.send_keys(sub)
    time.sleep(2)
    mouse.position = (431, 380)
    time.sleep(1)
    mouse.click(Button.left, 1)
    df1 = L_giv(sub)
    time.sleep(1)
    df1 = df1.reset_index(drop=True)  # important shit
    if(df1['SKU'][0] == int(sku)):
        print('working')
    elif(df1['SKU'][1] == int(sku)):
        print(df1['Product Title'][0])
        rel_form.send_keys(df1['Product Title'][0])
        mouse.position = (512, 685)
        time.sleep(2)
        mouse.click(Button.left, 1)
    elif(df1['SKU'][2] == int(sku)):
        print(df1['Product Title'][1])
        print(df1['Product Title'][0])
        rel_form.send_keys(df1['Product Title'][0])
        mouse.position = (512, 685)
        time.sleep(2)
        mouse.click(Button.left, 1)
        rel_form.send_keys(df1['Product Title'][1])
        mouse.position = (512, 685)
        time.sleep(2)
        mouse.click(Button.left, 1)
    else:
        for i in range(len(df1)):
            if(df1['SKU'][i] == int(sku)):
                print(df1['Product Title'][i-1])
                print(df1['Product Title'][i-2])
                print(df1['Product Title'][i-3])
                rel_form.send_keys(df1['Product Title'][i-3])
                mouse.position = (512, 685)
                time.sleep(2)
                mouse.click(Button.left, 1)
                rel_form.send_keys(df1['Product Title'][i-2])
                mouse.position = (512, 685)
                time.sleep(2)
                mouse.click(Button.left, 1)
                rel_form.send_keys(df1['Product Title'][i-1])
                mouse.position = (512, 685)
                time.sleep(2)
                mouse.click(Button.left, 1)


def L_giv(sub):
    names = dfs.Subcat.unique()
    df_list = list()
    j = 0
    for i in names:
        dfs_new = dfs[dfs.Subcat == i]
        df_list.append(dfs_new)
        if(i == sub):
            return df_list[j]
        j += 1


def image(img):
    Links_image = driver.find_element_by_link_text('Image')
    Links_image.click()
    input_image = driver.find_element_by_class_name('img-thumbnail')
    input_image.click()
    input_upload = driver.find_element_by_id('button-image')
    input_upload.click()
    time.sleep(2)
    mouse.position = (501, 253)
    time.sleep(1)
    mouse.click(Button.left, 1)
    time.sleep(0.5)
    keyboard.write(img)
    time.sleep(0.5)
    mouse.position = (742, 253)
    time.sleep(1)
    mouse.click(Button.left, 1)
    time.sleep(1)
    mouse.position = (263, 361)
    time.sleep(3)
    mouse.click(Button.left, 1)


def main():
    for i in range(len(dfs)):
        # Enter Url of your opencart cpanel
        driver.get('Enter the URL to admin panel')
        sku = dfs['SKU'][i]
        sku = str(sku)
        product = dfs['Product Title'][i]
        sub = dfs['Subcat'][i]
        price = dfs['Price'][i]
        price = str(price)
        tags = dfs['Tags'][i]
        model = dfs['Model'][i]
        Quan = dfs['Quantity'][i]
        Quan = str(Quan)
        img = dfs['Images'][i]
        img = str(img)
        auth()
        gen(product, tags)
        data(model, sku, price, Quan)
        link(sub, sku)
        image(img)
        driver.find_element_by_css_selector(
            'button.btn.btn-primary').click()  # Button to save the product


if __name__ == "main":
    main()
