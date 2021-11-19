import platform
import subprocess
import json


class CResponse:
    def __init__(self):
        self.status = 'uninitialized'
        self.message = 'Did not run'


response = CResponse()

result = []
if platform.system() == 'Windows':
    data = subprocess.check_output(['wmic', 'process', 'list', 'brief'])
    processes = str(data)
    try:
        header = (processes.split("\\r\\r\\n")[0]).split(" ")
        header = list(filter(None, header))
        for i in range(1, len(processes)):
            processes_array = {}
            each_process = (processes.split("\\r\\r\\n")[i]).split(" ")
            each_process = list(filter(None, each_process))
            processes_array[header.__getitem__(0)[2:]] = each_process.__getitem__(0)
            processes_array[" ".join(header[1:-4])] = " ".join(each_process[1:-4])
            processes_array[header[-4]] = each_process[-4]
            processes_array[header[-3]] = each_process[-3]
            processes_array[header[-2]] = each_process[-2]
            processes_array[header[-1]] = each_process[-1]
            result.append(processes_array)
    except IndexError as e:
        pass
    response.status = "success"
    response.message = result
else:
    try:
        processes = subprocess.Popen(['ps', '-U', '0'], stdout=subprocess.PIPE).communicate()[0]
        processes = str(processes.decode('utf-8')).split("\n")
        header = processes[0].split(" ")
        header = list(filter(None, header))

        result = []
        for i in range(1, len(processes)):
            processes_array = {}
            each_process = processes[i].split(" ")
            each_process = list(filter(None, each_process))
            processes_array[header[-4].strip()] = each_process[-4].strip()
            processes_array[header[-3].strip()] = each_process[-3].strip()
            processes_array[header[-2].strip()] = each_process[-2].strip()
            processes_array[header[-1].strip()] = each_process[-1].strip()
            result.append(processes_array)
    except Exception as e:
        pass
    response.status = "success"
    response.message = result

json_output = json.dumps(response, default=lambda x: x.__dict__)
print(json_output)

f = open("../results/output.json", "w+")
f.write(json_output)
f.close()

