# Projeto_CGPI
# Grupo: Cinthia Alves Barreto, Isabel Cavalcante Motta, Isabella Rubio Venancio

from tkinter import Tk, messagebox
import cv2
from tkinter import *
from tkinter.ttk import *
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import matplotlib


# janela do explorador de arquivos
janela = Tk()
# inicializando a imagem como null
img = None
arquivo = None
ult = None

def filtro_punch(imagem):
    # Aplicar um filtro de nitidez (kernel Laplaciano)
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], dtype=np.float32)

    imagem_punch = cv2.filter2D(imagem, -1, kernel)

    return imagem_punch


def distorcao_barril(imagem, intensidade=0.2):
    # Obter as dimensões da imagem
    altura, largura = imagem.shape[:2]

    # Criar uma grade de coordenadas para mapeamento
    mapa_x, mapa_y = np.meshgrid(np.arange(largura), np.arange(altura))

    # Calcular o centro da imagem
    centro_x, centro_y = largura // 2, altura // 2

    # Calcular as distâncias dos pixels ao centro
    distancias = np.sqrt((mapa_x - centro_x) ** 2 + (mapa_y - centro_y) ** 2)

    # Calcular a distorção de barril
    distorcao = 1.0 + intensidade * distancias / np.max(distancias)

    # Aplicar a distorção de barril
    mapa_x_dist, mapa_y_dist = (
        distorcao * (mapa_x - centro_x) + centro_x,
        distorcao * (mapa_y - centro_y) + centro_y,
    )

    # Remapear a imagem usando a interpolação bilinear
    imagem_distorcida = cv2.remap(
        imagem,
        mapa_x_dist.astype(np.float32),
        mapa_y_dist.astype(np.float32),
        interpolation=cv2.INTER_LINEAR,
    )

    return imagem_distorcida


# seleciona a imagem
def procurarImagem():
    # precisa ser global senao ele vai usar a variavel local
    global img, img_label, arquivo, ult
    arquivo = filedialog.askopenfilename(
        initialdir="/",
        title="Select a File",
        filetypes=(("Text files", "*.jpg*"), ("all files", "*.*")),
    )
    # atualiza a informaçao para a variavel global
    janela.state('zoomed') # maximiza a janela
    
    img2 = Image.open(arquivo) # abre o arquivo
    
    render = ImageTk.PhotoImage(img2) # renderizador(converte a imagem pata ser mostrada no tkinter)

    # serve para alterar qualquer coisa durante o processo
    img_label.configure(image=render)

    img_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    # imagem precisa trazer os dados
    img_label.image = render

    # coloca a imagem na janela
    botao_histograma.grid(row=0, column=2, sticky=W, pady=3)
    botao_PretoeBranco.grid(row=0, column=4, sticky=W, pady=3)
    botao_cinza.grid(row=0, column=5, sticky=W, pady=3)
    botao_prism.grid(row=0, column=8, sticky=W, pady=3)
    botao_winter.grid(row=0, column=6, sticky=W, pady=3)
    botao_magma.grid(row=0, column=7, sticky=W, pady=3)
    botao_RAINBOW.grid(row=0, column=9, sticky=W, pady=3)
    botao_original.grid(row=0, column=3, sticky=W, pady=3)
    botao_punch.grid(row=0, column=10, sticky=W, pady=3)
    botao_barril.grid(row=0, column=11, sticky=W, pady=3)
    img_label.grid(row=1, sticky=W, columnspan=15, pady=0)
    applyoriginal()


# define titulo da janela
janela.title("Processamento de Imagens")

# define a cor do fundo
janela.config(background="white")




