import os
from collections import namedtuple

from apscheduler.schedulers.background import BackgroundScheduler

class Daemon:
    path = os.getcwd() + 'lib/drone_hangar/static'

    def __init__(self):
        self.scheduler = BackgroundScheduler()

    def start_job(self, wrapped):
        # Pass a function to this method to instruct the Daemon on a new job.
        pass

    def storage_path(self, uri):
        check = ''
        p_list = self.path.split('/')

        p_len = len(p_list)

        while p_len != 0:
            check = '/'.join([p_list[p_len - 1], check])
            if os.path.exists(check):
                result = os.path.join(check, uri)
                print(
                    ' '.join([
                        '>>> Storage file populated at', result
                        ])
                )
                return result

            p_len = p_len - 1

        return os.path.abspath(result)
