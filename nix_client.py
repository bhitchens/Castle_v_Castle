import urllib, urllib.parse, urllib.request, json, sys, subprocess, ssl

url = 'https://192.168.1.1:8000'

ip = subprocess.Popen(("ip", "addr"), stdout = subprocess.PIPE)
key = subprocess.check_output(("md5sum"), stdin=ip.stdout)

data = {'key' : str(key),
	'team' : sys.argv[1]}

params = json.dumps(data)
request = urllib.request.Request(url, bytes(params, encoding='utf8'))

urllib.request.urlopen(request, context=ssl._create_unverified_context())