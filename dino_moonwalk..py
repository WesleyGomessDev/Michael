
import os
import time
from PIL import Image

CAMINHO = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "5Wu4.gif"
)

CARACTERES = " .:-=+*#%@"

def converter(frame, largura=60):
    frame = frame.convert("RGB")
    altura = max(1, int(frame.height / frame.width * largura * 0.45))
    frame = frame.resize((largura, altura))

    linhas = []
    for y in range(altura):
        linha = ""
        for x in range(largura):
            r, g, b = frame.getpixel((x, y))
            brilho = (r + g + b) // 3
            indice = brilho * (len(CARACTERES) - 1) // 255
            linha += CARACTERES[indice]
        linhas.append(linha)

    return "\n".join(linhas)

try:
    gif = Image.open(CAMINHO)
    quadros = []

    for i in range(gif.n_frames):
        gif.seek(i)
        desenho = converter(gif.copy())
        duracao = gif.info.get("duration", 80) / 1000
        quadros.append((desenho, max(0.02, duracao)))

    while True:
        for desenho, duracao in quadros:
            os.system("cls")
            print("  DINOSSAURO FAZENDO MOONWALK!")
            print("  Pressione Ctrl+C para sair\n")
            print(desenho)
            time.sleep(duracao)

except ImportError:
    print("Instale o Pillow: python -m pip install pillow")
except FileNotFoundError:
    print("Não encontrei o arquivo 5Wu4.gif.")
except KeyboardInterrupt:
    print("\nDança encerrada!")

