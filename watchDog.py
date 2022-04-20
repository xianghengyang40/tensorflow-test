import psutil
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from time import sleep
import threading

class WatchDog(object):
    """
    The run method watch if there is any hanging process (in sleeping status, 0 cpu usage),
    The run() method will be started and it will run in the background
    until the application exits.
    """
    def __init__(self, interval=1):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def kill_hanging_process(self, pid):
        p = psutil.Process(pid)
        if p.status() is 'sleeping' and p.name is 'python' and pid >1:
            print (p.name(), p.status(), pid)
            cpu_percent = p.cpu_percent(interval=10.0)
            if cpu_percent == 0.0 and p.name() is 'python':
                print ("kill process {}".format(pid))
                p.terminate()
                p.kill()
                p.wait(timeout=3)

    def run(self):
        """ Method that runs forever """
        while True:
            print('Check and kill hanging process in the background')
            pids = psutil.pids()
            for pid in pids:
              try:
                p = psutil.Process(pid)
                if p.status() is 'sleeping' and 'runner.py' in p.cmdline() and pid >1:
                    cpu_percent = p.cpu_percent(interval=1.0)
                    print (p.name(), p.status(), pid,cpu_percent)
                    if cpu_percent == 0.0:
                        print ("kill process {}".format(pid))
                        p.terminate()
                        p.kill()
              except Exception as e:
                    print(e.message)
              else:
                    continue

            sleep(3.0)


def get_parser():

    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", "--interval",
                        dest="interval",
                        help="time interval to collect cpu percentage", default=None)
    return parser

if __name__ == "__main__":
    args = get_parser().parse_args()
    interval = args.interval
    example = WatchDog(interval)
    while True:
         pass
