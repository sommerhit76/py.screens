# py.screens

Take screenshots of a website in different viewport widths.

## Prerequisites

* Python >= 3.6.4
* ChromeDriver
* Selenium WebDriver

```
pip install selenium
```

## Installing

### Configuration

The configuration is saved in a file called `pages--myconfig.json`.

```
{
    "url": "https://user:password@www.website.com",
    "pages": [
        {
            "slug": "/"
        },
        {
            "slug": "/faqs"
        },
        {
            "slug": "/faqs",
            "selenium": {
                "locator": "class=js-open-accordion",
                "action": "click"
            }
        }
    ]
}
```

```
# show help
screens.py -h

# run
screens.py -c pages--myconfig.json
```

## Authors

* **Stefan Franke** - *Initial work* - [sommerhit76](https://github.com/sommerhit76)

See also the list of [contributors](https://github.com/sommerhit76/py.screens/contributors) who participated in this project.

## License

This project is licensed under the GPLv3 License – see the [LICENSE](LICENSE) file for details
