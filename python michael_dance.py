
import os
import time
import shutil

# Poses alternadas para simular o Moonwalk
poses = [
    r"""
 O
/|_
/ \
""",
    r"""
 O
_|\ 
/ \
""",
    r"""
 O
/|\
/  \
""",
    r"""
 O
\|_
/ \
"""
]

largura = 50
posicao = largura - 10
direcao = -1
quadro = 0

try:
    while True:
        os.system("cls")

        print("=== MICHAEL JACKSON - MOONWALK ===")
        print("Pressione Ctrl+C para sair\n")

        # Desenha o personagem na posição atual
        linhas = poses[quadro % len(poses)].strip("\n").splitlines()

        for linha in linhas:
            print(" " * max(0, posicao) + linha)

        # Move o Michael para trás
        posicao += direcao * 2

        # Quando chega à borda, muda de direção
        if posicao <= 0:
            posicao = 0
            direcao = 1
        elif posicao >= largura - 10:
            posicao = largura - 10
            direcao = -1

        quadro += 1
        time.sleep(0.12)

except KeyboardInterrupt:
    os.system("cls")
    print("Michael encerrou o Moonwalk! 🕺")
