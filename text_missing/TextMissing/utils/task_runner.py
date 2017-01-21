from time import sleep

from datetime import datetime


class RepeatedTaskRunner:
    @staticmethod
    def run_task(task, timeout_seconds, params=None):
        while True:
            if params:
                task(*params)
            else:
                task()
            print("Ran task at", datetime.now(), "waiting", timeout_seconds, "seconds...")
            sleep(timeout_seconds)

# example
RepeatedTaskRunner.run_task(print, 5, ("Task", "with", "params"))
