export function detectCollision(ball, gameObject) {
    // Colisões com um GameObject
    // Partes da Bola que podem colidir
    let topBall = ball.position.y
    let rightBall = ball.position.x + ball.size
    let bottomBall = ball.position.y + ball.size
    let leftBall = ball.position.x

    let topGameObject = gameObject.position.y
    let rightGameObject = gameObject.position.x + gameObject.width
    let bottomGameObject = gameObject.position.y + gameObject.height
    let leftGameObject = gameObject.position.x

    if (bottomBall >= topGameObject
        && topBall <= bottomGameObject
        && leftBall >= leftGameObject
        && rightBall <= rightGameObject
    ) {
        return true
    } else {
        return false
    }
}