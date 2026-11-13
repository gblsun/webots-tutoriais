"""Gera os mundos/PROTO dos tutoriais 1-8 do Webots (R2025a) com identidade propria.

Tema: "Oficina" -- piso em tacos escuros, paredes azul-cobalto, layout proprio,
nomes e textos em portugues. Uso: python ferramentas/gerar_mundos.py
(regrava os .wbt e o .proto deste repositorio). Os valores exigidos por cada tutorial (tamanhos,
massas, raios, nomes de dispositivos, DEFs citados no texto) sao mantidos.
"""
import math
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P1 = os.path.join(RAIZ, "my_first_simulation")
P8 = os.path.join(RAIZ, "my_supervisor")
GH = "https://raw.githubusercontent.com/cyberbotics/webots/R2025a/projects/"

BG = "objects/backgrounds/protos/TexturedBackground.proto"
BGL = "objects/backgrounds/protos/TexturedBackgroundLight.proto"
ARENA = "objects/floors/protos/RectangleArena.proto"
FLOOR = "objects/floors/protos/Floor.proto"
BOX = "objects/factory/containers/protos/WoodenBox.proto"
EPUCK = "robots/gctronic/e-puck/protos/E-puck.proto"
PARQ = "appearances/protos/Parquetry.proto"
STEEL = "appearances/protos/OldSteel.proto"

# ---------------- paleta da "Oficina" ----------------
COBALTO = "0.13 0.3 0.62"        # paredes (tutorial 3 pede azul)
CINZA_QUENTE = "0.76 0.73 0.68"  # paredes antes do tutorial de aparencia
VERMELHO = "0.78 0.16 0.12"      # corpo do robo de 4 rodas (tutorial 6 pede vermelho)
VERDE = "0.18 0.62 0.32"         # rodas (tutorial 6 pede verde)
AZUL_SENSOR = "0.15 0.45 0.9"    # sensores (tutorial 6 pede azul)


def ext(*paths):
    return "".join(f'EXTERNPROTO "{GH}{p}"\n' for p in paths)


def view(pos, tgt=(0, 0, 0)):
    """Viewpoint olhando de `pos` para `tgt` (camera do Webots: x para frente, z para cima)."""
    dx, dy, dz = [t - p for p, t in zip(pos, tgt)]
    yaw = math.atan2(dy, dx)
    pitch = math.atan2(-dz, math.hypot(dx, dy))
    cy, sy, cp, sp = math.cos(yaw), math.sin(yaw), math.cos(pitch), math.sin(pitch)
    r = [[cy * cp, -sy, cy * sp], [sy * cp, cy, sy * sp], [-sp, 0, cp]]
    a = math.acos(max(-1.0, min(1.0, (r[0][0] + r[1][1] + r[2][2] - 1) / 2)))
    x, y, z = r[2][1] - r[1][2], r[0][2] - r[2][0], r[1][0] - r[0][1]
    n = math.sqrt(x * x + y * y + z * z)
    o = " ".join(f"{v:.4f}" for v in (x / n, y / n, z / n, a))
    p = " ".join(f"{v:g}" for v in pos)
    return f"Viewpoint {{\n  orientation {o}\n  position {p}\n}}\n"


def world_info(title, info, step=16, extra=""):
    lines = "".join(f'    "{i}"\n' for i in info)
    st = f"  basicTimeStep {step}\n" if step else ""
    return f'WorldInfo {{\n  info [\n{lines}  ]\n  title "{title}"\n{st}{extra}}}\n'


SKY = "TexturedBackground {\n}\nTexturedBackgroundLight {\n}\n"

PISO = """Floor {
  size 1 1
  tileSize 0.25 0.25
  appearance Parquetry {
    type "dark strip"
  }
}
"""

# Caixas: fora do centro, cada uma com rotacao propria (tutorial 1, hands-on #4).
CAIXAS = """DEF CAIXA_A WoodenBox {
  translation 0.3 0.3 0.05
  rotation 0 0 1 0.6
  name "caixa A"
  size 0.1 0.1 0.1
  mass 0.2
}
DEF CAIXA_B WoodenBox {
  translation -0.3 -0.3 0.05
  rotation 0 0 1 -0.25
  name "caixa B"
  size 0.1 0.1 0.1
  mass 0.2
}
DEF CAIXA_C WoodenBox {
  translation 0.35 -0.08 0.05
  rotation 0 0 1 1.1
  name "caixa C"
  size 0.1 0.1 0.1
  mass 0.2
}
"""


