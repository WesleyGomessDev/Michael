
import os
import time

# Quadros do dinossauro dançando
poses = [
r"""
              __
             / _)
    .-^^^-/ /
 __/       /
<__.|_|-|_|
       / \__
      /_____/
""",
r"""
              __
             / _)
    .-^^^-/ /
 __/       /
<__.|_|-|_|
      __/ /
     /____/
""",
r"""
              __
             / _)
    .-^^^-/ /
 __/       /
<__.|_|-|_|
        \ \__
         \___/
""",
r"""
              __
             / _)
    .-^^^-/ /
 __/       /
<__.|_|-|_|
       __/ /
      /____/
"""
]

posicao = 30
quadro = 0
direcao = -1

try:
    while True:
        os.system("cls")

        print("=" * 48)
        print("       🦖 DINOSSAURO MOONWALK 🕺")
        print("          Jurassic Dance Club")
        print("=" * 48)
        print()

        for linha in poses[quadro % len(poses)].splitlines():
            print(" " * max(0, posicao) + linha)

        print("\n       * deslizando para tras *")

        posicao += direcao

        if posicao <= 0:
            posicao = 30
            direcao = -1

        quadro += 1
        time.sleep(0.15)

except KeyboardInterrupt:
    os.system("cls")
    print("🦖 O dinossauro encerrou a danca!")
