import time

from celery import Celery
from core.services.site_validator import SiteValidator
from core.database.site import SiteDB
from core.schemas.site import Status, SiteUpdateSchemas
from core.services.redis_client.site import set_site_status, set_site_time_end, set_site_time_start
from core.services.site_validator import PdfParser

BROKER_URL = 'redis://redis:6379/1'
BACKEND_URL = 'redis://redis:6379/1'

celery = Celery('site_task', broker=BROKER_URL, backend=BACKEND_URL)
celery.conf.update(
    broker_connection_retry_on_startup=True
)

site_db = SiteDB()

@celery.task(bind=True, max_retries=3, ignore_result=True)
def pdf_pars_mistral(self, pdf: PdfParser):
    try:
        pdf.run_with_mistral()
        return True
    except Exception as e:
        raise self.retry(exc=e)

@celery.task(bind=True, max_retries=3, ignore_result=True)
def pdf_pars(self, pdf_path: str):
    try:
        pdf = PdfParser(pdf_path)
        pdf.run()
        pdf.run_with_mistral()
        return True
    except Exception as e:
        raise self.retry(exc=e)


@celery.task(bind=True, max_retries=3, ignore_result=True)
def do_pars(self, url: str):
    try:
        set_site_time_start(url, time.time())
        site_db.update_sync(url, SiteUpdateSchemas(**{"time_start": time.time()}))

        sv = SiteValidator(url)
        set_site_status(url, Status.parsing_1)
        site_db.update_sync(url, SiteUpdateSchemas(**{"status": Status.parsing_1.value}))
        sv.check_rule_1()

        set_site_status(url, Status.parsing_2)
        site_db.update_sync(url, SiteUpdateSchemas(**{"status": Status.parsing_2.value}))
        sv.check_rule_2()

        set_site_status(url, Status.ok)
        site_db.update_sync(url, SiteUpdateSchemas(**{"status": Status.ok.value}))

        set_site_time_end(url, time.time())
        site_db.update_sync(url, SiteUpdateSchemas(**{"time_end": time.time()}))
        return True
    except Exception as e:
        raise self.retry(exc=e)
