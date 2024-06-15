let up, left, center, right, down
let divs

window.addEventListener("load", () => {
    up = document.getElementById("UP")
    left = document.getElementById("LEFT")
    center = document.getElementById("CENTER")
    right = document.getElementById("RIGHT")
    down = document.getElementById("DOWN")

    divs = [up, left, center, right, down]
}, false)

function sendMessage(msg) {
    websocket.send(msg)
}


function receiveMessage(msg) {
    for (let i = 0; i < divs.length; i++) {
        if (i == msg) {
            element = divs[Number(i)]
            element.style.backgroundColor = "green"
        } else {
            element = divs[Number(i)]
            element.style.backgroundColor = "unset"
        }
    }
}