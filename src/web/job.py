import os
import time
from playwright.sync_api import sync_playwright
from playwright.sync_api import Page
from src.web.core.log.logger import logger
from src.web.constants.paths import ERROR_LOGIN, INPUT_TEXT_PASSWORD, INPUT_TEXT_USER, LOGIN_BUTTON
from src.web.domain.interfaces.notification_repository import INotificationRepository

class Job:
    _notification_repository: INotificationRepository = None
    
    def __init__(self, notification: INotificationRepository):
        self._notification_repository = notification

    def run(self) -> None:
        logger.info("Iniciando el job de scraping...")
        url = os.getenv("URL_PLATFORM")
        if not url:
            raise ValueError("La URL no está definida.")

        try:
            with sync_playwright() as pw:
                browser = pw.firefox.launch(headless=False)
                page = browser.new_page()
                page.goto(url)
                
                logger.info(f"Navegando a la URL: {url}")
                time.sleep(2)
                self.login(page)

                page.close()
                browser.close()
                pw.stop()
                logger.info("Job de scraping completado exitosamente.")

        except Exception as e:
            logger.error(f"Ocurrió un error en el job: {e}")

            
    
    def login(self, page: Page):
        try:
            logger.info("Iniciando sesión...")
            
            input_user = page.locator(INPUT_TEXT_USER)
            input_user.fill(os.getenv("IDUKAY_USERNAME"))
            
            input_password = page.locator(INPUT_TEXT_PASSWORD)
            input_password.fill(os.getenv("IDUKAY_PASSWORD"))
            
            logger.info(f"Llenando los campos de usuario y contraseña...{os.getenv("IDUKAY_USERNAME")} {os.getenv("IDUKAY_PASSWORD")}")
            
            login_button = page.locator(LOGIN_BUTTON)
            login_button.click()
            
            time.sleep(3) 
            
            is_error = page.locator(ERROR_LOGIN).wait_for(state="visible")
            
            if is_error:
                page.locator(ERROR_LOGIN).wait_for(state="visible", timeout=3000)
                error_message = page.locator(ERROR_LOGIN).inner_text()
                logger.error(f"Error al iniciar sesión: {error_message}")
                raise SystemExit(1) 

            time.sleep(6)
            
            pass
        except Exception as e:
            logger.error(f"Ocurrió un error al iniciar sesión: {e}")
