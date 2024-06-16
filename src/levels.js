import Brick from '/src/brick.js'

export function buildLevel(game, level) {
    let bricks = []

    level.forEach((row, rowIndex) => {
        row.forEach((brickBool, brickIndex) => {
            if (brickBool == 1) {
                let position = {
                    x: brickIndex * 80,
                    y: 70 + rowIndex * 25
                }

                bricks.push(new Brick(game, position))
            }
        })
    })

    return bricks
}

export const level1 = [
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
]

export const level2 = [
    [0, 1, 0, 1, 0, 0, 1, 0, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]