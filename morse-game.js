let palavraInput

// Carregar a página
window.addEventListener("load", () => {

  // Span onde mostramos os pontos
  level = document.getElementById("level")

  // Span onde mostramos se acertou
  resultado = document.getElementById("resultado")

  // Input da palavra
  palavraInput = document.getElementById("palavra")
}, false)


// Define the API URL
const apiUrl = 'https://random-word-api.herokuapp.com/word'


let mini, maxi
let pontos = 0
function startGame(dif) {
    // Tamanho das palavras
    mini = dif * 2
    maxi = dif * 3 + 1

    // Inicializar os pontos
    pontos = 0
    level.innerText = String(pontos)
    resultado.innerText = "Esperando..."
    resultado.style.color = "unset"

    gameStateWORD()
}


let word
function gameStateWORD() {
    // Tamanho aleatório
    let wordLen = Math.floor(Math.random() * (maxi - mini) + mini)

    // Gerar a palavra
    let thisUrl = apiUrl + `?length=${wordLen}`
    
    // Gerar uma palavra aleatória
    return fetch(thisUrl).then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok')
        }   
        return response.json()
    }).then(data => {
        // Guardar a palavra
        word = data[0]
        console.log(word)

        // Enviar a palavra para o ESP
        sendWord(word)
    }).catch(error => {
        console.error('Error:', error)
    })
}


function gameStateAGAIN() {
    // Enviar a palavra para o ESP (outra vez)
    sendWord(word)
}


function gameStateCHECK() {
    // Verificar se a palavra obtida é igual à gerada
    let guess = palavraInput.value.toLowerCase()
    if (guess == word) {
        pontos++
        level.innerText = String(pontos)
        resultado.innerText = "Certo!"
        resultado.style.color = "green"
    } else {
        resultado.innerText = "Errado :("
        resultado.style.color = "red"
    }
    gameStateWORD()
}


