from urllib.parse import urlparse
import socket
import sys
#sockets to talk with other computers
class URL:
    def __init__(self,ur):
        self.url=urlparse(ur)
        assert self.url.scheme =="http"

    def request(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = self.url.hostname
        port = self.url.port or 80
        s.connect((host, port))

        path = self.url.path or "/"
        request = f"GET {path} HTTP/1.0\r\n"
        request += f"Host: {host}\r\n"
        request += "\r\n"

        s.send(request.encode("utf8"))

        response = s.makefile("r", encoding="utf8", newline="\r\n")

        statusline = response.readline()
        version, status, explanation = statusline.split(" ", 2)

        headers = {}
        line = response.readline()
        while line != "\r\n":
            header, value = line.split(":", 1)
            headers[header.casefold()] = value.strip()
            line = response.readline()

        body = response.read()
        s.close()
        return body
        

def show(body):
    inTag = False
    inStyle = False
    inScript = False

    i = 0
    while i < len(body):
        if body[i:i+7].lower() == "<style>":
            inStyle = True
            i += 7
            continue
        if body[i:i+8].lower() == "</style>":
            inStyle = False
            i += 8
            continue
        if body[i:i+8].lower() == "<script>":
            inScript = True
            i += 8
            continue
        if body[i:i+9].lower() == "</script>":
            inScript = False
            i += 9
            continue

        c = body[i]

        if inStyle or inScript:
            i += 1
            continue

        if c == "<":
            inTag = True
        elif c == ">":
            inTag = False
        elif not inTag:
            print(c, end="")

        i += 1
  
def load(url):
    body=url.request()
    show(body)

if __name__=="__main__":
    load(URL(sys.argv[1]))
    
        
            









        
