import platform
import json


class CResponse:
    def __init__(self):
        self.status = 'uninitialized'
        self.message = 'Did not run'


response = CResponse()
try:
    response.status = "success"
    response.message = str(platform.system()) + " " + str(platform.version())
except Exception as e:
    response.status = "success"
    response.message = str(e)

json_output = json.dumps(response, default=lambda x: x.__dict__)
print(json_output)

f = open("../results/output.json", "w+")
f.write(json_output)
f.close()
