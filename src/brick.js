import {detectCollision} from '/src/collisionDetection.js'

// Tijolos que vão ser destruidos
export default class Brick {
    constructor(game, position) {
        // Guardar o Game object
        this.game = game

        // Imagem e tamanho do Tijolo
        this.image = document.getElementById('imgBrick')
        this.width = 78
        this.height = 24

        // Posição do Tijolo
        this.position = position

        // Marcar o Tijolo para ser apagado
        this.markedForDeletion = false
    }

    draw(ctx) {
        ctx.drawImage(this.image, this.position.x, this.position.y, this.width, this.height)
    }

    update() {
        if (detectCollision(this.game.ball, this)) {
            this.game.ball.speed.y = -this.game.ball.speed.y

            this.markedForDeletion = true
        }
    }
}