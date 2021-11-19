import os
import platform
import json
import subprocess
import sys
import psutil


settings_file = open("../settings.json", "r")
settings = json.load(settings_file);
settings_file.close()


class CResponse:
    def __init__(self):
        self.status = 'uninitialized'
        self.message = 'Did not run'


response = CResponse()


def kill_process(name, process):
    try:
        if platform.system() == 'Windows':
            if name == "name":
                os.system("taskkill /f /im " + str(process))
            elif name == "pid":
                os.system("taskkill /f /pid " + str(process))
            elif name == "user":
                os.system('taskkill /FI "USERNAME eq '+str(process)+'" /F')
            elif name == "filepath":
                os.system('WMIC Process Where "ExecutablePath=\''+str(process)+'\'" Call Terminate')
        else:
            if name == "name":
                for proc in psutil.process_iter():
                    if proc.name() == str(process):
                        proc.kill()
            elif name == "pid":
                os.system("kill -9 " + str(process))
            elif name == "user":
                os.system("killall -u " + str(process))
            elif name == "filepath":
                for proc in psutil.process_iter():
                    if proc.name() == str(process):
                        proc.kill()
        response.status = "success"
        response.message = "Process Killed Successfully"
    except Exception as e:
        response.status = str(e)
        response.message = "Process Kill failed"


if settings_file:
    if "KillProcessBy" in settings and "Value" in settings:
        kill_by = settings['KillProcessBy']
        value = settings['Value']
        kill_process(kill_by, value)

json_output = json.dumps(response, default=lambda x: x.__dict__)
print(json_output)

f = open("../results/output.json", "w+")
f.write(json_output)
f.close()

