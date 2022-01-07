import wsgiref.simple_server
import urllib.parse
import http.cookies

def extractCode(filename):
    file = open(filename, "r")
    lines = file.read()
    file.close()
    return lines

playerForm = '''
    <form action="/input">
        <h3>{} Move (1 to 9): <input type="text" name="{}"><input type="submit" name="Enter"></h3>
    </form>
'''
side1 = None
side2 = None

def application(environ, start_response):
    headers = [('Content-Type', 'text/html; charset=utf-8')]

    path = environ["PATH_INFO"]
    params = urllib.parse.parse_qs(environ["QUERY_STRING"])

    if path == "/":
        start_response("200 OK", headers)
        page = extractCode("homePage.html")
        return [page.encode()]

    elif path == "/chooseMode":
        mode = params["mode"][0] if "mode" in params else None
        start_response("200 OK", headers)
        if mode:
            if mode.isdigit() and int(mode) in [1,2]:
                page = extractCode("chooseSide.html")
                formatting = "Player 1" if mode == 2 else "Player"
                return [page.format(formatting).encode()]
        page = extractCode("homePage.html")
        page += "<h3>Please enter a valid mode</h3>"
        return [page.encode()]

    elif path == "/chooseSide":
        side = params["side"][0] if "side" in params else None
        start_response("200 OK", headers)
    else:
        start_response("404 Not Found", headers)
        return ["Status 404: Resource not found".encode()]

port = 8000
httpd = wsgiref.simple_server.make_server('', 8000, application)
print("Server serving at port:", port)
httpd.serve_forever()



