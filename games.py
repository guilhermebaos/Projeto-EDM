# Escreve o teu código aqui :-)

from machine import Pin, PWM
from time import sleep
from random import choice
import asyncio


def morse(pinr=25, ping=21, pinb=22):
    """
    Decifrar Código-Morse: Cria uma mensagem em código-morse (mostrada no LED RGB),
                        que o jogador deve decifrar.
    O LED RGB deve estar em lógica negativa.
    --- Parâmetros ---
    - pinr: pin ao qual está ligado a perna RED
    - ping: pin ao qual está ligado a perna GREEN
    - pinb: pin ao qual está ligado a perna BLUE
    - num_words:                         #???????????????????????????????????
    - difficulty: (nº de letras em cada) #???????????????????????????????????
    """

    # definir os LEDs
    red = Pin(pinr, Pin.OUT)
    red.value(1)
    green = Pin(ping, Pin.OUT)
    green.value(1)
    blue = Pin(pinb, Pin.OUT)
    blue.value(1)

    # definir as sequências em código-morse dos vários caracteres
    morse = {
        "A": ".--",
        "B": "-...",
        "C": "-.-.",
        "D": "-..",
        "E": ".",
        "F": "..-.",
        "G": "--.",
        "H": "....",
        "I": "..",
        "J": ".---",
        "K": "-.-",
        "L": ".-..",
        "M": "--",
        "N": "-.",
        "O": "---",
        "P": ".--.",
        "Q": "--.-",
        "R": ".-.",
        "S": "...",
        "T": "-",
        "U": "..-",
        "V": "...-",
        "W": ".--",
        "X": "-..-",
        "Y": "-.--",
        "Z": "--..",
        "0": "-----",
        "1": ".----",
        "2": "..---",
        "3": "...--",
        "4": "....-",
        "5": ".....",
        "6": "-....",
        "7": "--...",
        "8": "---..",
        "9": "----.",
    }

    # gerar a sequência de palavras do jogo
    word_sequence = ["SOS", "OK"]
    # usar um gerador de palavras aleatórias??????????????????????????????????????
    # ou simplesmente sequências de números em vez de palavras????????????????????

    # analisar cada palavra
    for word in word_sequence:

        # analisar cada caracter na palavra
        for letter in word:

            # associar o código do caracter
            code = morse[letter]
            print(letter)
            print(code)

            # mostrar no LED cada símbolo do código
            for sym in code:
                print(sym)

                blue.value(0)

                if sym == ".":
                    sleep(0.2)
                    blue.value(1)
                elif sym == "-":
                    sleep(0.6)
                    blue.value(1)
                sleep(0.4)

            sleep(1)

        sleep(3)

        # resposta do jogador

        # mostrar se está correta ou não
        answer = choice([0, 1])

        # avaliar a resposta do jogador
        if answer:
            for _ in range(6):
                green.value(not green.value())
                sleep(1 / 7)
        else:
            for _ in range(6):
                red.value(not red.value())
                sleep(1 / 7)
            # condição de repetir a palavra por ter errado?????????????????????

        sleep(3)

    return morse


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
    print("Start")

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

        await asyncio.sleep(3)
        # passar para o próximo nível
        n += 1

    # desligar os LEDs
    red.value(1)
    green.value(1)
    blue.value(1)


def colour_cycle(pinr=25, ping=21, pinb=22, cycles=3, pause=0.5):
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
        # transição desligado -> vermelho
        t = 1023
        while 1:
            if t < 0:
                t = 0
                break
            red.duty(t)
            await asyncio.sleep(1 / 500)
            t -= 5
        # transição vermelho -> verde
        green.duty(0)
        while 1:
            if t > 1023:
                t = 0
                break
            red.duty(t)
            await asyncio.sleep(1 / 500)
            t += 1
        # transição verde -> azul
        blue.duty(0)
        while 1:
            if t > 1023:
                t = 0
                break
            green.duty(t)
            await asyncio.sleep(1 / 500)
            t += 1
        # transição azul -> desligado
        while 1:
            if t > 1023:
                t = 0
                break
            blue.duty(t)
            await asyncio.sleep(1 / 500)
            t += 5
        await asyncio.sleep(pause)
        cycle_num += 1
    # desligar os LEDs, mas libertá-los para uso (desligar os sinais PWM)
    red.deinit()
    red = Pin(pinr, Pin.OUT)
    red.value(1)

    green.deinit()
    green = Pin(ping, Pin.OUT)
    green.value(1)

    blue.deinit()
    blue = Pin(pinb, Pin.OUT)
    blue.value(1)
