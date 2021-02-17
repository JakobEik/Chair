from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import cgi
from TableAssignment.DFA_RW import DFA_RW
from TableAssignment.ServerRequests import getFromServer, deleteFromServer, updateServer

HOST_NAME = '127.0.0.1'
PORT_NUMBER = 1235  # Maybe set this to 1234


class Status:
    status = False

    def set(self):
        self.status = True

    def reset(self):
        self.status = False

    def get(self):
        return self.status


status = Status()


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global status
        """Respond to a GET request."""
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        output = ''
        output += '<!DOCTYPE html>'
        output += '<html>'
        output += '<body>'
        output += '<h2>Products details</h2>'
        output += '<form method="POST" enctype="multipart/form-data" action="/product_info">'
        output += '<label for="legH">Leg Height (mm):</label><br>'
        output += '<input type="text" id="legH" name="legH"><br>'
        output += '<label for="legL">Leg Length (mm):</label><br>'
        output += '<input type="text" id="legL" name="legL"><br>'
        output += '<label for="legW">Leg Width (mm):</label><br>'
        output += '<input type="text" id="legW" name="legW"><br>'
        output += '<label for="topH"> Top Height (mm):</label><br>'
        output += '<input type="text" id="topH" name="topH"><br>'
        output += '<label for="topL">Top Length (mm):</label><br>'
        output += '<input type="text" id="topL" name="topL"><br>'
        output += '<label for="topW">Top Width (mm):</label><br>'
        output += '<input type="text" id="topW" name="topW"><br><br>'

        # submit button
        output += '<input type="submit" value="Submit">'
        output += '</form>'
        output += '</body></html>'

        if status.get():
            topL, topW, topH, legL, legW, legH = getFromServer()
            output += '<p>The table has been made with the parameters <br><br> '
            output += 'Leg height: ' + legH + ' <br>'
            output += 'Leg length: ' + legL + ' <br>'
            output += 'Leg width: ' + legW + ' <br>'
            output += 'Top height: ' + topH + ' <br>'
            output += 'Top length: ' + topL + ' <br>'
            output += 'Top width: ' + topW + ' <br> '
            output += '</p>'
            status.reset()

        elif not status.get() and self.path.endswith('product_info'):
            output += '<p> Looks like you put in non-integer values </p>'

        self.wfile.write(output.encode())

    # noinspection PyTypeChecker
    def do_POST(self):
        global status
        if self.path.endswith('/product_info'):
            # type = multipart/form-data
            contentType, primaryDictionary = cgi.parse_header(self.headers.get('content-type'))
            primaryDictionary['boundary'] = bytes(primaryDictionary['boundary'], "utf-8")
            content_len = int(self.headers.get('content-length'))
            primaryDictionary['CONTENT-LENGTH'] = content_len
            if contentType == 'multipart/form-data':
                # parses the form to a dictionary
                fields = cgi.parse_multipart(self.rfile, primaryDictionary)
                # print(fields)
                self.send_response(301)
                self.send_header("Content-type", "text/html")
                self.send_header('Location', '/product_info')
                self.end_headers()

                values = fields.values()
                allParamsCorrect = True
                for value in values:
                    if not str(value[0]).isnumeric():
                        allParamsCorrect = False

                if not allParamsCorrect:
                    print("Illegal inputs:", fields)

                if allParamsCorrect:
                    topL = fields.get('topL')[0]
                    topW = fields.get('topW')[0]
                    topH = fields.get('topH')[0]
                    legL = fields.get('legL')[0]
                    legW = fields.get('legW')[0]
                    legH = fields.get('legH')[0]
                    deleteFromServer()
                    updateServer(topL, topW, topH, legL, legW, legH)

                    # Get parameters from server and write to DFA file. They are the same as the params above
                    tL, tW, tH, lL, lW, lH = getFromServer()
                    DFA_RW(tL, tW, tH, lL, lW, lH)

                    # Sets the status to True to indicate that a table has been made
                    status.set()


if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print(time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER))

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER))
