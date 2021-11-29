import sys
from termcolor import colored, cprint

class Node:
    # classe noh
    def __init__(self, pai=None, posicao=None):
        self.g = 0
        self.h = 0
        self.f = 0

        self.pai = pai
        self.posicao = self.set_pos_int(posicao)

    def __le__(self, other):
        return self.f <= other.f

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        if other is None:
            return False
        return self.posicao == other.posicao

    def set_pos_int(self, posicao):
        tpl_pos_int = []
        for item in posicao:
            tpl_pos_int.append(int(item))
        return tpl_pos_int


def heuristica(pAtual, pProx):
    # distancia de manhattan
    (x1, y1) = pAtual.posicao
    (x2, y2) = pProx.posicao
    return abs(x1 - x2) + abs(y1 - y2)


def astar(mapa, ini, fim):
    # instancia o no inicial e final
    noInicial = Node(None, ini)
    noInicial.g = noInicial.h = noInicial.f = 0
    noFinal = Node(None, fim)
    noFinal.g = noFinal.h = noFinal.f = 0

    # cria a "lista aberta" e a "lista fechada"
    listaAberta = []
    listaFechada = []

    # adiciona o no inicial a lista aberta
    listaAberta.append(noInicial)

    # cria uma variavel flag para saber se o alvo foi encontrado
    achou = False
    # lista que guarda o caminho percorrido ate o no final
    path = []

    # percorre o mapa ate encontrar o fim
    while achou == False:
        # pesquisa o no com menor F da lista aberta
        noCorrente = min(listaAberta)
        # remove o no corrente da lista aberta
        index = listaAberta.index(noCorrente)
        listaAberta.pop(index)
        # adiciona o no corrente na lista fechada
        listaFechada.append(noCorrente)

        for pos in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            # pega as posicoes de todos os nos adjacentes
            posAdj = (noCorrente.posicao[0] + pos[0], noCorrente.posicao[1] + pos[1])
            # cria um no com as posicoes adjacentes
            noAdjacente = Node(None, posAdj)

            if posAdj[0] < 0 or posAdj[1] < 0 or posAdj[0] >= len(mapa) or posAdj[1] >= len(mapa[-1]):
                continue
            if mapa[posAdj[0]][posAdj[1]] == 1 or noAdjacente in listaFechada:
                continue
            
            if noAdjacente not in listaAberta:
                # fazendo o no corrente ser o pai do no adjacente
                noAdjacente.pai = noCorrente              
                # calculo dos parametros g h f
                noAdjacente.g = noAdjacente.g + 10
                noAdjacente.h = heuristica(noAdjacente, noFinal)
                noAdjacente.f = noAdjacente.g + noAdjacente.h
                # adicionando na lista aberta
                listaAberta.append(noAdjacente)
            else:
                if (noAdjacente in listaAberta) and (noAdjacente.g < noCorrente.g):
                    # calculo dos parametros g h f
                    noAdjacente.g = noAdjacente.g + 10
                    noAdjacente.f = noAdjacente.g + noAdjacente.h
                    noAdjacente.pai = noCorrente

        # condiçoes de parada
        if len(listaAberta) == 0 or noCorrente == noFinal:
            no = noCorrente
            while no is not None:
                path.append(no.posicao) 
                no = no.pai  # adiciona os pais na lista path
            achou = True
    return path[::-1]  # retorna o caminho reverso


def desenha_caminho(mapa, caminho):
    for item in caminho:
        mapa[item[0]][item[1]] = '*'
    print()

    for i in range(len(mapa)):
        for j in range(len(mapa[0])):
            if mapa[i][j] == 1:
                print(' ', colored("#", 'red'), end='')
            if mapa[i][j] == 0:
                print(' ', colored("#", 'white'), end='')
            if mapa[i][j] == '*':
                print(' ', colored(mapa[i][j], 'blue'), end='')
        print()


def le_mapa(arqMapa):
    # leitura do arquivo
    with open(arqMapa, 'r') as f:
        l = [[int(num) for num in line.split(' ') if num != '\n'] for line in f]
    return l


def main():
    # leitura do mapa e dos pontos de inicio e fim por linha de comando
    mapa = le_mapa(sys.argv[1])
    ini = sys.argv[2].split(',')[0], sys.argv[2].split(',')[0]
    fim = sys.argv[3].split(',')[0], sys.argv[3].split(',')[0]

    # chamada da funcao astar
    caminho = astar(mapa, ini, fim)

    # imprime as coordenadas dos pontos percorridos
    print("Caminho percorrido: ", caminho)

    # imprime o caminho percorrido
    desenha_caminho(mapa, caminho)


if __name__ == '__main__':
    main()
