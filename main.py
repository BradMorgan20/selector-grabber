from bs4 import BeautifulSoup
from requests import get
import sys
import fileinput
from _datetime import datetime

"""
Script to automatically generate selectors for use in Python automation.

This will try to retrieve all the locators required on the page. This may not work with virtual doms (i.e. Vue.js)

Created by Bradderz96 
"""

if len(sys.argv) < 1:
    print("Not enough arguments!")
else:
    url = "http://192.168.0.68:8000"
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    body_cols = html_soup.find_all('div', class_='body-col')
    text_input = html_soup.find_all("input", type="text")
    checkboxes = html_soup.find_all("input", type="checkbox")

    checkbox_names = []
    checkbox_elements = dict()
    name_counter = 1
    loop_counter = 1

    """
    Get the id first, then get the next best thing.
    """
    for checkbox in checkboxes:
        name_exists = False
        checkbox_name = ""
        if loop_counter == 1:
            checkbox_names.append(checkbox.get('name'))
        elif loop_counter != 1:
            while not name_exists:
                for name in checkbox_names:
                    if checkbox.get('name') == name:
                        checkbox_name = f"{checkbox.get('name')}-{name_counter}"
                        checkbox_names.append(checkbox_name)
                        name_counter = name_counter + 1
                        name_exists = True
                        break

                break

        if not name_exists:
            checkbox_name = checkbox.get('name')
            checkbox_names.append(checkbox_name)

        if len(checkbox.get('id')) > 0:
            checkbox_elements[f"cb{checkbox_name}"] = checkbox.get('id')
        elif len(checkbox.get('name')) > 0:
            checkbox_elements[f"cb{checkbox_name}"] = checkbox.get('name')

        loop_counter = loop_counter + 1

    datetime = datetime.now()
    formatted = datetime.strftime("%m_%d_%Y-%H_%M_%S") + "-test.py"
    bob = open(formatted, "w+")

    for key, value in checkbox_elements.items():
        bob.write(f"{key}={value}\n")

    bob.close()
