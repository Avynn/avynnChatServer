import websocket, json, sys

#from websocket import create_connection
#ws = create_connection("ws://localhost:8080/chat")
#print("sending 'Hello World'...")
#ws.send("Hello World")
#print("sent")
#ws.close

username = sys.argv[1]

def sendMessage(ws):
    message  = input ("> ")
    if (message == "\exit") :
        ws.close()
        sys.exit()
    objectToSend = {
        "username": username,
        "message": message
    }
    objectString = json.dumps(objectToSend)
    objectBytes = str.encode(objectString)
    ws.send(objectBytes)

def on_message(ws, message):
    messageObj = json.loads(message)
    print("{}: {}".format(messageObj["username"], messageObj["message"]))
    sendMessage(ws)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("connection closed")

def on_open(ws):
    print("enter your message!")
    sendMessage(ws)


if __name__ == "__main__":
    #websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:8080/chat",
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()


