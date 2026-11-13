"""Oficina - Tutorial 8: um supervisor que mexe no mundo.

Linha do tempo (1 passo = 32 ms):
  passo 0  -> teleporta o BB-8 para (2.5, 0, 0)
  passo 10 -> remove o BB-8
  passo 20 -> cria um Nao onde o BB-8 estava
  sempre   -> acompanha a bola criada no inicio e a pinta de vermelho
              quando ela encosta no chao (limite = raio da bola + folga)
"""
from controller import Supervisor

PASSO_MS = 32
FOLGA_CONTATO = 0.005  # margem (m) acima do raio para considerar a bola no chao
VERMELHO = [1, 0, 0]

supervisor = Supervisor()

bb8 = supervisor.getFromDef('BB-8')
bb8_translacao = bb8.getField('translation')

raiz_filhos = supervisor.getRoot().getField('children')

raiz_filhos.importMFNodeFromString(-1, 'DEF BALL Ball { translation 0 1 1 }')
bola = supervisor.getFromDef('BALL')
bola_cor = bola.getField('color')
# o tutorial usa 0.2 fixo; aqui o limite segue o raio real da bola (Ball padrao: 0.0325)
altura_contato = bola.getField('radius').getSFFloat() + FOLGA_CONTATO

passo = 0
bola_no_chao = False
while supervisor.step(PASSO_MS) != -1:
    if passo == 0:
        bb8_translacao.setSFVec3f([2.5, 0, 0])
        print("BB-8 teleportado para (2.5, 0, 0)")
    elif passo == 10:
        bb8.remove()
        print("BB-8 removido")
    elif passo == 20:
        raiz_filhos.importMFNodeFromString(-1, 'Nao { translation 2.5 0 0.334 }')
        print("Nao criado em (2.5, 0, 0.334)")

    x, y, z = bola.getPosition()
    if passo % 10 == 0:
        print(f"bola em ({x:.3f}, {y:.3f}, {z:.3f})")
    if z < altura_contato and not bola_no_chao:
        bola_cor.setSFColor(VERMELHO)
        bola_no_chao = True
        print(f"bola tocou o chao em z={z:.3f} -> pintada de vermelho")

    passo += 1
