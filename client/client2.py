import websocket, json, sys, curses, locale

try:
    import thread
except ImportError:
    import _thread as thread

'''
    #### Class declaration and argument handling ####
'''

#class used to track and update the yposition of the cursor in the receive message box.
class yPosTracker:
    def __init__(self):
        self.ypos = 1
    
    def getYpos(self):
        return self.ypos
    
    def setYpos(self, newYpos):
        self.ypos = newYpos

#if there is no command argument supplied prompt user for username.
if (len(sys.argv) != 2):
    print("Enter a nick/user name")
    username = input(">")
else:
    username = sys.argv[1]

'''
    #### Global Inits ####
'''

#Setting of locale
locale.setlocale(locale.LC_ALL, "")
code = locale.getpreferredencoding()

#stdscr noecho init
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(1)

#get height and width of screen.
height, width = stdscr.getmaxyx()

#calculate division between two screens
div = int(round(height - (height/6)))
divHeight = int(round(height/6))

#receive message box and send message box init.
receiveMessageBox = curses.newwin(div, width, 0, 0)
sendMessageBox = curses.newwin(divHeight, width, div, 0)

#init ypos tracker on the heap
ypos = yPosTracker()

'''
    #### Function Declarations ####
'''

#thread main, used for synchronisly sending messages
def sendThread(*args):
    while(True):
        #allow echoing in the send message box and get string from top left corner.
        curses.echo()
        userMessage = sendMessageBox.getstr(1,1).decode("utf-8")
        curses.noecho()
        
        #check for /exit command which will cause the program to exit.
        if(userMessage == "/exit"):
            ws.close()
        
        #send message through socket, clear and refresh send message box.
        sendMessage(args[0], userMessage)
        sendMessageBox.clear()
        sendMessageBox.refresh()

def sendMessage(ws, message):
    #create object dictionary for json.dumps
    object = {
        "username": username,
        "message": message
    }

    #package dictionary and send accross web socket.
    objectStr = json.dumps(object)
    encodedStr = str.encode(objectStr)
    ws.send(encodedStr)

def receiveMessage(window, div, message, yPosObject):
    
    #get ypos from the tracker
    ypos = yPosObject.getYpos()
    
    #render string on window and get the current cursor pos.
    window.addstr(ypos, 1, message)
    cursorY, cursorX = window.getyx()
    
    #if the cursor is below the window scroll up to get it back in
    if (cursorY > div):
        window.scroll((cursorY - div))
    
    #set new ypos and move cursor back to the sendMessageBox
    yPosObject.setYpos(cursorY + 1)
    sendMessageBox.move(1,1)
    window.refresh()


'''
    #### Web Socket Closures ####
'''

def on_message(ws, message):
    #load message from string create format string and pass that to receive message.
    messageObj = json.loads(message)
    message = "{}: {}".format(messageObj["username"], messageObj["message"])
    receiveMessage(receiveMessageBox, div, message, ypos)

def on_error(ws, error):
    #print the error
    print(error)

def on_close(ws):
    #return terminal to original state and exit
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()
    sys.exit()

def on_open(ws):
    thread.start_new_thread(sendThread, (ws, 0))

'''
    #### "Main" function ####
'''


if __name__ == "__main__":
    ws = websocket.WebSocketApp("ws://localhost:8080/chat",
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()

