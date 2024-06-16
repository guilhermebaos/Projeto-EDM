from games import colour_cycle
from random import choice
from machine import Pin
import asyncio
import web
import gc


# Botões Input
NO = Pin(14, Pin.IN, Pin.PULL_UP)
NE = Pin(13, Pin.IN, Pin.PULL_UP)
SO = Pin(10, Pin.IN, Pin.PULL_UP)
SE = Pin(9, Pin.IN, Pin.PULL_UP)
C = Pin(12, Pin.IN, Pin.PULL_UP)

BTNS = [NO, NE, C, SO, SE]

# Pinos dos LEDs
red = Pin(25, Pin.OUT)
green = Pin(21, Pin.OUT)
blue = Pin(22, Pin.OUT)

RGB = [red, green, blue]


def turnON(index):
    for pos, item in enumerate(RGB):
        if pos == index:
            item.value(0)
        else:
            item.value(1)


def turnOFF():
    for pos, item in enumerate(RGB):
        item.value(1)


# Mostrar que chegamos ao main.py
turnON(1)

# Criar a App
app = web.App(host='0.0.0.0', port=80)

# Criar WebSocket client
WS_CLIENTS = set()


async def send_message(msg):
    for ws_client in WS_CLIENTS:
        try:
            await ws_client.send(msg)
        except Exception as e:
            print("Error sending message: " + str(e))


running_tasks = dict()
async def stop_tasks():
    global running_tasks
    for task in running_tasks.values():
        task.cancel()


async def receive_message(msg):

    # Ordem para ligar um dos LEDs
    if msg in ["0", "1", "2"]:
        await stop_tasks()
        turnON(int(msg))

    elif msg == "OFF":
        turnOFF()

    elif msg == "CYCLE_START":
        task = asyncio.create_task(colour_cycle(cycles=1e6))
        running_tasks["colour_cycle"] = task

    elif msg == "STOP":
        asyncio.create_task(send_message(msg))
        await stop_tasks()
        await asyncio.sleep(0)
        turnOFF()

    elif "MEMORY" in msg:
        dif = int(msg[-1])
        task = asyncio.create_task(memory(num_levels=1e6, difficulty=dif))
        running_tasks["memory"] = task

    return


# Verificar se algum botão foi clicado
last_message = "-1"
async def checkbut():
    global WS_CLIENTS, last_message
    while True:
        new_message = "5"
        for index, item in enumerate(BTNS):
            if not item.value():
                new_message = str(index)
                break

        if new_message != last_message:
            asyncio.create_task(send_message(new_message))
            last_message = new_message

        await asyncio.sleep_ms(5)


async def memory(
        pinr=25,
        ping=21,
        pinb=22,
        butr=10,
        butg=14,
        butb=13,
        butres=9,
        butsub=12,
        num_levels=10,
        difficulty=1,
        ):
    """
    Jogo da Memória: Cria uma sequência de cores aleatória (mostrada no LED RGB),
                    que o jogador deve repetir de seguida.
    O LED RGB deve estar em lógica negativa.
    --- Parâmetros ---
    - pinr: pin ao qual está ligado a perna RED
    - ping: pin ao qual está ligado a perna GREEN
    - pinb: pin ao qual está ligado a perna BLUE
    - butr: pin ao qual está ligado o botão correspondente ao RED
    - butg: pin ao qual está ligado o botão correspondente ao GREEN
    - butb: pin ao qual está ligado o botão correspondente ao BLUE
    - butres: pin ao qual está ligado o botão que dá reset na resposta
    - butsub: pin ao qual está ligado o botão que submete a resposta
    - num_levels: número de níveis do jogo (corresponde ao nº de sequências criadas.
                A sequência seguinte tem +1 cor que a anterior)
    - difficulty: nível de dificuldade (associada ao tempo de pausa entre cores).
                Pode ser 1, 2 ou 3.
    """

    # escolher a dificuldade
    pauses_list = [1.5, 1, 0.5]
    pause = pauses_list[difficulty - 1]

    # definir os LEDs
    red = Pin(pinr, Pin.OUT)
    red.value(1)
    green = Pin(ping, Pin.OUT)
    green.value(1)
    blue = Pin(pinb, Pin.OUT)
    blue.value(1)

    # definir os botões
    butred = Pin(butr, Pin.IN, Pin.PULL_UP)
    butgreen = Pin(butg, Pin.IN, Pin.PULL_UP)
    butblue = Pin(butb, Pin.IN, Pin.PULL_UP)
    butreset = Pin(butres, Pin.IN, Pin.PULL_UP)
    butsubmit = Pin(butsub, Pin.IN, Pin.PULL_UP)

    # gera os níveis
    n = 1
    while n != num_levels+1:
        # enviar o nível para o site
        asyncio.create_task(send_message("LEVEL" + str(n)))

        # gerar a sequência de cores aleatória
        colours = ["red", "green", "blue"]
        random_sequence = []
        for _ in range(n):
            random_sequence.append(choice(colours))

        # mostrar a sequência de cores gerada piscando os LEDs por ordem
        for colour in random_sequence:
            if colour == "red":
                for _ in range(2):
                    red.value(not red.value())
                    await asyncio.sleep(pause)
            elif colour == "green":
                for _ in range(2):
                    green.value(not green.value())
                    await asyncio.sleep(pause)
            elif colour == "blue":
                for _ in range(2):
                    blue.value(not blue.value())
                    await asyncio.sleep(pause)

        await asyncio.sleep(0.5)

        # sinalizar ao jogador que pode começar a jogada
        for _ in range(4):
            green.value(not green.value())
            await asyncio.sleep(1 / 10)

        # guardar a resposta do jogador
        moves = []
        while 1:

            if not butred.value():  # pressiona vermelho
                moves.append("red")
                await asyncio.sleep(0.3)

            if not butgreen.value():  # pressiona verde
                moves.append("green")
                await asyncio.sleep(0.3)

            if not butblue.value():  # pressiona azul
                moves.append("blue")
                await asyncio.sleep(0.3)

            if not butreset.value():  # dar reset à resposta
                moves = []
                await asyncio.sleep(0.3)

            if not butsubmit.value():  # submeter a resposta
                break

        await asyncio.sleep(1)

        # mostrar se a resposta está correta ou não
        answer = (moves == random_sequence)
        if answer:
            for _ in range(6):
                green.value(not green.value())
                await asyncio.sleep(1 / 7)
        else:
            for _ in range(6):
                red.value(not red.value())
                await asyncio.sleep(1 / 7)

            n -= 1  # repetir o nível

        # passar para o próximo nível
        n += 1

        await asyncio.sleep(2)


    # desligar os LEDs
    red.value(1)
    green.value(1)
    blue.value(1)


