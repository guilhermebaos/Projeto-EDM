console.log("Index.js!")
console.log(websocket)

function sendMessage(msg) {
    websocket.send(msg)
}