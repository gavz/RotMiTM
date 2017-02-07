#!/usr/bin/python
from flask import Flask

app=Flask(__name__)
@app.route('/', methods= ['GET', 'POST'])

def CustomResponse():
  headers = {
  "Server": "nginx", # Spoof
  "Content-Type": "text/html",
  "Connection": "close",
  }
  response="<html><h1>CustomResponse<h1><br><p>The request was intercepted and this is the new response</p><br><script>alert('XSS')</script></html>"
  returncode=200
  return response, returncode, headers

#app.run(host='127.0.0.1', port=80, debug=True)
app.run(host='127.0.0.1', port=443, debug=True, ssl_context='adhoc')

