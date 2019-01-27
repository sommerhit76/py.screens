import re

from Classes.output import Output
from Classes.color import Color


class Page:
    viewports = {375, 768, 1024, 1400}
    num_total_screenshots = 0
    num_zpadding = 0

    def __init__(self, url, folder_website):
        self.url = url
        self.folder_website = folder_website

    def take_screenshot(
        self,
        counter,
        driver,
        slug,
        selenium
    ):
        for viewport in self.viewports:
            slug_cleaned = re.sub(
                r"[/%?=&_\[\]]",
                "-",
                slug[1:]
            )

            # change slug in case of home page
            if slug_cleaned == '-':
                slug_cleaned = ''

            if self.num_total_screenshots >= 10:
                self.num_zpadding = 2
            elif self.num_total_screenshots >= 100:
                self.num_zpadding = 3

            file_name = str(counter).zfill(self.num_zpadding) \
                        + '__w' \
                        + str(viewport).zfill(4) \
                        + '__' \
                        + slug_cleaned
            file_name = file_name.rstrip('_') + '.png'
            print(file_name, end=' ', flush=True)

            # open web page
            driver.set_window_size(viewport, 400)
            driver.get(self.url + slug)
            required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
            driver.set_window_size(viewport, required_height)

            # make some Selenium magic
            if selenium:
                locator_mode, locator_value = selenium['locator'].split('=')
                if locator_mode == 'class':
                    driver.find_element_by_class_name(locator_value).click()
                elif locator_mode == 'id':
                    driver.find_element_by_id(locator_value).click()
                else:
                    Output.print(
                        Output.MSG_ERROR,
                        'locator mode `' + locator_mode + '` not defined, please use `class` or `id`'
                    )
                    driver.quit()
                    exit(1)

            if driver.save_screenshot('output/' + self.folder_website + '/' + file_name):
                color = Color.OKGREEN
            else:
                color = Color.FAIL

            print(color + '📷' + Color.ENDC)
