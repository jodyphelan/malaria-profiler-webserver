from celery import Celery
from flask import Flask,current_app,url_for
import subprocess as sp



def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


flask_app = Flask(__name__)
flask_app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379',
)
celery = make_celery(flask_app)

@celery.task
def run_task(fq1,fq2,run_id,result_dir):
    if fq2:
        sp.call(f"malaria-profiler profile -1 {fq1} -2 {fq2} --prefix {run_id} --dir {result_dir} 2> {result_dir}/{run_id}.log",shell=True)
    else:
        sp.call(f"malaria-profiler profile -1 {fq1} --prefix {run_id} --dir {result_dir} 2> {result_dir}/{run_id}.log",shell=True)
