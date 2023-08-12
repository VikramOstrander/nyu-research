author: Vikram Ostrander
date: 6-16-2023

scrapy is a asyncronous api for building web crawlers with python
scrapy was used to efficiently scrape data from healthgrades.com to compile doctors.csv
note: this project was made with scrapy version 2.6.0

getting started with scrapy
    note: scrapy recommends installation in a dedicated virtual environment
    install scrapy with "pip install Scrapy"
    make a project with "scrapy startproject [project_name]"

setup
    replace settings.py with the supplied settings.py
    move scrape_manager.py into the main project directory
    move spider.py into the spiders folder

usage
    run with "py scrape_manager.py"
    change the starting index by editing START in scrape_manager.py

------------

files
    scrape_manager.py:      python script to run healthgrades_spider in intervals to avoid ip blocking
    settings.py:            custom settings for healthgrades_spider scrapy project
    spider.py:              spider class for healthgrades scrapy project  
