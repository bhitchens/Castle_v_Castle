import urllib, urllib.parse, urllib.request, json, sys, subprocess, ssl, os

url = 'https://192.168.1.1:8000/'

file = open('test', 'w')
subprocess.Popen(("ipconfig"), stdout = file, stderr = file, shell = True)
file.close()
key = subprocess.check_output(("powershell.exe", "Get-FileHash", "test"))
os.remove('test')

data = {'key' : str(key),
	'team' : sys.argv[1]}

params = json.dumps(data)
request = urllib.request.Request(url, bytes(params, encoding='utf8'))

urllib.request.urlopen(request, context=ssl._create_unverified_context())