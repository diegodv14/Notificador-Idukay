import os
from playwright.sync_api import sync_playwright

from src.web.core.log.logger import logger


def job():
    pw = sync_playwright().start()
    try:
        logger.info("Iniciando el job de scraping...")
        url = os.getenv("URL_PLATFORM") 
        if not url:
            raise ValueError("La url no esta definida.")
        
        chrome = pw.firefox.launch(headless=False)
        page = chrome.new_page()
        page.goto(url)
    
    except Exception as e:
        logger.error(f"Ocurrió un error durante el job de scraping: {e}")
    finally:
        pw.stop()