import pygame
import random
import os
from colorama import Fore, Back, Style

print("Jogo da cobrinha")
print("-"*30)
nome = input("Nome do Jogador: ")
pontos = []

pygame.init()
pygame.display.set_caption("Jogo da cobrinha")
largura, altura = 1200, 800
tela =pygame.display.set_mode((largura, altura))
relogio = pygame.time.Clock()


preta = (0, 0, 0)
branca = (255, 255, 255)
vermelha = (255, 0, 0)
azul = (0, 0, 255)
verde = (0, 255, 0)


tamanho_snake = 20
velocidade_jogo = 15

def gerar_comida():
    comida_x = (random.randrange(0, (largura - tamanho_snake)) // tamanho_snake) * tamanho_snake
    comida_y = (random.randrange(0, (altura - tamanho_snake)) // tamanho_snake) * tamanho_snake

    return comida_x, comida_y


def desenhar_comida(tamanho, comida_x, comida_y):
    pygame.draw.rect(tela, verde, [comida_x, comida_y, tamanho, tamanho])


def desenhar_cobra(tamanho, pixels):
    for pixel in pixels:
        pygame.draw.rect(tela, branca, [pixel[0], pixel[1], tamanho, tamanho])

def desenhar_pontuacao(pontuacao):
    fonte = pygame.font.SysFont('Helvetica', 35)
    texto = fonte.render(f'Pontuação: {pontuacao}', True, azul)
    tela.blit(texto, [1, 40])

def desenhar_nome(nome_jogador):
    fonte = pygame.font.SysFont('Helvetica', 35)
    texto = fonte.render(f'Jogador: {nome_jogador}', True, azul)
    tela.blit(texto, [1, 1])

def selecionar_velocidade(tecla):
    if tecla == pygame.K_DOWN:
        velocidade_x = 0
        velocidade_y = tamanho_snake

    elif tecla == pygame.K_UP:
        velocidade_x = 0
        velocidade_y = -tamanho_snake

    elif tecla == pygame.K_RIGHT:
        velocidade_x = tamanho_snake
        velocidade_y = 0

    elif tecla == pygame.K_LEFT:
        velocidade_x = -tamanho_snake
        velocidade_y = 0


    return velocidade_x, velocidade_y

def rodar_jogo():
    fim_jogo = False

    x = largura / 2
    y = altura / 2

    velocidade_x = 0
    velocidade_y = 0
    tamanho_cobrinha = 1
    pixels = []
    pontuacao_total = 0

    comida_x, comida_y = gerar_comida()

    while not fim_jogo:
        tela.fill(preta)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                fim_jogo = True

            elif evento.type == pygame.KEYDOWN:
                velocidade_x, velocidade_y = selecionar_velocidade(evento.key)

        desenhar_comida(tamanho_snake, comida_x, comida_y)

        x += velocidade_x
        y += velocidade_y

        # atualizar posicao da cobra
        if x < 0 or x >= largura or y < 0 or y >= altura:
            fim_jogo = True

        # desenhar_cobra
        pixels.append([x, y])
        if len(pixels) > tamanho_cobrinha:
            del pixels[0]

        # verificando se a cobrinha bateu no proprio corpo
        for pixel in pixels[:-1]:
            if pixel == [x, y]:
                fim_jogo = True

        desenhar_cobra(tamanho_snake, pixels)

        desenhar_pontuacao(tamanho_cobrinha - 1)

        desenhar_nome(nome)

        pygame.display.update()

        # criar nova comida
        if x == comida_x and y == comida_y:
            tamanho_cobrinha += 1
            pontuacao_total += 1
            comida_x, comida_y = gerar_comida()


        relogio.tick(velocidade_jogo)
        
    pontos.append(pontuacao_total)


def salvar_ranking():
    dados = []
    if os.path.isfile("Ranking_jogo_cobrinha.txt"):
        with open("Ranking_jogo_cobrinha.txt", "r") as arq:
            dados = arq.readlines()

    if pontos:
        dados.append(f"{nome};{pontos[-1]}\n") 
        with open("Ranking_jogo_cobrinha.txt", "w") as arq:
            for linha in dados:
                arq.write(linha)

def mostrar_pontuacao():
    dados = []
    if os.path.isfile("Ranking_jogo_cobrinha.txt"):
        with open("Ranking_jogo_cobrinha.txt", "r") as arq:
            dados = arq.readlines()

    jogadores = []
    pontuacoes = []
    for linha in dados:
        partes = linha.strip().split(";")
        if len(partes) == 2 and partes[1].isdigit():
            jogadores.append(partes[0])
            pontuacoes.append(int(partes[1]))

    juntos = sorted(zip(pontuacoes, jogadores), reverse=True)

    print("Ranking do Jogo Snake")
    print("-----------------------------------------------------")
    print("Nº Nome do Jogador..............: Pontos")

    for pos, (ponto, jogador) in enumerate(juntos, start=1):
        if jogador == nome:
            print(Fore.RED + f"{pos:2d} {jogador:30s}   {ponto:2d}" + Style.RESET_ALL)
        else:
            print(f"{pos:2d} {jogador:30s}   {ponto:2d}")

while True:
    print("1. Iniciar o jogo")
    print("2. Visualizar Ranking do Snake.io")
    print("3. Finalizar")
    opcao = int(input("Opção: "))
    if opcao == 1:
        rodar_jogo()
        salvar_ranking()
        mostrar_pontuacao()
        break
    elif opcao == 2:
        mostrar_pontuacao()
    elif opcao == 3:
        break
    else:
        break