#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import errno
import argparse
import shutil
import re

from selenium import webdriver


class Color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# set variables
counter = 1
viewports = {375, 768, 1024, 1400}
folder_website = ''
num_total_screenshots = 0
num_zpadding = 1

# parse command line args
parser = argparse.ArgumentParser(description='Take screenshots of a website in different viewport widths.')
parser.add_argument(
    '-b',
    '--base',
    metavar='',
    type=str,
    required=True,
    help='base url, e. g. https://www.google.at (without ending "/")'
)
parser.add_argument(
    '-p',
    '--pages',
    metavar='',
    type=str,
    required=True,
    help='name of text file containing the webpages (`pages*.txt`)'
)

args = parser.parse_args()


def take_screenshot(driver, slug, locator):
    global counter

    for viewport in viewports:
        slug_cleaned = re.sub(
            r"[/%?=&_\[\]]",
            "-",
            slug[1:]
        )

        # change slug in case of home page
        if slug_cleaned == '-':
            slug_cleaned = ''

        global num_zpadding
        if num_total_screenshots >= 10:
            num_zpadding = 2
        elif num_total_screenshots >= 100:
            num_zpadding = 3

        file_name = str(counter).zfill(num_zpadding) \
                    + '__w' \
                    + str(viewport).zfill(4) \
                    + '__' \
                    + slug_cleaned
        file_name = file_name.rstrip('_') + '.png'
        print(file_name, end=' ', flush=True)

        # open web page
        driver.set_window_size(viewport, 400)
        driver.get(args.base + slug)
        required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
        driver.set_window_size(viewport, required_height)

        # make some Selenium magic
        if locator != '':
            locator_mode, locator_value = locator.split('=')
            driver.find_element_by_class_name(locator_value).click()

        if driver.save_screenshot('output/' + folder_website + '/' + file_name):
            color = Color.OKGREEN
        else:
            color = Color.FAIL

        print(color + '📷' + Color.ENDC)

    counter += 1


def create_folder(name):
    try:
        os.makedirs(name)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def start_webdriver():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('log-level=2')

    return webdriver.Chrome(options=options)


def stop_webdriver(driver):
    driver.quit()


def process_data(driver):
    f = open(args.pages)

    # calculate maximum number of screenshots
    global num_total_screenshots
    num_total_screenshots = sum(1 for line in f)

    f.seek(0)
    for line in f:
        line = line.strip()
        if line[0:1] == '#' or line[0:1] == ' ':
            continue

        # extract Selenium action
        if ';' in line:
            slug, locator = line.split(';')
        else:
            slug = line
            locator = ''

        take_screenshot(driver, slug, locator)

    f.close()


def build_folder_name(base):
    if '@' in base:
        auth, url = base.split('@')
    else:
        url = re.sub(
            "http[s]?://",
            "",
            base
        )

    url = re.sub(
        r"[/]",
        "-",
        url
    )

    return url


def main():
    print()

    # check if the parameters are correct
    if not os.path.isfile(args.pages):
        print(
            Color.FAIL + '[ERROR]' + Color.ENDC
            + ' The file `' + args.pages + '` could not be found'
        )
        exit(1)

    # build folder structure
    global folder_website
    folder_website = build_folder_name(args.base)

    if not os.path.isdir('output'):
        create_folder('output')
    if os.path.isdir('output/' + folder_website):
        shutil.rmtree('output/' + folder_website)
    create_folder('output/' + folder_website)

    driver = start_webdriver()
    process_data(driver)
    stop_webdriver(driver)


if __name__ == '__main__':
    main()
