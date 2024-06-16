import Game from '/src/game.js'

// Selecionar o canvas e o seu Context
let canvas = document.getElementById('gameScreen')

let ctx = canvas.getContext('2d')


// Constantes
const GAME_WIDTH = canvas.width
const GAME_HEIGHT = canvas.height


// Criar o Game Objetct
let game = new Game(GAME_WIDTH, GAME_HEIGHT)


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
