let d1, d2, d3
let btns

let level
let palavra

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
}, false)


// Desligar tarefas do ESP antes de sair da página
window.addEventListener("visibilitychange", (event) => {
    websocket.send("STOP")
}, false)


function sendMessage(msg) {
    websocket.send(msg)
}


function sendWord(msg) {
    websocket.send(`MORSE:${msg}`)
}


function receiveMessage(msg) {
    console.log(msg)
}


function selectDifficulty(dif) {
    // Start game
    startGame(dif)

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