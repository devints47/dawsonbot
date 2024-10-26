import cv2
import pytesseract
import argparse
import time

from PIL import Image
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from datetime import datetime

start_time = time.time()

email = ""
pw = ""

print("Dawsonbot intializing...\n")
time.sleep(1)


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

    # Apply an "average" blur to the image

    blurred = cv2.blur(image, (3,3))
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
        if "Item" in line:
            lines.pop(i)
        if line == "Price":
            lines.pop(i)

    for i, line in enumerate(lines):
        if line == '':
            lines.pop(i)
        if "Item" in line:
            lines.pop(i)
        if line == "Price":
            lines.pop(i)
        print(f"Line {i}: {line}")

    for line in lines:
        if "Kratom" in line:
            line = line.replace("Kratom", "Mitra")
            descriptions.append(str(line))
        elif "Kava" in line:
            descriptions.append(str(line))
        elif "Keg" in line:
            descriptions.append(str(line))


    count = len(descriptions)
    del lines[0:len(descriptions)]

    print(descriptions)
    print(len(descriptions))
    #
    # for i, line in enumerate(lines):
    #     print(f"Line {i}: {line}")
    for i, line in enumerate(lines):
        if "Quantity" in line:
            quantities = lines[i+1:i+count+1]
            print("hit quantity")

        if "Unit" in line:
            unit_prices = lines[i+1:i+count+1]
            print("hit unit price")

    print(len(descriptions), len(quantities), len(unit_prices))

    if len(quantities) == 0:
        quantities = [0]*len(descriptions)
    if len(unit_prices) == 0:
        unit_prices = [0]*len(descriptions)

    for i, description in enumerate(descriptions):
        print(f"{i}. {descriptions[i]}:\n    Quantity: {quantities[i]}\n    Unit Price: {unit_prices[i]}\n")
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
    try:
        driver.find_elements(by="name", value="action")[2].click()
    except:
        pass
    time.sleep(1)
    try:
        driver.find_element(by="id", value="btnAllowParallelLogin").click()
        time.sleep(1)
    except:
        pass
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

    for i, description in enumerate(descriptions):
        if description == 'Keg Deposit':
            continue
        WebDriverWait(driver, 3).until(lambda driver: driver.find_element(by="id", value="DivAddLineItem"))
        driver.find_element(by="id", value="DivAddLineItem").click()
        time.sleep(1)
        try:
            row = driver.find_element(by="id", value=f"{i}")
        except:
            driver.find_element(by="id", value="DivAddLineItem").click()
            time.sleep(1)
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
    print("--- Inventory finished in %s seconds ---" % round((time.time() - start_time), 3))
else:
    print("Try taking another screenshot and inputting the image again. sowwy :(")
