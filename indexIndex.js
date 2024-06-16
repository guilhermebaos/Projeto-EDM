let no, ne, center, so, se
let divs

// Carregar a página
window.addEventListener("load", () => {
    no = document.getElementById("NO")
    ne = document.getElementById("NE")
    center = document.getElementById("CENTER")
    so = document.getElementById("SO")
    se = document.getElementById("SE")

    divs = [no, ne, center, so, se]
}, false)


// Desligar tarefas do ESP antes de sair da página
window.addEventListener("visibilitychange", () => {
    websocket.send("STOP")
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