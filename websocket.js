let websocket
let display
function init() {
    let scheme
    if (window.location.protocol == 'https:')
        scheme = 'wss:'
    else
        scheme = 'ws:'

    display = document.getElementById("display")
    
    let wsUri = scheme + '//' + window.location.hostname + '/ws';
    console.log("Connecting to " + wsUri + "...")

    websocket           = new WebSocket(wsUri)
    websocket.onopen    = function(evt) { onOpen    (evt) }
    websocket.onclose   = function(evt) { onClose   (evt) }
    websocket.onmessage = function(evt) { onMessage (evt) }
    websocket.onerror   = function(evt) { onError   (evt) }

}

function onOpen(evt) {
    console.log("Connected")
    display.innerText = "Conectado!"
    display.style.color = "green"
}

function onClose(evt) {
    console.log("Disconnected")
    display.innerText = "Desconectado :("
    display.style.color = "red"
}

function onMessage(evt) {
    console.log(evt.data)
    receiveMessage(evt.data)
}

function onError(evt) {
    console.log('ERROR: ' + evt.data)
}

window.addEventListener("load", init, false)