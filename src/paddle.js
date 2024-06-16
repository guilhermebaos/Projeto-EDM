// Objeto Paddle
export default class Paddle {
    constructor(game) {
        // Altura e Largura da Paddle
        this.width = 150
        this.height = 20

        // Cor da Paddle
        this.color = 'cyan'

        // Velocidade da Paddle
        this.maxSpeed = 100
        this.speed = 0

        // Posição da Paddle
        this.position = {
            x: (game.gameWidth - this.width) / 2,
            y: game.gameHeight - this.height - 10    // Está a 10px da parte de baixo do ecrã
        }

        // Valor máximo do X da Paddle
        this.maxX = game.gameWidth - this.width
    }

    // Desenhar no Canvas a Paddle
    draw(ctx) {
        ctx.fillStyle = this.color
        ctx.fillRect(this.position.x, this.position.y, this.width, this.height)
    }

    // Alterar a Velocidade da Paddle, estas funções são chamadas pelo InputHandler
    moveLeft() {
        this.speed = -this.maxSpeed
    }
    moveRight() {
        this.speed = this.maxSpeed
    }
    stop() {
        this.speed = 0
    }

    // Atualizar a Posição da Paddle
    update(deltaTime) {
        this.position.x += this.speed / deltaTime

        // Detetar Colisões com as Paredes
        if (this.position.x < 0 || this.position.x > this.maxX) {
            this.position.x -= this.speed / deltaTime
        }
    }
}