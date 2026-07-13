import copy
import networkx as nx
from database.DAO import DAO
class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self.mapAttori = {}



    def getRatings(self):
        return DAO.getRatings()

    def getNumNodi(self):
        return len(self._grafo.nodes)

    def getNumArchi(self):
        return len(self._grafo.edges)

    def buildGraph(self,r1,r2):
        self._grafo.clear()
        nodi = []
        for a in DAO.getNodes(r1,r2):
            nodi.append(a)
        self._grafo.add_nodes_from(nodi)
        for a in nodi:
            self.mapAttori[a.id] =a

        incassi = {}   # (attore1, attore2) = [(movie, incasso), ....]
        for a1, a2, movie, peso in DAO.getArchi(r1,r2):
            if a1 not in self.mapAttori or a2 not in self.mapAttori:
                continue
            attore1 = self.mapAttori[a1]
            attore2 = self.mapAttori[a2]
            if (attore1, attore2) not in incassi:
                incassi[(attore1, attore2)] = []
                pesoTot= 0
                peso = int(peso.replace(" ","").replace("$",""))
                pesoTot += peso
                incassi[(attore1, attore2)].append((movie, pesoTot))
            else:
                if peso is not None:
                    pesoTot = 0
                    peso = int(peso.replace(" ", "").replace("$", ""))
                    pesoTot += peso
                    incassi[(attore1, attore2)].append((movie, pesoTot))
            for (attore1, attore2) in incassi:
                incasso = 0
                for movie, peso in incassi[(attore1, attore2)]:
                    incasso+= peso
                self._grafo.add_edge(attore1, attore2, weight=incasso)


    def archiPesati(self):
        res = []
        for u,v,data in self._grafo.edges(data=True):
            res.append((u,v,data["weight"]))
        res.sort(key=lambda x: x[2], reverse=True)

        componenti = nx.number_connected_components(self._grafo)
        massima = max(list(nx.connected_components(self._grafo)), key=len)


        return res[:5], componenti, massima


    def bestCammino(self):
        self.bestPath = []
        for n in self._grafo.nodes:
            self.ricorsione(n, [n])
        return self.bestPath

    def ricorsione(self, n, parziale):
        if len(parziale)> len(self.bestPath):
            self.bestPath = copy.deepcopy(parziale)

        for vicino in self._grafo.neighbors(n):
            if vicino.date_of_birth < n.date_of_birth:
                if vicino not in parziale:
                    parziale.append(vicino)
                    self.ricorsione(vicino, parziale)
                    parziale.pop()
