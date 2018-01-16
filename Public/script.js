var ws = new WebSocket("ws://10.111.61.161:8080/chat");
let username = window.prompt("Choose a username");

ws.onerror = function (event) {
    console.log(event.data);
}

ws.onmessage = function(event) {
    messageObj = JSON.parse(event.data);

    $(function () {
        $("#receiveMessageBox").append("<p>" + messageObj["username"] + " : " + messageObj["message"] + "</p>");
    });
}

ws.onopen = function(event) {
    console.log("connection established!");
}

$(function () {
    $("#sendMessageBox").keypress(function (event) {
        var message = ""
    
        if(event["key"] == "Enter"){
            message = $(this).val();

            console.log(message);
    
            let objToSend = {
                "username": username,
                "message": message
            }
    
            ws.send(JSON.stringify(objToSend));
    
            $(this).val("");
        }
    });
});
