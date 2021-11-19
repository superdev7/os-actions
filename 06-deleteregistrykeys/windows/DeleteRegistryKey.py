import json
import subprocess
import sys
import winreg


settings_file = 0
settings_file = open("../settings.json", "r")
settings = json.load(settings_file);
settings_file.close()


class CResponse:
    def __init__(self):
        self.status = 'uninitialized'
        self.message = 'Did not run'


response = CResponse()


def delete_reg(reg_path, name):
    try:
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path)
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_ALL_ACCESS)
        winreg.DeleteValue(registry_key, name)
        winreg.CloseKey(registry_key)
        response.status = "success"
        response.message = "Registry deleted Successfully"
    except WindowsError as e:
        response.status = str(e)
        response.message = "Registry delete failed"


if settings_file:
    if "RegistryPath" in settings and "KeyName" in settings and "KeyValue" in settings:
        path = settings["RegistryPath"]
        key = settings["KeyName"]
        value = settings["KeyValue"]
        delete_reg(path, key, value)

json_output = json.dumps(response, default=lambda x: x.__dict__)
print(json_output)

f = open("../results/output.json", "w+")
f.write(json_output)
f.close()

