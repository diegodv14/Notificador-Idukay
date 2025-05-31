from apscheduler.schedulers.blocking import BlockingScheduler
from src.web.job import job
from apscheduler.triggers.interval import IntervalTrigger
from src.web.core.log.logger import logger


def main(): 
    logger.info("Iniciando el job de scraping...")
    scheduler = BlockingScheduler()
    scheduler.add_job(job, IntervalTrigger(seconds=10), id='job_scraping')
    
    logger.info("Scheduler iniciado. Esperando ejecuciones...")
    scheduler.start()

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        logger.warning("[Info]: Scheduler detenido por el usuario.")
