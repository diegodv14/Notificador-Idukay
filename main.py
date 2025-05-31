from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from src.web.core.log.logger import logger
from src.web.core.container import container
from src.web.job import Job

from dotenv import load_dotenv

load_dotenv()

def start_job():
    notification_service = container.notification_service()
    job_instance = Job(notification_service)
    job_instance.run()
    

def main(): 
    logger.info("Iniciando el job de scraping...")
    scheduler = BlockingScheduler()
    scheduler.add_job(start_job, IntervalTrigger(seconds=10), id='job_scraping')
    
    logger.info("Scheduler iniciado. Esperando ejecuciones...")
    scheduler.start()

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        logger.warning("[Info]: Scheduler detenido por el usuario.")
