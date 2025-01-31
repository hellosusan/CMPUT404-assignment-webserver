#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos, 2022 Susan (Ngoc Thao Nguyen) Trang
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        #print ("Got a request of: %s\n" % self.data)
        
        decodedRequest = self.data.decode().split(' ')
        
        try:
            # The path of the request
            path  = decodedRequest[1]
            
            # The relative path
            # Normalize variable path to remove redundant separators (handle test_get_group)
            # Cite: https://stackoverflow.com/a/37205088
            relpath = './www' + os.path.normpath(path)
            
            # when request method is GET
            if decodedRequest[0] == 'GET':
                # relpath exists and is the path of a file
                if os.path.isfile(relpath):
                    file = open(relpath, 'r')
                    content = file.read()
                    file.close()
                    contentType = path.split('.')[1]
                    respond = f'HTTP/1.1 200 OK\r\nContent-Type: text/{contentType}\r\nContent-Length: {len(content)}\r\n\r\n{content}'
                 
                # relpath exists and is the path of a directory
                elif os.path.isdir(relpath):
                    if path[-1] == '/':
                        file = open(f'{relpath}/index.html', 'r')
                        content = file.read()
                        file.close()
                        respond = f'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(content)}\r\n\r\n{content}'
                    else:
                        respond = f'HTTP/1.1 301 Move Permanently\r\nLocation: {path}/\r\n'
                
                # relpath not exists 
                else:
                    respond = 'HTTP/1.1 404 Not Found\r\n'
            
            # method is not GET: not support
            else:
                respond = 'HTTP/1.1 405 Method Not Allowed\r\n'
            
            self.request.sendall(bytearray(respond,'utf-8'))
        
        except:
            pass
        
        return

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