def applyhistograma():
    global ult
    if ult == 0:
        img = cv2.imread(arquivo)
        filter_name = "Original"
    elif ult == 1:
        img = cv2.imread(arquivo, cv2.IMREAD_GRAYSCALE)
        limiar, img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)
        filter_name = "Preto e Branco"
    elif ult == 2:
        img = cv2.imread(arquivo, cv2.IMREAD_GRAYSCALE)
        filter_name = "Cinza"
    elif ult == 3:
        img = cv2.imread(arquivo, cv2.IMREAD_GRAYSCALE)
        mapa_cores = cv2.COLORMAP_JET
        filter_name = "Prism"
    elif ult == 4:
        img = cv2.imread(arquivo, cv2.IMREAD_GRAYSCALE)
        mapa_cores = cv2.COLORMAP_WINTER
        filter_name = "Winter"
    elif ult == 5:
        img = cv2.imread(arquivo, cv2.IMREAD_GRAYSCALE)
        mapa_cores = cv2.COLORMAP_MAGMA
        filter_name = "Magma"
    elif ult == 6:
        img = cv2.imread(arquivo)
        img = distorcao_barril(img, intensidade=0.2)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        filter_name = "Distorção de Barril"
    elif ult == 7:
        img = cv2.imread(arquivo, cv2.IMREAD_GRAYSCALE)
        img = filtro_punch(img)
        filter_name = "Punch"
    elif ult == 8:
        img = cv2.imread(arquivo, cv2.IMREAD_GRAYSCALE)
        mapa_cores = cv2.COLORMAP_RAINBOW
        filter_name = "RAINBOW"

    if ult != 0 and ult != 2 and ult != 1 and ult != 7 and ult != 6:
        img = cv2.applyColorMap(img, mapa_cores)
    janela_histograma = Toplevel(janela)
    janela_histograma.title(f"Histograma da Imagem {filter_name}")
    janela_histograma.geometry("600x600")
    figura = Figure(figsize=(6, 4), dpi=100)
    figura_canvas = FigureCanvasTkAgg(figura, janela_histograma)
    histr = cv2.calcHist([img], [0], None, [256], [0, 256])
    plot = figura.add_subplot(111)
    plot.plot(histr)
    figura_canvas.draw()
    figura_canvas.get_tk_widget().pack()
    return

def applyoriginal():
    global ult
    ult = 0
    return


def applyPretoeBranco():
    global ult
    ult = 1
    img = cv2.imread(arquivo, 0)
    plt.imshow(img, cmap="binary")
    plt.axis("off")
    plt.show()
    return


def applyCinza():
    global ult
    ult = 2
    img = cv2.imread(arquivo, 0)
    plt.imshow(img, cmap="gray")
    plt.axis("off")
    plt.show()
    return


def applyPrism():
    global ult
    ult = 3
    img = cv2.imread(arquivo, 0)
    plt.imshow(img, cmap="prism")
    plt.axis("off")
    plt.show()
    return


def applyRAINBOW():
    global ult
    ult = 4
    img = cv2.imread(arquivo, cv2.IMREAD_GRAYSCALE)
    img = cv2.applyColorMap(img, cv2.COLORMAP_RAINBOW)
    plt.imshow(img, cmap="gray")
    plt.axis("off")
    plt.show()
    return


def applyBarril():
    global ult
    ult = 6
    img = cv2.imread(arquivo)
    img = distorcao_barril(img, intensidade=0.2)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(img, cmap="gray")
    plt.axis("off")
    plt.show()
    return


def applyWinter():
    global ult
    ult = 4
    img = cv2.imread(arquivo, 0)
    plt.imshow(img, cmap="winter")
    plt.axis("off")
    plt.show()
    return


def applyMagma():
    global ult
    ult = 5
    img = cv2.imread(arquivo, 0)
    plt.imshow(img, cmap="magma")
    plt.axis("off")
    plt.show()
    return


def applypunch():
    global ult
    ult = 7
    img = cv2.imread(arquivo, cv2.IMREAD_GRAYSCALE)
    img = filtro_punch(img)
    plt.imshow(img, cmap="magma")
    plt.axis("off")
    plt.show()
    return


# cria um botao
botao_busca = tk.Button(janela,text="Procurar\n Arquivo",command=procurarImagem, height=5, width=17, border=5)
# botao par sair do programa
botao_sair = tk.Button(janela, text="Sair", command=exit, height=5, width=7)

botao_histograma = tk.Button(janela, text="Histograma", command=applyhistograma, height=5, width=15)
botao_PretoeBranco = tk.Button(janela, text="Preto e branco", command=applyPretoeBranco, height=5, width=15)
botao_cinza = tk.Button(janela, text="Cinza", command=applyCinza, height=5, width=15)
botao_prism = tk.Button(janela, text="Prism", command=applyPrism, height=5, width=15)
botao_winter = tk.Button(janela, text="Winter", command=applyWinter, height=5, width=15)
botao_magma = tk.Button(janela, text="Magma", command=applyMagma, height=5, width=15)
botao_original = tk.Button(janela, text="Imagem Original", command=applyoriginal, height=5, width=15)
botao_RAINBOW = tk.Button(janela, text="RAINBOW", command=applyRAINBOW, height=5, width=15)
botao_punch = tk.Button(janela, text="Punch", command=applypunch, height=5, width=15)
botao_barril = tk.Button(janela, text="Distroção\n de Barril", command=applyBarril, height=5, width=15)

img_label = tk.Label(janela, width=1350, height=590, padx=10, pady=2)

botao_sair.grid(row=0, column=0, sticky=W, pady=0)

botao_busca.grid(row=0, column=1, sticky=W, pady=0)

# faz a janela esperar para algum evento acontecer
janela.mainloop()
