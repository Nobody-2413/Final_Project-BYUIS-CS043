import wsgiref.simple_server
import urllib.parse
import http.cookies
import gameFunctions as func

def extractCode(filename):
    file = open(filename, "r")
    lines = file.read()
    file.close()
    return lines

playerForm = '''
    <form action="/input">
        <h3><font face="Courier new" size="4">{} Move (1 to 9): </font><input type="text" name="move"><input type="submit" name="Enter"></h3>
    </form>
'''

startButton = '''
<form action="/playGame">
    <input type="submit" value="Start">
</form>
'''

p1 = None
p2 = None

def determineNames(mode):
    name1 = "Player 1" if mode == 2 else "Player"
    name2 = "Player 2" if name1 == "Player 1" else "Computer"
    return [name1, name2]


def determineSides(side1):
    s1 = side1
    s2 = "O" if s1 == "X" else "X"
    return [s1, s2]


def formattedPage(page, n1, s1, n2, s2, board, inputType):
    return page.format(n1, s1, n2, s2, board[0], board[1], board[2], board[3], board[4], board[5], board[6], board[7], board[8], inputType)


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
        if mode:
            if mode.isdigit() and int(mode) in [1,2]:
                formatting = "Player 1" if int(mode) == 2 else "Player"
                headers.append(('Set-Cookie', 'mode={}'.format(mode)))
                start_response("200 OK", headers)
                page = extractCode("chooseSide.html")
                return [page.format(formatting).encode()]

        start_response("200 OK", headers)
        page = extractCode("homePage.html")
        page += "<h3>Please enter a valid mode</h3>"
        return [page.encode()]


    elif path == "/chooseSide":
        if 'HTTP_COOKIE' not in environ:
            start_response("200 OK", headers)
            return [extractCode("homePage.html").encode()]

        cookies = http.cookies.SimpleCookie()
        cookies.load(environ['HTTP_COOKIE'])
        if 'mode' not in cookies:
            start_response("200 OK", headers)
            return [extractCode("homePage.html").encode()]
        mode = int(cookies['mode'].value)
        player1, player2 = determineNames(mode)

        side = params["side"][0] if "side" in params else None
        if side:
            side = side.upper()
            if side == 'X' or side == 'O':
                side1 = side
                side2 = 'O' if side1 == 'X' else 'X'
                headers.append(("Set-Cookie", "side1={}".format(side1)))
                start_response("200 OK", headers)
                p = extractCode("displayBoard.html")
                page = p.format(player1, side1, player2, side2, "~", "~", "~", "~", "~", "~", "~", "~", "~", startButton)
                return [page.encode()]
        start_response("200 OK", headers)
        page = extractCode("chooseSide.html").format(player1)
        page += "<h3>Please enter a valid side.</h3>"
        return [page.encode()]


    elif path == "/playGame":
        if 'HTTP_COOKIE' not in environ:
            start_response("200 OK", headers)
            return [extractCode("homePage.html").encode()]

        cookies = http.cookies.SimpleCookie()
        cookies.load(environ['HTTP_COOKIE'])
        if not ('mode' in cookies and 'side1' in cookies):
            start_response("200 OK", headers)
            return [extractCode("homePage.html").encode()]

        mode = int(cookies['mode'].value)
        side = cookies['side1'].value
        n1, n2 = determineNames(mode)
        side1, side2 = determineSides(side)

        board = ["~" for x in range(9)]
        next = func.gofirst()

        if mode == 1:
            p1 = func.Player(side1, board, n1)
            p2 = func.Computer(side2, board, n2)

            if next == p2.side:
                move = p2.chooseMove()
                p2.makeMove(move)
                next = p1.side

        inpName = n1 if next == side1 else n2

        headers.append(('Set-Cookie', 'next={}'.format(next)))
        headers.append(('Set-Cookie', 'board={}'.format(",".join(board))))
        p = extractCode("displayBoard.html")
        inpBox = playerForm.format(inpName)
        page = formattedPage(p, n1, side1, n2, side2, board, inpBox)

        start_response("200 OK", headers)
        return [page.encode()]


    else:
        start_response("404 Not Found", headers)
        return ["Status 404: Resource not found".encode()]

port = 8000
httpd = wsgiref.simple_server.make_server('', 8000, application)
print("Server serving at port:", port)
httpd.serve_forever()




