import websocket, json, sys, curses, locale
try:
    import thread
except ImportError:
    import _thread as thread

class yPosTracker:
    def __init__(self):
        self.ypos = 1
    
    def getYpos(self):
        return self.ypos
    
    def setYpos(self, newYpos):
        self.ypos = newYpos

username = sys.argv[1]

locale.setlocale(locale.LC_ALL, "")
code = locale.getpreferredencoding()

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(1)

height, width = stdscr.getmaxyx()

div = int(round(height - (height/6)))
divHeight = int(round(height/6))

receiveMessageBox = curses.newwin(div, width, 0, 0)
sendMessageBox = curses.newwin(divHeight, width, div, 0)

ypos = yPosTracker()

def sendThread(*args):
    while(True):
        curses.echo()
        userMessage = sendMessageBox.getstr(1,1).decode("utf-8")
        curses.noecho()
        if(userMessage == "/exit"):
            ws.close()
        sendMessage(args[0], userMessage)
        sendMessageBox.clear()
        sendMessageBox.refresh()

def sendMessage(ws, message):
    object = {
        "username": username,
        "message": message
    }
    objectStr = json.dumps(object)
    encodedStr = str.encode(objectStr)
    ws.send(encodedStr)

def receiveMessage(window, div, message, yPosObject):
    ypos = yPosObject.getYpos()
    window.addstr(ypos, 1, message)
    cursorY, cursorX = window.getyx()
    if (cursorY > div):
        window.scroll((cursorY - div))
    yPosObject.setYpos(cursorY + 1)
    receiveMessageBox.move(1,1)
    window.refresh()

def on_message(ws, message):
    messageObj = json.loads(message)
    message = "{}: {}".format(messageObj["username"], messageObj["message"])
    receiveMessage(receiveMessageBox, div, message, ypos)

def on_error(ws, error):
    print(error)

def on_close(ws):
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()
    sys.exit()

def on_open(ws):
    thread.start_new_thread(sendThread, (ws, 0))


if __name__ == "__main__":
    #websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:8080/chat",
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()

