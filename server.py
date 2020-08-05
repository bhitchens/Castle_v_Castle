from http.server import BaseHTTPRequestHandler, HTTPServer
import ssl, json, time, sys

def score(ipAddr, curTime, serverDict, team, key):
	global redScore
	global blueScore

	#anti-cheat - store md5 of ip addr on first submit; reject future submits without same key
	if (serverDict[ipAddr + "key"] == ""):
		serverDict.update({ipAddr + "key" : key})
	if (serverDict[ipAddr + "key"] == key):
		if (curTime - serverDict[ipAddr] > 60):
			if ("blue" in team):
				blueScore += 1
				serverDict.update({ipAddr : curTime})
			if ("red" in team):
				redScore += 1
				serverDict.update({ipAddr : curTime})

class MyHandler(BaseHTTPRequestHandler):
	def _set_headers(s):
		s.send_response(200)
		s.send_header("Content-type", "text/html")
		s.end_headers()

	def do_HEAD(s):
		s._set_headers()

	def do_GET(s):
		s._set_headers()
		s.wfile.write(b"<html><head><title>Scores</title></head>")
		s.wfile.write(b"<body><p>Red: %d Blue: %d</p>" % (redScore, blueScore))
		s.wfile.write(b"</body></html>")

	def do_POST(s):
		s._set_headers()
		content_length = int(s.headers['Content-Length'])
		body = s.rfile.read(content_length)
		jsonMessage = json.loads(body)
		ipAddr = s.client_address[0]
		curTime = time.time()
		score(ipAddr, curTime, serverDict, jsonMessage["team"], jsonMessage["key"])
		print("Red: %d Blue: %d" % (redScore, blueScore))

def run(server_class=HTTPServer, handler_class=MyHandler, port=8000):
	server_address = ('', port)
	httpd = server_class(server_address, handler_class)
	httpd.socket = ssl.wrap_socket(httpd.socket, keyfile='./server.key', certfile='./server.cert', server_side='True')
	httpd.serve_forever()


if __name__ == "__main__":
	global redScore
	global blueScore
	global serverDict
	serverDict = {}
	for arg in sys.argv[1:]:
		serverDict[arg] = 0
		serverDict[arg + "key"] = ""
	redScore = 0
	blueScore = 0
	run()