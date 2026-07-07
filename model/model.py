import copy
import networkx as nx
from database.DAO import DAO
class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self.mapId = {}


    def getRatings(self):
        return DAO.getRatings()


    def buildGraph(self,r1,r2):
        self._grafo.clear()
        nodi = []
        self.mapId = {}
        for a in DAO.getNodes(r1,r2):
            nodi.append(a)
        self._grafo.add_nodes_from(nodi)
        for a in nodi:
            if a.id not in self.mapId:
                self.mapId[a.id] = a

        self.addEdges(r1,r2)

    def addEdges(self,r1,r2):
        diz ={}
        coppie = DAO.getCoppie(r1,r2)
        for a1, a2, movie, peso in coppie:
            if a1 not in self.mapId or a2 not in self.mapId:
                # il ratings l'ho già controllato nella query (condizione sui nodi)
                continue
            attore1 = self.mapId[a1]
            attore2 = self.mapId[a2]

            # (a1,a2) = [(movie, incasso), (movie, incasso)....]
            if (attore1, attore2) not in diz:
                diz[(attore1, attore2)] = []
                pesoTot = 0
                if peso is not None:
                    peso = peso.replace("$", "")
                    pesoTot += int(peso.replace(" ", ""))
                diz[(attore1,attore2)].append((movie,pesoTot))
            else:
                pesoTot=0
                if peso is not None:
                    peso = peso.replace("$", "")
                    pesoTot += int(peso.replace(" ", ""))
                diz[(attore1,attore2)].append((movie,pesoTot))

        for attore1,attore2 in diz:
            incasso = 0
            for movie, peso in diz[(attore1,attore2)]:
                incasso += peso
            self._grafo.add_edge(attore1, attore2, weight=incasso)



    def getNumArchi(self):
        return len(self._grafo.edges)
    def getNumNodi(self):
        return len(self._grafo.nodes)

    def getArchiPesati(self):
        res = []
        for u,v,data in self._grafo.edges(data=True):
            res.append((u,v,data["weight"]))
        res.sort(key=lambda x: x[2], reverse=True)
        numero = nx.number_connected_components(self._grafo)
        componenti = list(nx.connected_components(self._grafo))
        piuGrande = max(componenti, key=len)
        return res[:5] , numero, piuGrande
    # ==============================================
    # RICORSIONE
    # ==============================================
    # cammino semplice di lunghezza massima
    # ogni nodo successivo ha un'età strett decrescente
    def bestPath(self):
        self._bestPath = []
        for nodo in self._grafo.nodes:  # siccome non ho un nodo di partenza
            # provo con tutti i nodi del grafo
            self._ricorsione(nodo, [nodo], nodo.date_of_birth)
        return self._bestPath

    def _ricorsione(self, nodoCorrente, parziale, etaUltimo):
        if len(parziale) > len(self._bestPath):
            self._bestPath= copy.deepcopy(parziale)


        for vicino in self._grafo.neighbors(nodoCorrente):
            if vicino not in parziale and vicino.date_of_birth > etaUltimo:
                parziale.append(vicino)
                self._ricorsione(vicino, parziale, vicino.date_of_birth)
                parziale.pop()

