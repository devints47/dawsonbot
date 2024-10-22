import cv2
import pytesseract
import argparse
import time

from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from datetime import datetime

start_time = time.time()

email = ""
pw = ""


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="SalesOrder_img.png")

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

def read_img():
    """ Read image and convert to text """
    # construct the argument parser and parse the arguments

    args = vars(ap.parse_args())

    # load the image and convert it to grayscale
    image = cv2.imread(args["image"])
    cv2.imshow("Original", image)

    # Apply an "average" blur to the image

    blurred = cv2.blur(image, (3,3))
    cv2.imshow("Blurred_image", blurred)
    img = Image.fromarray(blurred)
    text = pytesseract.image_to_string(img, lang='eng')
    lines = text.split("\n")
    # for i, line in enumerate(lines):
    #     print(f"Line {i}: {line}")
    return lines


def process_lines(lines):
    """ Break out processed text from image into lists """
    descriptions = []
    quantities = []
    unit_prices = []
    discounts = []

    for i, line in enumerate(lines):
        if line == '':
            lines.pop(i)

    for i, line in enumerate(lines):
        print(f"Line {i}: {line}")
    for i, line in enumerate(lines):
        if "Kratom" in line:
            lines[i] = lines[i].replace("Kratom", "Mitra")
        if "Quantity" in line:
            descriptions = lines[0:i]
            count = i
            quantities = lines[i+1:i+count+1]

        if "Unit Price" in line and "Discount" in line:
            unit_prices = lines[i+1:i+count+1]
            discounts = lines[i+count:i+count+count]
        elif "Unit Price" in line and "Discount" not in line:
            unit_prices = lines[i+1:i+count+1]
            discounts = lines[i+count+1:i+count+count+1]


    for i, description in enumerate(descriptions):
        print(f"{i} - Description: {descriptions[i]}, Quantity: {quantities[i]}, Unit Price: {unit_prices[i]}, Discount: {discounts[i]}")
    return descriptions, quantities, unit_prices, discounts


def make_dawsons_day(descriptions, quantities, unit_prices, discounts):
    """ Selenium script to login to website and input inventory """
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://app.xtrachef.com/XtraChefAccount/Account/LogOn')
    driver.find_element(by='id', value='username').send_keys(email)
    driver.find_element(by="name", value="action").click()
    time.sleep(1)
    driver.find_element(by="id", value="password").send_keys(pw)
    driver.find_element(by="name", value="action").click()
    time.sleep(1)
    driver.find_elements(by="name", value="action")[2].click()
    time.sleep(1)
    driver.find_element(by="id", value="btnAllowParallelLogin").click()
    time.sleep(1)
    driver.get('https://app.xtrachef.com/Invoice/Invoice/InvoiceList')
    time.sleep(1)
    driver.find_element(by="id", value="menu-dropdown-2").click()
    time.sleep(1)
    driver.find_element(by="id", value="menu-dropdown-2-contents").click()
    time.sleep(2)

    driver.find_element(by="id", value="VendorName").click()
    driver.find_element(by="id", value="VendorName").send_keys("MITRA")
    time.sleep(1)
    driver.find_element(by="id", value="VendorName").send_keys(Keys.DOWN)
    driver.find_element(by="id", value="VendorName").send_keys(Keys.ENTER)
    time.sleep(1)

    driver.find_element(by="id", value="IdStreetAddress").click()
    driver.find_element(by="id", value="IdStreetAddress").clear()
    driver.find_element(by="id", value="IdStreetAddress").send_keys("16810 Oriole Rd, Suite 7")
    driver.find_element(by="id", value="IdCity").click()
    driver.find_element(by="id", value="IdCity").clear()
    driver.find_element(by="id", value="IdCity").send_keys("Fort Myers")
    driver.find_element(by="id", value="IdState").click()
    driver.find_element(by="id", value="IdState").clear()
    driver.find_element(by="id", value="IdState").send_keys("FL")
    driver.find_element(by="id", value="IdZipCode").click()
    driver.find_element(by="id", value="IdZipCode").clear()
    driver.find_element(by="id", value="IdZipCode").send_keys("33912")
    driver.find_element(by="id", value="IdCountry").click()
    driver.find_element(by="id", value="IdCountry").clear()
    driver.find_element(by="id", value="IdCountry").send_keys("US")
    driver.find_element(by="id", value="InvDate").click()

    for i, description in enumerate(descriptions):
        if description == 'Keg Deposit':
            continue
        driver.find_element(by="id", value="DivAddLineItem").click()
        time.sleep(2)
        row = driver.find_element(by="id", value=f"{i}")
        row.find_element(by="id", value=f"ItemDescription_{i}").click()
        row.find_element(by="id", value=f"ItemDescription_{i}").send_keys(description[:10])
        time.sleep(1)
        row.find_element(by="id", value=f"ItemDescription_{i}").send_keys(Keys.DOWN)
        row.find_element(by="id", value=f"ItemDescription_{i}").send_keys(Keys.ENTER)
        row.find_element(by="id", value=f"Qty_{i}").send_keys(quantities[i])
        row.find_element(by="id", value=f"UnitPrice_{i}").send_keys(Keys.CONTROL + "a")
        row.find_element(by="id", value=f"UnitPrice_{i}").send_keys(Keys.DELETE)
        row.find_element(by="id", value=f"UnitPrice_{i}").send_keys(unit_prices[i])

    return



lines = read_img()
descriptions, quantities, unit_prices, discounts = process_lines(lines)
text = input("Does this look right? y/n\n")
if text == 'y':
    make_dawsons_day(descriptions, quantities, unit_prices, discounts)
    print("--- Inventory finished in %s seconds ---" % round((time.time() - start_time)), 3)
else:
    text = input("Try taking another screenshot and inputting the image again. sowwy :(")
