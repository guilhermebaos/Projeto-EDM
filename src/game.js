import Paddle from '/src/paddle.js'
import Ball from '/src/ball.js'
import InputHandler from '/src/input.js'

import {buildLevel, level1, level2, level3} from '/src/levels.js'

const GAMESTATE = {
    PAUSED: 0,
    RUNNING: 1,
    MENU: 2,
    GAMEOVER: 3,
    NEWLEVEL: 4
}

// Objeto Game
export default class Game {
    constructor(gameWidth, gameHeight) {
        // Largura e Altura do Canvas
        this.gameWidth = gameWidth
        this.gameHeight = gameHeight

        // Definir o Estado inicial
        this.gamestate = GAMESTATE.MENU

        // Carregar os Objetos
        this.paddle = new Paddle(this)
        this.ball = new Ball(this)

        this.gameObjects = []
        this.bricks = []

        // Input Handler
        this.handler = new InputHandler(this)

        // Vidas do jogo
        this.lives = 3

        // Níveis
        this.levels = [level1, level2, level3]
        this.currentLevel = 0
    }

    // Inicializar os Níveis do Breakout
    start() {
        if (this.gamestate !== GAMESTATE.MENU
            && this.gamestate !== GAMESTATE.NEWLEVEL) return

        this.bricks = buildLevel(this, this.levels[this.currentLevel])
        this.ball.reset()

        this.gameObjects = [
            this.paddle,
            this.ball,
            ...this.bricks
        ]

        this.gamestate = GAMESTATE.RUNNING
    }

    // Atualizar todos os Objetos
    update(deltaTime) {
        if (this.gamestate === GAMESTATE.PAUSED
            || this.gamestate === GAMESTATE.MENU
            || this.gamestate === GAMESTATE.GAMEOVER) return
        
        if (this.lives === 0) this.gamestate = GAMESTATE.GAMEOVER
        
        if (this.bricks.length === 0) {
            this.currentLevel++
            this.gamestate = GAMESTATE.NEWLEVEL
            this.start()
        }

        this.gameObjects.forEach((gameObj) => gameObj.update(deltaTime))

        this.gameObjects = this.gameObjects.filter(object => !object.markedForDeletion)
        this.bricks = this.bricks.filter(object => !object.markedForDeletion)
    }

    // Desenhar todos os Objetos
    draw(ctx) {
        this.gameObjects.forEach((gameObj) => gameObj.draw(ctx))

        if (this.gamestate === GAMESTATE.PAUSED) {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.5)'
            ctx.fillRect(0, 0, this.gameWidth, this.gameHeight)

            
            ctx.font = '30px Arial'
            ctx.textAlign = 'center'
            ctx.fillStyle = 'white'

            ctx.fillText('Em Pausa', this.gameWidth / 2, this.gameHeight / 2)
        }

        if (this.gamestate === GAMESTATE.MENU) {
            ctx.fillStyle = 'rgba(0, 0, 0, 1)'
            ctx.fillRect(0, 0, this.gameWidth, this.gameHeight)

            
            ctx.font = '50px Arial'
            ctx.textAlign = 'center'
            ctx.fillStyle = 'white'

            ctx.fillText('Clica no START para começar', this.gameWidth / 2, this.gameHeight / 2)
        }

        if (this.gamestate === GAMESTATE.GAMEOVER) {
            ctx.fillStyle = 'rgba(0, 0, 0, 1)'
            ctx.fillRect(0, 0, this.gameWidth, this.gameHeight)
    
            
            ctx.font = '50px Arial'
            ctx.textAlign = 'center'
            ctx.fillStyle = 'red'
    
            ctx.fillText('Gameover!', this.gameWidth / 2, this.gameHeight / 2)
        }
    }

    // Fazer pausa ao jogo
    togglePause() {
        if (this.gamestate == GAMESTATE.PAUSED) {
            this.gamestate = GAMESTATE.RUNNING
        } else {
            this.gamestate = GAMESTATE.PAUSED
        }
    }
}