def epuck(ctrl):
    # comeca na metade oeste, olhando para +x (a bola de tijolo fica logo a frente)
    return f'DEF EXPLORADOR E-puck {{\n  translation -0.25 0.1 0\n  name "explorador"\n  controller "{ctrl}"\n}}\n'


def bolas(com_aparencia):
    if com_aparencia:
        # tutorial 3: textura de tijolo do disco (hands-on #4) e OldSteel (hands-on #3)
        ap1 = """PBRAppearance {
        baseColorMap ImageTexture {
          url [
            "textures/red_brick_wall.jpg"
          ]
        }
        roughness 0.5
        metalness 0
      }"""
        ap2 = "OldSteel {\n      }"
        n1, n2, d2 = "bola de tijolo", "bola de aco", "BOLA_ACO"
    else:
        ap1 = ap2 = "PBRAppearance {\n        roughness 1\n        metalness 0\n      }"
        n1, n2, d2 = "bola 1", "bola 2", "BOLA_2"
    return f"""DEF BOLA_TIJOLO Solid {{
  translation -0.05 0.1 0.2
  children [
    Shape {{
      appearance {ap1}
      geometry DEF BALL_GEOMETRY Sphere {{
        radius 0.05
        subdivision 2
      }}
    }}
  ]
  name "{n1}"
  boundingObject USE BALL_GEOMETRY
  physics Physics {{
  }}
}}
DEF {d2} Solid {{
  translation 0.15 -0.22 0.2
  children [
    DEF BOLA_2_SHAPE Shape {{
      appearance {ap2}
      geometry Sphere {{
        radius 0.05
        subdivision 2
      }}
    }}
  ]
  name "{n2}"
  boundingObject USE BOLA_2_SHAPE
  physics Physics {{
  }}
}}
"""


def paredes(cor, rough):
    """Quatro paredes sem fisica, todas usando uma unica definicao de Shape (tutorial 2, #8)."""
    s = f"""DEF PAREDE_LESTE Solid {{
  translation 0.5 0 0.05
  children [
    DEF WALL_SHAPE Shape {{
      appearance PBRAppearance {{
        baseColor {cor}
        roughness {rough}
        metalness 0
      }}
      geometry Box {{
        size 0.02 0.98 0.1
      }}
    }}
  ]
  name "parede leste"
  boundingObject USE WALL_SHAPE
}}
"""
    for nome, t, rot in [("OESTE", "-0.5 0 0.05", None),
                         ("SUL", "0 -0.5 0.05", "0 0 1 1.5708"),
                         ("NORTE", "0 0.5 0.05", "0 0 1 1.5708")]:
        r = f"  rotation {rot}\n" if rot else ""
        s += f"""DEF PAREDE_{nome} Solid {{
  translation {t}
{r}  children [
    USE WALL_SHAPE
  ]
  name "parede {nome.lower()}"
  boundingObject USE WALL_SHAPE
}}
"""
    return s


HALTERE = """DEF HALTERE Solid {
  translation -0.1 -0.25 0.1
  rotation 0 1 0 1.5708
  children [
    DEF G0 Group {
      children [
        Shape {
          appearance DEF METAL_ESCOVADO PBRAppearance {
            baseColor 0.55 0.57 0.6
            roughness 0.35
            metalness 0.8
          }
          geometry Cylinder {
            height 0.1
            radius 0.01
          }
        }
        Pose {
          translation 0 0 0.05
          children [
            DEF PESO Shape {
              appearance DEF FERRO_FUNDIDO PBRAppearance {
                baseColor 0.12 0.12 0.13
                roughness 0.8
                metalness 0.4
              }
              geometry Sphere {
                radius 0.03
                subdivision 2
              }
            }
          ]
        }
        Pose {
          translation 0 0 -0.05
          children [
            USE PESO
          ]
        }
      ]
    }
  ]
  name "haltere"
  contactMaterial "dumbbell"
  boundingObject USE G0
  physics Physics {
    density -1
    mass 2
    centerOfMass [
      0 0 0.01
    ]
  }
}
"""

CONTATO = """  contactProperties [
    ContactProperties {
      material1 "default"
      material2 "dumbbell"
      coulombFriction [
        1
      ]
    }
  ]
"""


