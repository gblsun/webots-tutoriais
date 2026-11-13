"""Oficina - Tutorial 6: o carrinho de 4 rodas desvia de obstaculos.

Dois sensores de distancia (ds_left/ds_right) olham para frente, abertos
0.3 rad. Leitura abaixo de 950 = obstaculo a menos de ~10 cm: o carrinho gira
no proprio eixo por 100 passos e depois volta a andar em frente.
"""
from controller import Robot

PASSO_MS = 64
VELOCIDADE = 1.0            # rad/s nas rodas
LIMIAR_OBSTACULO = 950.0    # lookupTable padrao: 1000 = nada a vista
PASSOS_DE_DESVIO = 100

robo = Robot()

sensores = []
for nome in ('ds_right', 'ds_left'):
    s = robo.getDevice(nome)
    s.enable(PASSO_MS)
    sensores.append(s)

# wheel1/wheel3 ficam do lado esquerdo, wheel2/wheel4 do lado direito
rodas = []
for i in range(1, 5):
    r = robo.getDevice(f'wheel{i}')
    r.setPosition(float('inf'))
    r.setVelocity(0.0)
    rodas.append(r)
rodas_esq = (rodas[0], rodas[2])
rodas_dir = (rodas[1], rodas[3])

contador_desvio = 0
while robo.step(PASSO_MS) != -1:
    vel_esq = vel_dir = VELOCIDADE
    if contador_desvio > 0:
        contador_desvio -= 1
        vel_dir = -VELOCIDADE           # gira no proprio eixo
    elif any(s.getValue() < LIMIAR_OBSTACULO for s in sensores):
        contador_desvio = PASSOS_DE_DESVIO
        print(f"[{robo.getName()} {robo.getTime():7.2f} s] obstaculo! desviando")

    for r in rodas_esq:
        r.setVelocity(vel_esq)
    for r in rodas_dir:
        r.setVelocity(vel_dir)
