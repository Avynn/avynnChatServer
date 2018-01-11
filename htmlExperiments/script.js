console.log("hello world!");

var ws = new WebSocket("ws://localhost:8080/chat");

ws.onerror = function (event) {
    console.log(event.data);
}

ws.onMessage = function(event) {
    messageObj = JSON.parse(event.data);
    
}

$(function () {
    $("<p>This a scripted test!</p>").appendTo("#receiveMessageBox")
});


console.log("ran jquery");