# Página Index
@app.route('/')
async def index_handler(r, w):
    with open("index.html") as file:
        w.write(file.read())
    await w.drain()


@app.route('/index.html')
async def index_handler2(r, w):
    with open("index.html") as file:
        w.write(file.read())
    await w.drain()


@app.route('/index.js')
async def indexjs_handler(r, w):
    with open("index.js") as file:
        w.write(file.read())
    await w.drain()


# Página jogo da memória
@app.route('/memory.html')
async def memory_handler(r, w):
    with open("memory.html") as file:
        w.write(file.read())
    await w.drain()


@app.route('/memory.js')
async def memoryjs_handler(r, w):
    with open("memory.js") as file:
        w.write(file.read())
    await w.drain()


# Página código morse
@app.route('/morse.html')
async def morse_handler(r, w):
    with open("morse.html") as file:
        w.write(file.read())
    await w.drain()


@app.route('/morse.js')
async def morsejs_handler(r, w):
    with open("morse.js") as file:
        w.write(file.read())
    await w.drain()


# Ficheiros auxiliares
@app.route('/style.css')
async def style_handler(r, w):
    with open("style.css") as file:
        w.write(file.read())
    await w.drain()


@app.route('/websocket.js')
async def websocketjs_handler(r, w):
    with open("websocket.js") as file:
        w.write(file.read())
    await w.drain()


@app.route('/ws')
async def ws_handler(r, w):
    global WS_CLIENTS

    # Upgrade Connection to WebSocket
    try:
        ws = await web.WebSocket.upgrade(r, w)
    except Exception as e:
        print("WebSocket upgrade failed: " + str(e))
        return

    # Allow reading (?)
    r.closed = False

    # Add current client to set
    WS_CLIENTS.add(ws)

    while not r.closed:
        # Handle ws events
        evt = await ws.recv()

        if evt is None or evt['type'] == 'close':
            ws.open = False
        elif evt['type'] == 'text':
            msg = evt['data']
            asyncio.create_task(receive_message(msg))

    # Remove current client from set
    WS_CLIENTS.discard(ws)


# Ver https://docs.micropython.org/en/latest/reference/constrained.html#the-heap
async def garbage_collection():
    while True:
        gc.collect()
        gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())
        await asyncio.sleep(1)


# Começar o programa
async def main():
    # Ligar a aplicação
    asyncio.create_task(app.serve())

    # Ligar a recolha de lixo
    asyncio.create_task(garbage_collection())

    # Mostrar que o programa está pronto a começar!
    await asyncio.sleep(0.2)
    turnOFF()

    # Ver se algum botão foi premido (loop infinito)
    await checkbut()


# Start event loop and create server task
asyncio.run(main())


# colour_cycle(cycles=2)
# loop.create_task(memory(difficulty=2))
# morse()


# red.value(1)
# green.value(0)
# blue.value(0)

# f=1000000
# red = PWM(Pin(25))
# red.freq(f)
# red.duty(1023)

# green = PWM(Pin(21))
# green.freq(f)
# green.duty(1023)

# blue = PWM(Pin(22))
# blue.freq(f)
# blue.duty(1023)

# r = 0
# g = 0
# b = 0

# while True:

#     if not SO.value(): # roxo
#         g = 1023
#         r = b = 0

#     if not C.value(): # branco
#         g = r = b = 0

#     if not SE.value(): # vermelho
#         g = b = 1023
#         r = 0

#     if not NO.value(): # verde
#         g = 0
#         r = b = 1023

#     if not NE.value(): # azul
#         b = 0
#         r = g = 1023

#     red.duty(r)
#     sleep_us(1)
#     red.duty(1023)
#     sleep_us(1)

#     green.duty(g)
#     sleep_us(1)
#     green.duty(1023)
#     sleep_us(1)

#     blue.duty(b)
#     sleep_us(1)
#     blue.duty(1023)
#     sleep_us(1)

