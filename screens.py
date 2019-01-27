#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import argparse
import json
import shutil

from selenium import webdriver
from Classes.output import Output
from Classes.file_system import FileSystem
from Classes.page import Page


# set variables
pages = {}

# parse command line args
parser = argparse.ArgumentParser(description='Take screenshots of a website in different viewport widths.')
parser.add_argument(
    '-c',
    '--config',
    metavar='',
    type=str,
    required=True,
    help='name of configuration file'
)

args = parser.parse_args()


def start_webdriver():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('log-level=2')

    return webdriver.Chrome(options=options)


def process_data():
    """
    iterate through dict `pages` to take screenshots
    :return:
    """
    driver = start_webdriver()
    counter = 1

    for page in pages:
        if 'ignore' in page and page['ignore'] is True:
            continue

        selenium = {}
        if 'selenium' in page:
            selenium = {
                "locator": page['selenium']['locator']
            }

        webpage = Page(url, folder_website)
        webpage.take_screenshot(
            counter,
            driver,
            page['slug'],
            selenium
        )

        counter += 1

    driver.quit()


def init():
    # check if configuration file is present
    if not os.path.isfile(args.config):
        Output.print(
            Output.MSG_ERROR,
            'the configuration file `' + args.config + '` could not be found'
        )
        exit(1)

    # read configuration file
    global pages, url
    with open(args.config) as json_data_file:
        data = json.load(json_data_file)

    pages = data['pages']
    url = data['url']

    # build folder structure
    global folder_website
    folder_website = FileSystem.build_folder_name(url)

    if not os.path.isdir('output'):
        FileSystem.create_folder('output')
    if os.path.isdir('output/' + folder_website):
        shutil.rmtree('output/' + folder_website)
    FileSystem.create_folder('output/' + folder_website)


def main():
    print()
    init()
    process_data()


if __name__ == '__main__':
    main()