def roda(n, x, y):
    forma = f"""DEF WHEEL Shape {{
            appearance PBRAppearance {{
              baseColor {VERDE}
              roughness 0.9
              metalness 0
            }}
            geometry Cylinder {{
              height 0.02
              radius 0.04
              subdivision 24
            }}
          }}""" if n == 1 else "USE WHEEL"
    fis = "DEF WHEEL_PH Physics {\n        }" if n == 1 else "USE WHEEL_PH"
    return f"""    DEF WHEEL{n} HingeJoint {{
      jointParameters HingeJointParameters {{
        axis 0 1 0
        anchor {x} {y} 0
      }}
      device [
        RotationalMotor {{
          name "wheel{n}"
        }}
      ]
      endPoint Solid {{
        translation {x} {y} 0
        rotation 1 0 0 1.5708
        children [
          {forma}
        ]
        name "roda {n}"
        boundingObject USE WHEEL
        physics {fis}
      }}
    }}
"""


def sensor(nome, y, ang, primeiro):
    forma = f"""DEF DS_SHAPE Shape {{
          appearance PBRAppearance {{
            baseColor {AZUL_SENSOR}
            roughness 0.4
            metalness 0
          }}
          geometry Box {{
            size 0.01 0.01 0.01
          }}
        }}""" if primeiro else "USE DS_SHAPE"
    return f"""    DEF {nome.upper()} DistanceSensor {{
      translation 0.1 {y} 0
      rotation 0 0 1 {ang}
      children [
        {forma}
      ]
      name "{nome}"
      boundingObject USE DS_SHAPE
    }}
"""


def filhos_robo():
    return (f"""    DEF BODY Shape {{
      appearance PBRAppearance {{
        baseColor {VERMELHO}
        roughness 0.6
        metalness 0
      }}
      geometry Box {{
        size 0.2 0.1 0.05
      }}
    }}
""" + roda(1, 0.05, 0.06) + roda(2, 0.05, -0.06) + roda(3, -0.05, 0.06)
            + roda(4, -0.05, -0.06)
            + sensor("ds_right", -0.03, -0.3, True) + sensor("ds_left", 0.03, 0.3, False))


ROBO_4_RODAS = ("""DEF CARRINHO Robot {
  translation -0.2 -0.15 0.04
  rotation 0 0 1 0.6
  children [
""" + filhos_robo() + """  ]
  name "carrinho"
  boundingObject USE BODY
  physics Physics {
    density -1
    mass 1
  }
  controller "four_wheels_collision_avoidance"
}
""")

PROTO = ("""#VRML_SIM R2025a utf8
# Tutorial 7: Your First PROTO -- robo de 4 rodas da "Oficina".
# Campos pedidos pelo tutorial: translation, rotation, bodyMass.
# Extras: name (para varias instancias no mesmo mundo) e controller.

PROTO FourWheelsRobot [
  field SFVec3f    translation  0 0 0.04
  field SFRotation rotation     0 0 1 0
  field SFString   name         "carrinho"
  field SFFloat    bodyMass     1
  field SFString   controller   "four_wheels_collision_avoidance"
]
{
  Robot {
    translation IS translation
    rotation IS rotation
    children [
""" + "".join("    " + l + "\n" for l in filhos_robo().rstrip("\n").split("\n")) + """    ]
    name IS name
    boundingObject USE BODY
    physics Physics {
      density -1
      mass IS bodyMass
    }
    controller IS controller
  }
}
""")

files = {}

files["worlds/my_first_simulation.wbt"] = (
    "#VRML_SIM R2025a utf8\n\n" + ext(BG, BGL, ARENA, PARQ, BOX, EPUCK) + "\n"
    + world_info("Oficina - T1: primeira simulacao",
                 ["Tutorial 1: arena, tres caixas e o e-puck andando para frente."])
    + view((-0.95, -0.85, 0.75), (0, 0, 0)) + SKY
    + """RectangleArena {
  floorTileSize 0.25 0.25
  floorAppearance Parquetry {
    type "dark strip"
  }
  wallHeight 0.05
}
""" + CAIXAS + epuck("epuck_go_forward"))

files["worlds/obstacles.wbt"] = (
    "#VRML_SIM R2025a utf8\n\n" + ext(BG, BGL, FLOOR, PARQ, BOX, EPUCK) + "\n"
    + world_info("Oficina - T2: obstaculos",
                 ["Tutorial 2: piso simples, duas bolas com fisica (DEF/USE) e paredes."])
    + view((-0.9, 0.95, 0.85), (0, 0, 0)) + SKY + PISO + CAIXAS
    + epuck("epuck_go_forward") + bolas(False) + paredes(CINZA_QUENTE, "1"))

