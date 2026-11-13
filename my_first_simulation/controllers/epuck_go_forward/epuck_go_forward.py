"""Oficina - Tutorial 1: o explorador (e-puck) anda em linha reta, devagar.

Os motores ficam em modo de controle de velocidade (posicao alvo infinita)
e giram a 10% da velocidade maxima.
"""
from controller import Robot

PASSO_MS = 64             # multiplo do basicTimeStep (16 ms)
VELOCIDADE_MAX = 6.28     # rad/s, limite dos motores do e-puck
FRACAO_VELOCIDADE = 0.1   # 10% da maxima, como pede o tutorial

robo = Robot()

motor_esq = robo.getDevice('left wheel motor')
motor_dir = robo.getDevice('right wheel motor')
for motor in (motor_esq, motor_dir):
    motor.setPosition(float('inf'))   # modo velocidade
    motor.setVelocity(FRACAO_VELOCIDADE * VELOCIDADE_MAX)

print(f"[{robo.getName()}] seguindo em frente a {FRACAO_VELOCIDADE * VELOCIDADE_MAX:.2f} rad/s")

while robo.step(PASSO_MS) != -1:
    pass
