# Webots Tutoriais — "Oficina"

Versão do Grupo dos [8 tutoriais oficiais do Webots](https://cyberbotics.com/doc/guide/tutorial-1-your-first-simulation-in-webots)
(Webots **R2025a**, controladores em **Python**).

Os valores que cada tutorial exige (tamanhos, massas, raios, nomes de dispositivos,
DEFs citados no texto) foram mantidos, mas o resto tem identidade própria:
tema "Oficina", com piso em tacos escuros, paredes azul-cobalto, layout próprio
das caixas, bolas e robôs, câmeras próprias e nomes/textos em português.

## Estrutura

```
my_first_simulation/          tutoriais 1 a 7
  worlds/                     um .wbt por tutorial
  controllers/                controladores Python
  protos/FourWheelsRobot.proto
my_supervisor/                tutorial 8
ferramentas/gerar_mundos.py   gera todos os .wbt e o .proto
```

| # | Tutorial | Mundo | Controlador |
|---|---|---|---|
| 1 | Primeira simulação | `my_first_simulation.wbt` | `epuck_go_forward` |
| 2 | Modificando o ambiente | `obstacles.wbt` | `epuck_go_forward` |
| 3 | Aparência | `appearance.wbt` | `epuck_go_forward` |
| 4 | Mais sobre controladores | `collision_avoidance.wbt` | `epuck_avoid_collision` |
| 5 | Sólido composto e física | `compound_solid.wbt` | `epuck_avoid_collision` |
| 6 | Robô de 4 rodas | `4_wheels_robot.wbt` | `four_wheels_collision_avoidance` |
| 7 | Primeiro PROTO | `4_wheels_robot_proto.wbt` | `four_wheels_collision_avoidance` |
| 8 | Supervisor | `my_supervisor/worlds/my_supervisor.wbt` | `supervisor_controller` |
