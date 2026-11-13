"""Oficina - Tutorial 4: o explorador (e-puck) desvia de obstaculos.

Le os 8 sensores infravermelhos (ps0..ps7). Se algo aparece a esquerda
(ps5-ps7) ele gira para a direita; se aparece a direita (ps0-ps2) ele gira
para a esquerda; senao segue em frente a meia velocidade.
"""
from controller import Robot

PASSO_MS = 64
VELOCIDADE_MAX = 6.28
LIMIAR_OBSTACULO = 80.0           # leitura IR acima disso = obstaculo perto
SENSORES_DIREITA = (0, 1, 2)      # ps0, ps1, ps2
SENSORES_ESQUERDA = (5, 6, 7)     # ps5, ps6, ps7

robo = Robot()

sensores = []
for i in range(8):
    s = robo.getDevice(f'ps{i}')
    s.enable(PASSO_MS)
    sensores.append(s)

motor_esq = robo.getDevice('left wheel motor')
motor_dir = robo.getDevice('right wheel motor')
for motor in (motor_esq, motor_dir):
    motor.setPosition(float('inf'))
    motor.setVelocity(0.0)

estado_anterior = None
while robo.step(PASSO_MS) != -1:
    # 1) ler sensores
    leituras = [s.getValue() for s in sensores]

    # 2) decidir
    obstaculo_dir = any(leituras[i] > LIMIAR_OBSTACULO for i in SENSORES_DIREITA)
    obstaculo_esq = any(leituras[i] > LIMIAR_OBSTACULO for i in SENSORES_ESQUERDA)

    vel_esq = vel_dir = 0.5 * VELOCIDADE_MAX
    estado = "em frente"
    if obstaculo_esq:
        vel_dir = -0.5 * VELOCIDADE_MAX      # gira para a direita
        estado = "girando para a direita"
    elif obstaculo_dir:
        vel_esq = -0.5 * VELOCIDADE_MAX      # gira para a esquerda
        estado = "girando para a esquerda"

    if estado != estado_anterior:
        print(f"[{robo.getTime():7.2f} s] {estado}")
        estado_anterior = estado

    # 3) atuar
    motor_esq.setVelocity(vel_esq)
    motor_dir.setVelocity(vel_dir)
