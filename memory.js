let d1, d2, d3
let btns

let level

// Carregar a página
window.addEventListener("load", () => {
    d1 = document.getElementById("d1")
    d2 = document.getElementById("d2")
    d3 = document.getElementById("d3")

    btns = [d1, d2, d3]

    // Enable button action
    for (let i = 0; i < btns.length; i++) {
        btns[i].addEventListener("click", (event) => {
            selectDifficulty(i + 1)
        })
    }

    // Span onde mostramos o nível
    level = document.getElementById("level")
}, false)


// Desligar tarefas do ESP antes de sair da página
window.addEventListener("visibilitychange", (event) => {
    websocket.send("STOP")
}, false)


function sendMessage(msg) {
    websocket.send(msg)
}


function receiveMessage(msg) {
    if (msg.startsWith("LEVEL")) {
        level.innerText = msg.slice(msg.length-1)
    }
}


function selectDifficulty(dif) {
    // Start game
    try {
        console.log(`MEMORY${dif}`)
        sendMessage(`MEMORY${dif}`)
    } catch (e) {
        console.log(e)
    }

    // Disable buttons
    for (let i = 0; i < btns.length; i++) {
        btns[i].setAttribute("disabled", "disabled")
    }
}


function restartGame() {
    // Desativar o ESP
    sendMessage("STOP")

    // Enable buttons
    for (let i = 0; i < btns.length; i++) {
        btns[i].removeAttribute("disabled")
    }
}