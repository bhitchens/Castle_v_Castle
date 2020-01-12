import urllib, urllib.parse, urllib.request, json, sys, subprocess, ssl, os

url = 'http://192.168.100.1'

file = open('test', 'w')
subprocess.Popen(("ipconfig"), stdout = file, stderr = file, shell = True)
key = subprocess.check_output(("powershell.exe", "Get-FileHash", "test"))
file.close()
os.remove('test')

data = {'key' : str(key),
	'team' : sys.argv[1]'}

params = json.dumps(data)
request = urllib.request.Request(url, bytes(params, encoding='utf8'))

urllib.request.urlopen(request, context=ssl._create_unverified_context())