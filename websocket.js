let websocket
function init() {
    let scheme
    if (window.location.protocol == 'https:')
        scheme = 'wss:'
    else
        scheme = 'ws:'

    
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
}

function onClose(evt) {
    console.log("Disconnected")
}

function onMessage(evt) {
    console.log(evt.data)
    document.getElementById("button").innerHTML = evt.data
}

function onError(evt) {
    console.log('ERROR: ' + evt.data)
}

window.addEventListener("load", init, false)