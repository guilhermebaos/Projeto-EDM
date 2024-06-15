from games import colour_cycle, memory, morse
from machine import Pin, PWM
from time import sleep_us, sleep
import asyncio
import web

# Botões Input
NO = Pin(14, Pin.IN, Pin.PULL_UP)
NE = Pin(13, Pin.IN, Pin.PULL_UP)
SO = Pin(10, Pin.IN, Pin.PULL_UP)
SE = Pin(9, Pin.IN, Pin.PULL_UP)
C = Pin(12, Pin.IN, Pin.PULL_UP)

led = Pin(25, Pin.OUT)
led.value(0)
sleep(0.2)
led.value(1)


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


# Verificar se algum botão foi clicado
async def checkbut():
    global WS_CLIENTS
    state = True
    while True:
        if C.value() != state:
            state = not state
            msg = 'Button ' + ('OFF' if state else 'ON')
            await send_message(msg)
        await asyncio.sleep_ms(10)


# Página Index
@app.route('/')
async def index_handler(r, w):
    with open("index.html") as file:
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
            led.value(True if msg == "LED OFF" else False)

    await send_message(str(r.closed))

    # Remove current client from set
    WS_CLIENTS.discard(ws)

# Start event loop and create server task
loop = asyncio.get_event_loop()
loop.create_task(app.serve())
loop.create_task(checkbut())
# loop.create_task(memory(difficulty=2))
loop.run_forever()


# colour_cycle(cycles=2)
# asyncio.run(memory(difficulty=2))
# morse()

# red = Pin(25, Pin.OUT)
# green = Pin(21, Pin.OUT)
# blue = Pin(22, Pin.OUT)

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

