# Nome: Erick Lima Figueiredo
# Matricula: ES98898

import heapq as p_queue
from copy import deepcopy

from Posicao import Posicao
from AEstrela import AEstrela
from QuebraCabeca import QuebraCabeca
from QuebraCabecaImp import QuebraCabecaImp


class GameState:
    def __init__(self, qc, parent, g):
        self.__qc = qc
        self.__parent = parent
        self.__g = g
        self.__f = g + qc.getValor()

    @property
    def g(self): return self.__g
    
    @g.setter
    def g(self, g):
        self.__g = g

    @property
    def f(self): return self.__f

    @property
    def qc(self): return self.__qc

    @property
    def parent(self): return self.__parent
    
    def __gt__(self, other): return self.f >= other.f


class AEstrelaImp(AEstrela):
    def hasSolucao(self, qc):
        '''
        Verifica a existência de solução com base na verificação
        do número de inversões presentes no tabuleiro
        '''
        flat_board = [col for line in qc.getTab() for col in line]

        BOARD_LEN = len(flat_board)
        n_inversions = 0

        for i in range(BOARD_LEN):
            for j in range(i+1, BOARD_LEN):
                if flat_board[i] > flat_board[j] and flat_board[i] != -1 and flat_board[j] != -1:
                    n_inversions += 1

        # Caso o número de inversões seja par, há solução
        return not n_inversions % 2

    def getSolucao(self, qc):
        # Verifica se já está ordenado
        if qc.isOrdenado():
            return []

        if self.hasSolucao(qc):
            # Mesclamos o A* com o Algoritmo de Dijkstra
            visited = []
            steps = []

            # Cria a fila de prioridade
            queue = [(qc.getValor(), GameState(qc, None, 0))]
            p_queue.heapify(queue)
            
            while len(queue):
                w, curr = p_queue.heappop(queue)
                
                # Se não tiver sido visitado, visite
                if curr.qc.hashCode() in visited:
                    continue
                
                visited.append(curr.qc.hashCode())
                
                empty_coord = curr.qc.getPosVazio()
                moves = curr.qc.getMovePossiveis()
                
                for m in moves:
                    # Expande o próximo movimento
                    next_qc = deepcopy(curr.qc)
                    next_qc.move(empty_coord.getLinha(), empty_coord.getColuna(),
                                m.getLinha(), m.getColuna())
                    
                    # Verifica se o jogo ficou ordenado
                    if next_qc.isOrdenado():
                        # captura e exibe os passos
                        
                        steps.append(next_qc.getPosVazio())
                        while curr:
                            steps.append(curr.qc.getPosVazio())
                            curr = curr.parent
                        
                        return steps[::-1]
                    
                    # Senão adiciona o próximo elemento (com peso definido pelo F(x) = g(x) + 1 + h(x))
                    p_queue.heappush(queue,(curr.g + 1 + next_qc.getValor(), GameState(next_qc, curr, curr.g+1)))

        # Se não tiver solução retorna um movimento inválido
        return [Posicao(-1, -1)]
