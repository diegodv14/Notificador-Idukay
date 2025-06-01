import os
import time
from typing import Any, Dict, List
from playwright.sync_api import sync_playwright
from playwright.sync_api import Page
from src.web.core.log.logger import logger
import polars as pl
from src.web.constants.paths import ERROR_LOGIN, INPUT_TEXT_PASSWORD, INPUT_TEXT_USER, LOGIN_BUTTON, PARCIAL_NOTES
from src.web.domain.interfaces.notification_repository import INotificationRepository
from src.web.domain.types.index import NoteEntry
from web.infraestructure.services.dataframe_service import DataFrameService
from web.infraestructure.services.evaluation_service import EvaluationService

class Job:
    _notification_repository: INotificationRepository = None
    listStudents: list = []
    notes: List[NoteEntry] = []
    
    def __init__(self, notification: INotificationRepository):
        self._notification_repository = notification

    def run(self) -> None:
        logger.info("Iniciando el job de scraping...")
        url = os.getenv("URL_PLATFORM")
        if not url:
            logger.error("La URL no está definida en las variables de entorno.")
            return

        try:
            with sync_playwright() as pw:
                browser = pw.firefox.launch(headless=False)
                page = browser.new_page()
                page.goto(url)
                logger.info(f"Navegando a la URL: {url}")

                time.sleep(2)
                if not self.login(page):
                    logger.error("Login fallido. El proceso se detiene.")
                    page.close()
                    browser.close()
                    return

                time.sleep(6)

                if not self.get_students(page):
                    logger.error("No se pudieron obtener los estudiantes.")
                else:
                    logger.info(f"Estudiantes obtenidos: {self.listStudents}")
                    
                time.sleep(2)
                
                for index, student in enumerate(self.listStudents):
                    # Dropdown de estudiantes
                    students_options = page.locator("li[ng-if='is_parent'].open ul.user-menu")
                    
                    if not students_options.is_visible():
                        self.open_dropdown(page)
                        time.sleep(7)
                    
                    self.go_to_student(page, student)
                    self.notes.append({"student": student, "notes": []})
                    
                    time.sleep(5)
                    sidebar_notes = page.locator(PARCIAL_NOTES)
                    
                    if not sidebar_notes.is_visible():
                        logger.error(f"No se encontró el botón de notas parciales para el estudiante: {student}")
                        continue
                    
                    sidebar_notes.click()
                    
                    time.sleep(6)
                    
                    has_topic = self.get_topics(page, index)
                    if not has_topic:
                        logger.error(f"No se encontraron materias para el estudiante: {student}")
                        continue
                    
                    time.sleep(2)
                            
                    self.get_notes(page, index)
                    

                df = DataFrameService.create_dataframe(self.notes)  
                df = df.filter(pl.col("Nota") != "-")
                df.write_csv("notas_estudiantes.csv")
                
                filter_df = EvaluationService.get_bad_notes(df)
                        
                if not filter_df.is_empty():
                    logger.info("Se encontraron notas bajas. Enviando notificación...")
                    self._notification_repository.send_notification(
                        data=filter_df
                    )

                page.close()
                browser.close()
                pw.stop()
                logger.info("Job de scraping completado exitosamente.")

        except Exception as e:
            logger.error(f"Ocurrió un error en el job: {e}")
            
    
    def login(self, page: Page) -> bool:
        try:
            logger.info("Iniciando sesión...")

            input_user = page.locator(INPUT_TEXT_USER)
            input_user.fill(os.getenv("IDUKAY_USERNAME"))

            input_password = page.locator(INPUT_TEXT_PASSWORD)
            input_password.fill(os.getenv("IDUKAY_PASSWORD"))

            login_button = page.locator(LOGIN_BUTTON)
            login_button.click()

            time.sleep(3)

            try:
                error_element = page.locator(ERROR_LOGIN)
                if error_element.is_visible():
                    error_message = error_element.inner_text()
                    logger.error(f"Error al iniciar sesión: {error_message}")
                    return False
            except:
                pass

            logger.info("Inicio de sesión exitoso.")
            return True

        except Exception as e:
            logger.error(f"Ocurrió un error al iniciar sesión: {e}")
            return False
        
        
    
    def open_dropdown(self, page: Page) -> bool:
        try:
            logger.info("Buscando botón del dropdown de estudiantes...")

            popover_button = page.locator("li[ng-if='is_parent'] a[data-toggle='dropdown']")

            if not popover_button.is_visible():
                logger.error("No se encontró el botón para desplegar estudiantes.")
                return False

            popover_button.click()
            logger.info("Se hizo clic en el botón del dropdown.")

            try:
                page.wait_for_function(
                    "el => el.closest('li').classList.contains('open')",
                    popover_button,
                    timeout=3000
                )
                logger.info("El dropdown se abrió correctamente.")
            except Exception:
                logger.warning("El dropdown no se abrió automáticamente. Se intentará forzar apertura.")
                element_handle = popover_button.element_handle()
                if element_handle is None:
                    logger.error("No se pudo obtener el elemento para forzar apertura.")
                    return False
                page.evaluate("el => el.closest('li').classList.add('open')", element_handle)
        
        except Exception as e:
            logger.error(f"Ocurrió un error al abrir el dropdown: {e}")
            return False


        
    def get_students(self, page: Page) -> bool:
        try:
            
            self.open_dropdown(page)
            students_options = page.locator("li[ng-if='is_parent'].open ul.user-menu li a")
            count = students_options.count()

            if count == 0:
                logger.warning("No se encontraron estudiantes en la lista.")
                return False

            self.listStudents = []
            for i in range(count):
                item = students_options.nth(i)
                text = item.inner_text().strip()
                self.listStudents.append(text)

            return True

        except Exception as e:
            logger.error(f"Ocurrió un error al obtener los usuarios: {e}")
            return False
        
        
        
    def go_to_student(self, page: Page, student: str) -> bool:
        try:
            logger.info(f"Navegando al estudiante: {student}")
            students_options = page.locator("li[ng-if='is_parent'].open ul.user-menu li a")
            count = students_options.count()

            for i in range(count):
                item = students_options.nth(i)
                text = item.inner_text().strip()
                if text == student:
                    item.click()
                    logger.info(f"Se hizo clic en el estudiante: {student}")
                    return True

            logger.warning(f"No se encontró el estudiante: {student}")
            return False

        except Exception as e:
            logger.error(f"Ocurrió un error al navegar al estudiante: {e}")
            return 
        
    
    def get_topics(self, page: Page, index: int) -> bool:
        try:
            logger.info("Obteniendo materias...")
            topics = page.locator(".pricing-span-header .widget-box .widget-body .widget-main ul li.ng-scope")
            if topics.count() == 0:
                logger.error("No se encontraron las materias.")
                return False

            count = topics.count()
            logger.info(f"Cantidad de materias encontrados: {count}")

            for i in range(count):
                topic = topics.nth(i).inner_text().strip()
                self.notes[index]["notes"].append({"topic": topic, "note": []})
                
            return True

        except Exception as e:
            logger.error(f"Ocurrió un error al obtener los temas: {e}")
            return False
    
    
    
    def get_notes(self, page: Page, index: int) -> bool:
        
        try: 
            logger.info("Obteniendo notas parciales...")
            notes_table = page.locator(".pricing-span-body")
            if not notes_table.is_visible():
                logger.error("No se encontró la tabla de notas.")
                return False

            cols = notes_table.locator(".pricing-span.courses-table")
            logger.info(f"Cantidad de columnas encontradas: {cols.count()}")
            count = cols.count()
            
            for i in range(count):
                col = cols.nth(i)
                
                title = col.locator(".widget-box .widget-header .courses-table-title div").inner_text().strip()
                
                rows = col.locator(".widget-box .widget-body .widget-main ul li.ng-scope")
                rows_count = rows.count()
                logger.info(f"Cantidad de filas encontradas en la columna {title}: {rows_count}")
                
                for j in range(rows_count):
                    row = rows.nth(j)
                    note = row.locator("span").inner_text().strip()           
                    self.notes[index]["notes"][j]["note"].append({"type": title, "note": note})
            
            return True
        
        
        except Exception as e:
            logger.error(f"Ocurrió un error al obtener las notas: {e}")
            return False


