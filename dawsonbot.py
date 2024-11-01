import os
import cv2
import pytesseract
import argparse
import time

from PIL import Image
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

start_time = time.time()

email = ""
pw = ""

print("\033[32;5mDawsonbot intializing...\033[0m\n")
time.sleep(2)


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help="SalesOrder_img.png")
ap.add_argument("-a", "--all", action='store_true', help="All images in directory")

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

def read_img(image_filename=None):
    """ Read image and convert to text """
    if image_filename is None:
        image = cv2.imread(args.image)
    else:
        image = cv2.imread(image_filename)

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

    for i, line in enumerate(lines):
        if line == '':
            lines.pop(i)
        if "Item" in line:
            lines.pop(i)
        if line == "Price":
            lines.pop(i)
        if line == "Discount":
            lines.pop(i)

    for i, line in enumerate(lines):
        if line == '':
            lines.pop(i)
        if "Item" in line:
            lines.pop(i)
        if line == "Price":
            lines.pop(i)
        if line == "Discount":
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

    for i, line in enumerate(lines):
        if "Quantity" in line:
            quantities = lines[i+1:i+count+1]

        if "Unit" in line:
            unit_prices = lines[i+1:i+count+1]

    print(f"--- Array Length: {len(descriptions)}, {len(quantities)}, {len(unit_prices)} ---")

    if len(quantities) == 0:
        quantities = [0]*len(descriptions)
    else:
        for i, quantity in enumerate(quantities):
            quantities[i] = quantity.split(" ")[0]
    if len(unit_prices) == 0:
        unit_prices = [0]*len(descriptions)
    else:
        for i, unit_price in enumerate(unit_prices):
            unit_prices[i] = unit_price.split(" ")[0]

    for i, description in enumerate(descriptions):
        print(f"{i}. {descriptions[i]}:\n    Quantity: {quantities[i]}\n    Unit Price: {unit_prices[i]}\n")
    return descriptions, quantities, unit_prices


def login():
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
    try:
        driver.find_element(by="id", value="select2-roleId-container").click()
        driver.find_element(By.CLASS_NAME, value="select2-search__field").click()
        driver.find_element(By.CLASS_NAME, value="select2-search__field").send_keys(Keys.DOWN)
        driver.find_element(By.CLASS_NAME, value="select2-search__field").send_keys(Keys.DOWN)
        driver.find_element(By.CLASS_NAME, value="select2-search__field").send_keys(Keys.ENTER)
        driver.find_element(by="id", value="btnSelect").click()
        time.sleep(1)
    except:
        pass
    return driver


def input_inventory(descriptions, quantities, unit_prices, driver=None):
    """ Selenium script to login to website and input inventory """
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
        if 'Keg Deposit' in description:
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
        row.find_element(by="id", value=f"ItemDescription_{i}").send_keys(description[:23])
        time.sleep(1)
        row.find_element(by="id", value=f"ItemDescription_{i}").send_keys(Keys.DOWN)
        row.find_element(by="id", value=f"ItemDescription_{i}").send_keys(Keys.ENTER)
        row.find_element(by="id", value=f"Qty_{i}").send_keys(quantities[i])
        row.find_element(by="id", value=f"UnitPrice_{i}").send_keys(Keys.CONTROL + "a")
        row.find_element(by="id", value=f"UnitPrice_{i}").send_keys(Keys.DELETE)
        row.find_element(by="id", value=f"UnitPrice_{i}").send_keys(unit_prices[i])

    return

# construct the argument parser and parse the arguments
args = ap.parse_args()

# If all images selected, loop through the images and process them, else process for the selected image
if args.all:
    images = []
    for image in os.listdir("fixed_pngs"):
        if image.endswith(".png"):
            images.append(image)

    skipped_files = []
    completed_files = []
    for i, image in enumerate(images):
        lines = read_img(f"fixed_pngs/{image}")
        descriptions, quantities, unit_prices = process_lines(lines)
        print(f"--- Iteration {i+1} ---")
        text = input(f"Table processed for '{image}'. Does this look right? y/n\n")
        if text == 'y':
            if i == 0:
                driver = login()
            input_inventory(descriptions, quantities, unit_prices, driver)
            completed_files.append(image)
        else:
            print(f"Skipping '{image}' and moving on to the next file.")
            skipped_files.append(image)

    print("--- End of List ---")
    if completed_files:
        print(f"Completed files: {completed_files}")
    if skipped_files:
        print(f"Skipped files: {skipped_files}")
    else:
        print("No files skipped!")
    print("Inventory finished in %s seconds" % round((time.time() - start_time), 3))
    print("Dawsonbot shutting down...")

else:
    lines = read_img()
    descriptions, quantities, unit_prices = process_lines(lines)
    text = input(f"Table processed for '{args.image}'. Does this look right? y/n\n")
    if text == 'y':
        driver = login()
        input_inventory(descriptions, quantities, unit_prices, driver)
        print("--- Inventory finished in %s seconds ---" % round((time.time() - start_time), 3))
    else:
        print("Try taking another screenshot and inputting the image again. sowwy :(")
        print("Dawsonbot shutting down...")
