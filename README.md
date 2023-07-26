# Batch Code Checker

This repo is designed for checking(tracking) the production date of cosmetics products

## Packages
- pandas
- Selenium
- openpyxl
- Jinja2

use the commands below to install the packages
```bash
pip install -r requirements.txt
```

## Attention:
Make sure you have already downloaded the webdriver before you use the program.
There are 4 different webdrivers to select:
- [Chrome](https://chromedriver.chromium.org/downloads)
- [Edge](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)
- [Firefox](https://github.com/mozilla/geckodriver/releases)
- [Safari](https://webkit.org/blog/6900/webdriver-support-in-safari-10/)

Follow the instruction to download the webdriver and read the documentation based on your chosen webdriver.
In this program, I use Safari as an example.
Make sure you turn on the remote automation in Safari.

To Enable Remote Automation in Safari:
    - Open Safari
    - Go to Safari > Preferences > Advanced
    - Check "Show Develop menu in menu bar"
    - Go to Develop > Allow Remote Automation

![settings](./img/img1.png)
![Show Develop menu in menu bar](./img/img2.png)
![Allow Remote Automation](./img/img3.png)
