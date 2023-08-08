# Batch Code Checker

This repo is designed for checking(tracking) the production date of cosmetics products

## Installation
Clone the repository to your local machine or download the zip file.
```bash
git clone https://github.com/LittleFish-Coder/batch-code-checker.git
```

## Packages
The packages are listed in the requirements.txt file: 
- pandas==2.0.2
- selenium==4.10.0
- openpyxl==3.1.2
- jinja2==3.1.2
- unidecode==1.3.6

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the packages.
```bash
pip install -r requirements.txt
```
Or use pip3 depending on your python version
```bash
pip3 install -r requirements.txt
```

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
