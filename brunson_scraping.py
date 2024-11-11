import requests
from bs4 import BeautifulSoup 
import pandas as pd
import sqlite3
from datetime import datetime
import logging
import os
import schedule
import time


def setup_logging():
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = f'logs/nba_scraper_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log'

    logging.basicConfig(level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[
                        logging.FileHandler(log_file), 
                        logging.StreamHandler()
                    ]
                    )
    return logging.getLogger(__name__)