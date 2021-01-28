import os
from collections import namedtuple


class Daemon:
    # The ur-class at the root of all Daemon activity.
    path = os.getcwd() + 'lib/drone_hangar/static'

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
