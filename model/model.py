import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()



    def getRatings(self):
        return DAO.getRatings()



    def buildGraph(self,r1,r2):
        self._grafo.clear() # reset
        nodi = []
        for a in DAO.getNodes(r1,r2):
            nodi.append(a)
        self._grafo.add_nodes_from(nodi)
        self.addEdges(r1,r2)

    def addEdges(self,r1,r2):
        incassi = DAO.getIncassi(r1,r2)
        diz={}
        MovieIncasso= dict()
        # attoreID = [(movieID, incasso), (movieID, incasso)...]
        for attore, movie, incasso in incassi:
            if attore not in diz:
                diz[attore]=[]
            diz[attore].append(movie)
            MovieIncasso[movie] = incasso

        nodi = list(self._grafo.nodes)
        for i in range(len(nodi)):
            for j in range(i+1, len(nodi)):   # evito coppie di attori duplicati
                a1 = nodi[i].id
                a2 = nodi[j].id
                filmA1 = set()
                filmA2 = set()

                for a_id in diz:
                    if a_id == a1:
                        filmA1.update(diz[a_id])
                    if a_id == a2:
                        filmA2.update(diz[a_id])
                comuni = filmA1.intersection(filmA2)
                if len(comuni) >0:
                    peso = 0
                    for m in comuni:
                        if MovieIncasso[m] is not None:
                            try:
                                valore = MovieIncasso[m].replace("$", "").replace(",", "").strip()
                                peso += float(valore)
                            except (ValueError, AttributeError):
                                pass
                            self._grafo.add_edge(nodi[i], nodi[j], weight=peso)


    def getNumArchi(self):
        return len(self._grafo.edges)
    def getNumNodi(self):
        return len(self._grafo.nodes)


    def getPesi(self):
        res=[]
        for u, v, data in self._grafo.edges(data=True):
            res.append((u,v,data["weight"]))
        res.sort(key=lambda x: x[2], reverse=True)

        numCompConnesse = nx.number_connected_components(self._grafo)
        lista = []
        for c in nx.connected_components(self._grafo):
            lista.append((c, len(c)))
        lista.sort(key=lambda x: x[1], reverse=True)
        lista_nodi = []
        for n in lista[0][0]:
            lista_nodi.append(n)

        return res[:5], numCompConnesse, lista[0][1], lista_nodi

    #=================== RICORSIONE ===============================
    def _PercorsoPiuLungo(self):
        self._bestPath = []
        for n in self._grafo.nodes: # devo partire da ogni nodo del grafo
            # come nodo iniziale
            self._ricorsione1([n])
        return self._bestPath

    def _ricorsione1(self, parziale):
        if len(parziale) >len(self._bestPath):
            self._bestPath = list(parziale)

        ultimo= parziale[-1]
        for vicino in self._grafo.neighbors(ultimo):
            if vicino not in parziale:
                parziale.append(vicino)
                self._ricorsione1(parziale)
                parziale.pop()


    # ============CAMMINO DI LUNGHEZZA MAX , OGNI NODO CON ETA'STRETT. DECRESCENTE =====
    def percorsoLunghmax(self):
        self._bestPath = []
        for n in self._grafo.nodes: # devo partire da ogni nodo del grafo
            # come nodo iniziale
            self._ricorsione2([n])
        return self._bestPath

    def _ricorsione2(self, parziale):
        if len(parziale) >len(self._bestPath):
            self._bestPath = list(parziale)

        ultimo= parziale[-1]
        for vicino in self._grafo.neighbors(ultimo):
            if vicino not in parziale:
                if vicino.date_of_birth > ultimo.date_of_birth:
                    parziale.append(vicino)
                    self._ricorsione2(parziale)
                    parziale.pop()