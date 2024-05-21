from machine import Pin, PWM, DAC, ADC


# Parameters
PWMfreq = 10_000


# LED output pins in PWM
RED = PWM(Pin(25), freq=PWMfreq, duty_u16=0)
GRE = PWM(Pin(21), freq=PWMfreq, duty_u16=0)
BLU = PWM(Pin(22), freq=PWMfreq, duty_u16=0)



