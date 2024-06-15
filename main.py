from games import colour_cycle, memory, morse
from machine import Pin, PWM
from time import sleep_us, sleep
import asyncio

# colour_cycle(cycles=2)
asyncio.run(memory(difficulty=2))
# morse()

#red = Pin(25, Pin.OUT)
#green = Pin(21, Pin.OUT)
#blue = Pin(22, Pin.OUT)

#red.value(1)
#green.value(0)
#blue.value(0)

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

# NO = Pin(14, Pin.IN, Pin.PULL_UP)
# NE = Pin(13, Pin.IN, Pin.PULL_UP)
# SO = Pin(10, Pin.IN, Pin.PULL_UP)
# SE = Pin(9, Pin.IN, Pin.PULL_UP)
# C = Pin(12, Pin.IN, Pin.PULL_UP)

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

