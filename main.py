from datetime import datetime

from flask import Flask
from flask_apscheduler import APScheduler

import HackerNewsAPI

_cache = {}
ENDPOINT_1 = 'endpoint_1_data'
ENDPOINT_2 = 'endpoint_2_data'
ENDPOINT_3 = 'endpoint_3_data'
class SchedulerConfig:
    SCHEDULER_API_ENABLED = False


app = Flask("Hacker News API")
app.config.from_object(SchedulerConfig())

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()


@scheduler.task("interval", id="endpoint_1_job", next_run_time=datetime.now(), seconds=30, misfire_grace_time=900, coalesce=True, max_instances=1)
def endpoint_1_job():
    print("Job for endpoint 1 executed")
    result = HackerNewsAPI.endpoint_1()
    with scheduler.app.app_context():
      _cache[ENDPOINT_1] = result
    print("Job for endpoint 1 finished.")

@scheduler.task("interval", id="endpoint_2_job", next_run_time=datetime.now(), seconds=30, misfire_grace_time=900, coalesce=True, max_instances=1)
def endpoint_2_job():
    print("Job for endpoint 2 exeuted")
    result = HackerNewsAPI.endpoint_2()
    with scheduler.app.app_context():
      _cache[ENDPOINT_2] = result
    print("Job for endpoint 2 finished.")

@scheduler.task("interval", id="endpoint_3_job", next_run_time=datetime.now(), seconds=30, misfire_grace_time=900, coalesce=True, max_instances=1)
def endpoint_3_job():
    print("Job for endpoint 3 exeuted")
    result = HackerNewsAPI.endpoint_3()
    with scheduler.app.app_context():
      _cache[ENDPOINT_3] = result
    print("Job for endpoint 3 finished.")


@app.route("/hello")
def hello():
    return "Hello!!"

@app.route("/endpoint_1")
def endpoint_1():
    if ENDPOINT_1 in _cache:
      return _cache[ENDPOINT_1]
    else:
      return "Endpoint 1: Data is still being fetched. Please try later.", 503

@app.route("/endpoint_2")
def endpoint_2():
    if ENDPOINT_2 in _cache:
      return _cache[ENDPOINT_2]
    else:
      return "Endpoint 2: Data is still being fetched. Please try later.", 503

@app.route("/endpoint_3")
def endpoint_3():
    if ENDPOINT_3 in _cache:
      return _cache[ENDPOINT_3]
    else:
      return "Endpoint 3: Data is still being fetched. Please try later.", 503

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000)
