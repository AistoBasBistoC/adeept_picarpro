################################
##Generated with a lot of love##
##    with   EasyPython       ##
##Web site: easycoding.tn     ##
################################
import RPi.GPIO as GPIO
from http.server import BaseHTTPRequestHandler, HTTPServer

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)
request = None

class RequestHandler_httpd(BaseHTTPRequestHandler):
  def do_GET(self):
    global request
    messagetosend = bytes('Hello!',"utf")
    self.send_response(200)
    self.send_header('Content-Type', 'text/plain')
    self.send_header('Content-Length', len(messagetosend))
    self.end_headers()
    self.wfile.write(messagetosend)
    request = self.requestline
    request = request[5 : int(len(request)-9)]
    print(request)
    if request == 'on':
      GPIO.output(26,False)
    if request == 'off':
      GPIO.output(26,True)
    return


server_address_httpd = ('192.168.254.29',8080)
httpd = HTTPServer(server_address_httpd, RequestHandler_httpd)
print('Starting Server.....')
httpd.serve_forever()
