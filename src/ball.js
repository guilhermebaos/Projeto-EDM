import {detectCollision} from '/src/collisionDetection.js'

// Objeto Ball
export default class Ball {
    constructor(game) {
        // Guardar o Game object
        this.game = game

        // Imagem e tamanho da Bola
        this.image = document.getElementById('imgBall')
        this.size = 16

        // Valores máximo para o X e Y da Bola
        this.maxX = game.gameWidth - this.size
        this.maxY = game.gameHeight - this.size

        this.reset()
    }

    reset() {
        // Posição e Velocidade da Bola
        this.position = {x: 100, y: 400}
        this.speed = {x: 80, y: -40}
    }

    // Desenhar a Bola
    draw(ctx) {
        ctx.drawImage(this.image, this.position.x, this.position.y, this.size, this.size)
    }

    // Atualizar a posição da Bola
    update(deltaTime) {
        this.position.x += this.speed.x / deltaTime
        this.position.y += this.speed.y / deltaTime

        // Detetar colisões com as paredes
        if (this.position.x < 0 || this.position.x > this.maxX) {
            this.speed.x = -this.speed.x
        }
        if (this.position.y < 0) {
            this.speed.y = -this.speed.y
        }

        // Detetar se a bola atingiu a parte debaixo do jogo
        if (this.position.y > this.maxY) {
            this.game.lives--
            this.reset()
        }

        // Detetar colisões com outros objetos do jogo
        if (detectCollision(this, this.game.paddle)) {
            this.speed.y = -this.speed.y
            this.position.y = this.game.paddle.position.y - this.size
        }
    }
}