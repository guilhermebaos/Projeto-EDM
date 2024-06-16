from machine import Pin, PWM
from time import sleep
from random import choice
import asyncio


async def colour_cycle(pinr=25, ping=21, pinb=22, cycles=3, pause=0.5):
    """
    Cria um ciclo de cores (off -> vermelho -> verde -> azul -> off) no LED RGB.
    O LED RGB deve estar em lógica negativa.
    No final de execução de todos os ciclos, a cor vermelha pisca três vezes.
    --- Parâmetros ---
    - pinr: pin ao qual está ligado a perna RED
    - ping: pin ao qual está ligado a perna GREEN
    - pinb: pin ao qual está ligado a perna BLUE
    - cycles: número de ciclos
    - pause: pausa entre ciclos
    """

    # definir os sinais PWM
    f = 1_000_000

    red = PWM(Pin(pinr))
    red.freq(f)
    red.duty(1023)

    green = PWM(Pin(ping))
    green.freq(f)
    green.duty(1023)

    blue = PWM(Pin(pinb))
    blue.freq(f)
    blue.duty(1023)

    # fazer o ciclo de cores durante cycles vezes
    cycle_num = 0
    try:
        while 1:

            # quebrar o ciclo quando fizer todas as vezes
            if cycle_num == cycles:
                t1 = 0
                t2 = 1023
                # piscar o LED vermelho para mostrar que terminou
                for _ in range(6):
                    red.duty(t1)
                    await asyncio.sleep(1 / 7)
                    t1, t2 = t2, t1
                break

            # Transição desligado -> vermelho
            t = 1023
            while 1:
                if t < 0:
                    t = 0
                    break
                red.duty(t)
                await asyncio.sleep(1 / 500)
                t -= 5

            # Transição vermelho -> verde
            green.duty(0)
            while 1:
                if t > 1023:
                    t = 0
                    break
                red.duty(t)
                await asyncio.sleep(1 / 500)
                t += 1

            # Transição verde -> azul
            blue.duty(0)
            while 1:
                if t > 1023:
                    t = 0
                    break
                green.duty(t)
                await asyncio.sleep(1 / 500)
                t += 1

            # Transição azul -> desligado
            while 1:
                if t > 1023:
                    t = 0
                    break
                blue.duty(t)
                await asyncio.sleep(1 / 500)
                t += 5
            await asyncio.sleep(pause)
            cycle_num += 1

    except asyncio.CancelledError:
        pass

    # Desligar os LEDs e libertá-los para uso (desligar os sinais PWM)
    finally:
        red.deinit()
        red = Pin(pinr, Pin.OUT)
        red.value(1)

        green.deinit()
        green = Pin(ping, Pin.OUT)
        green.value(1)

        blue.deinit()
        blue = Pin(pinb, Pin.OUT)
        blue.value(1)
