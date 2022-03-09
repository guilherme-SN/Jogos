from random import randint


def numera():
    c = 1
    for i in range(2, -1, -1):
        for j in range(3):
            tabn[i][j] = c
            c += 1


def criaTab(jogada=0):
    print('\n+---+---+---+')
    for i in range(3):
        for j in range(3):
            if j == 2:
                print('| {} |'.format(tabn[i][j]), end='')
            else:
                print('| {} '.format(tabn[i][j]), end='')
        print('\n+---+---+---+')


def trocaP(j):
    if j == 1:
        j = -1
    elif j == -1:
        j = 1
    return j


def verifica():
    g = ''
    for i in range(3):
        soma1 = 0
        soma2 = 0
        for j in range(3):
            soma1 += tabp[i][j]
            soma2 += tabp[j][i]
        if soma1 == 3 or soma2 == 3:
            g = 'Jogador 1'
        elif soma1 == -3 or soma2 == -3:
            g = 'Jogador 2'

    if g == '':
        d1 = tabp[0][0] + tabp[1][1] + tabp[2][2]
        d2 = tabp[0][2] + tabp[1][1] + tabp[2][0]
        if d1 == 3 or d2 == 3:
            g = 'Jogador 1'
        elif d1 == -3 or d2 == -3:
            g = 'Jogador 2'
    res = 0
    if g == '':
        for i in tabp:
            res += i.count(0)
        if res == 0:
            g = 'Empate'
    return g


# Programa principal

tabn = [['', '', ''], ['', '', ''], ['', '', '']]
tabp = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
numera()

ganhador = ''
jogador = 1
valida = False

criaTab()

while True:
    while not valida:
        if jogador == 1:
            jog = int(input('Deseja jogar X em qual posição? '))
        elif jogador == -1:
            jog = int(input('Deseja jogar O em qual posição? '))
            # jog = randint(0, 9)   AI sem o I
        for i in range(0, 3):
            for j in range(0, 3):
                if jog == tabn[i][j] and tabp[i][j] == 0:
                    if jogador == 1:
                        tabn[i][j] = '\033[32;1mX\033[m'
                        tabp[i][j] = 1
                        valida = True
                    elif jogador == -1:
                        tabn[i][j] = '\033[31;1mO\033[m'
                        tabp[i][j] = -1
                        valida = True
    valida = False
    criaTab(jog)
    jogador = trocaP(jogador)
    ganhador = verifica()
    if ganhador != '':
        break

if ganhador == 'Empate':
    print('\033[33;1mO jogo deu EMPATE\033[m')
else:
    print('O ganhador da partida foi ==> \033[33;1;40m{}\033[m'.format(ganhador))
