var ws = new WebSocket("ws://localhost:8080/chat");

ws.onerror = function (event) {
    console.log(event.data);
}

ws.onmessage = function(event) {
    messageObj = JSON.parse(event.data);
    console.log(messageObj);

    $(function () {
        $("#receiveMessageBox").append("<p>" + messageObj["username"] + " : " + messageObj["message"] + "</p>");
    });
}

ws.onopen = function(event) {
    console.log("connection established!");

    let objToSend = {
        "username": "html client",
        "message": "hello world!"
    }

    ws.send(JSON.stringify(objToSend));
}
