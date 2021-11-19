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


def set_reg(reg_path, name, value):
    global response
    try:
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path)
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, value)
        winreg.CloseKey(registry_key)
        response.status = "success"
        response.message = "Registry set Successfully"
    except Exception as e:
        response.status = str(e)
        response.message = "Registry set failed"


def create_reg(reg_path, name, value):
    try:
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path)
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, value)
        winreg.CloseKey(registry_key)
        response.status = "success"
        response.message = "Registry created Successfully"
    except Exception as e:
        response.status = str(e)
        response.message = "Registry creation failed"


if settings_file:
    if "Operation" in settings and "RegistryPath" in settings and "KeyName" in settings and "KeyValue" in settings:
        operation = settings["Operation"]
        path = settings["RegistryPath"]
        key = settings["KeyName"]
        value = settings["KeyValue"]
        if operation == "SetRegistry":
            set_reg(path, key, value)
        elif operation == "CreateRegistry":
            create_reg(path, key, value)

json_output = json.dumps(response, default=lambda x: x.__dict__)
print(json_output)

f = open("../results/output.json", "w+")
f.write(json_output)
f.close()