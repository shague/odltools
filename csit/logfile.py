import os
from subprocess import Popen


class LogFile():
    TMP = "/tmp"
    LOGFILE = "log.html"

    def __init__(self, logpath, jobpath, job):
        if jobpath is None:
            jobpath = self.TMP
        self.jobpath = "{}/{}".format(jobpath, job)
        self.logpath = logpath

    def unzip_log_file0(self):
        Popen("gunzip -fk {}".format(self.logpath), shell=True).wait()

    def unzip_log_file1(self):
        Popen("gunzip -kc {} > {}".format(self.logpath, self.jobpath + "/log.html"), shell=True).wait()

    def unzip_log_file(self):
        Popen("gunzip -cfk {} > {}".format(self.logpath, self.jobpath + "/" + self.LOGFILE), shell=True).wait()

    def mkdir_job_path(self):
        try:
            os.makedirs(self.jobpath)
        except OSError:
            if not os.path.isdir(self.jobpath):
                raise

    def parse_log(self):
        pass