files["worlds/appearance.wbt"] = (
    "#VRML_SIM R2025a utf8\n\n" + ext(BG, BGL, FLOOR, PARQ, STEEL, BOX, EPUCK) + "\n"
    + world_info("Oficina - T3: aparencia",
                 ["Tutorial 3: paredes azul-cobalto, bola de tijolo (textura local) e bola OldSteel."])
    + view((-0.55, -0.6, 0.4), (0, 0, 0.05)) + SKY + PISO + CAIXAS
    + epuck("epuck_go_forward") + bolas(True) + paredes(COBALTO, "0.5"))

files["worlds/collision_avoidance.wbt"] = (
    "#VRML_SIM R2025a utf8\n\n" + ext(BG, BGL, FLOOR, PARQ, STEEL, BOX, EPUCK) + "\n"
    + world_info("Oficina - T4: desvio de colisao",
                 ["Tutorial 4: o e-puck le os 8 sensores IR e desvia de caixas, bolas e paredes."])
    + view((-0.2, -1.05, 1.1), (0, 0, 0)) + SKY + PISO + CAIXAS
    + epuck("epuck_avoid_collision") + bolas(True) + paredes(COBALTO, "0.5"))

files["worlds/compound_solid.wbt"] = (
    "#VRML_SIM R2025a utf8\n\n" + ext(BG, BGL, FLOOR, PARQ, STEEL, BOX, EPUCK) + "\n"
    + world_info("Oficina - T5: solido composto",
                 ["Tutorial 5: haltere de 2 kg (cilindro + 2 esferas), centro de massa deslocado",
                  "e ContactProperties default/dumbbell (troque coulombFriction para 0 e veja deslizar)."],
                 extra=CONTATO)
    + view((-0.6, -0.75, 0.45), (-0.1, -0.2, 0.05)) + SKY + PISO + CAIXAS
    + epuck("epuck_avoid_collision") + bolas(True) + paredes(COBALTO, "0.5") + HALTERE)

files["worlds/4_wheels_robot.wbt"] = (
    "#VRML_SIM R2025a utf8\n\n" + ext(BG, BGL, FLOOR, PARQ) + "\n"
    + world_info("Oficina - T6: robo de 4 rodas",
                 ["Tutorial 6: robo feito do zero -- corpo, 4 HingeJoints com motor e 2 sensores de distancia."])
    + view((0.85, -0.9, 0.8), (0, 0, 0)) + SKY + PISO + paredes(COBALTO, "0.5") + ROBO_4_RODAS)

files["protos/FourWheelsRobot.proto"] = PROTO

files["worlds/4_wheels_robot_proto.wbt"] = (
    "#VRML_SIM R2025a utf8\n\n" + ext(BG, BGL, FLOOR, PARQ)
    + 'EXTERNPROTO "../protos/FourWheelsRobot.proto"\n\n'
    + world_info("Oficina - T7: primeiro PROTO",
                 ["Tutorial 7: dois robos criados a partir do PROTO FourWheelsRobot."])
    + view((0, -1.1, 1.0), (0, 0, 0)) + SKY + PISO + paredes(COBALTO, "0.5")
    + """FourWheelsRobot {
  translation -0.2 -0.15 0.04
  rotation 0 0 1 0.6
  name "carrinho"
}
FourWheelsRobot {
  translation 0.2 0.25 0.04
  rotation 0 0 1 -2.4
  name "carrinho pesado"
  bodyMass 2
}
""")

for rel, content in files.items():
    path = os.path.join(P1, rel)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print("wrote", path)

sup = ("#VRML_SIM R2025a utf8\n\n" + ext(BG, BGL, ARENA, PARQ, "robots/sphero/bb8/protos/BB-8.proto")
       + "IMPORTABLE " + ext("robots/softbank/nao/protos/Nao.proto")
       + "IMPORTABLE " + ext("objects/balls/protos/Ball.proto") + "\n"
       + world_info("Oficina - T8: supervisor",
                    ["Tutorial 8: o supervisor teleporta e remove o BB-8, cria o Nao",
                     "e acompanha uma bola que fica vermelha ao tocar o chao."], step=16)
       + view((-3.2, -5.2, 4.2), (0.8, 0.3, 0)) + SKY
       + """RectangleArena {
  floorSize 10 10
  floorTileSize 1 1
  floorAppearance Parquetry {
    type "mosaic"
  }
}
DEF BB-8 BB-8 {
  translation -1 -1 0
  controller "<none>"
}
Robot {
  name "supervisor"
  controller "supervisor_controller"
  supervisor TRUE
}
""")
path = os.path.join(P8, "worlds", "my_supervisor.wbt")
with open(path, "w", encoding="utf-8", newline="\n") as f:
    f.write(sup)
print("wrote", path)
