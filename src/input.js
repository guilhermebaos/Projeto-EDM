// Define o que acontece com os Inputs
export default class InputHandler {
    constructor(game) {
        document.addEventListener('keydown', key => {
            switch(key.code) {
                case 'ArrowLeft':
                    game.paddle.moveLeft()
                    break

                case 'ArrowRight':
                    game.paddle.moveRight()
                    break

                case 'Escape':
                    game.togglePause()
                    break

                case 'Space':
                    game.start()
                    break

                default:
                    break
            }
        })
        document.addEventListener('keyup', key => {
            switch(key.code) {
                case 'ArrowLeft':
                    if (game.paddle.speed < 0) game.paddle.stop()
                    break

                case 'ArrowRight':
                    if (game.paddle.speed > 0) game.paddle.stop()
                    break

                default:
                    break
            }
        })
    }
}