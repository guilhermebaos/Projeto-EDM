import Game from '/src/game.js'

// Selecionar o canvas e o seu Context
let canvas = document.getElementById('gameScreen')

let ctx = canvas.getContext('2d')


// Constantes
const GAME_WIDTH = canvas.width
const GAME_HEIGHT = canvas.height


// Criar o Game Objetct
let game = new Game(GAME_WIDTH, GAME_HEIGHT)
window.game = game


function receiveMessage(msg) {
    switch(msg) {
        case '0':
            window.game.paddle.moveLeft()
            break

        case '1':
            window.game.paddle.moveRight()
            break

        case '3':
            window.game.start()
            break

        case '4':
            window.game.togglePause()
            break

        case '5':
            if (window.game.paddle.speed < 0) window.game.paddle.stop()
            if (window.game.paddle.speed > 0) window.game.paddle.stop()
            break

        default:
            break
    }
}

window.receiveMessage = receiveMessage

console.log(receiveMessage)


// Criar o Game Loop
let lastTime = 0

function gameLoop(timeStamp) {
    let deltaTime = timeStamp - lastTime
    lastTime = timeStamp

    ctx.clearRect(0, 0, GAME_WIDTH, GAME_HEIGHT)

    game.update(deltaTime)
    game.draw(ctx)

    requestAnimationFrame(gameLoop)
}

requestAnimationFrame(gameLoop)
