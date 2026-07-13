import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDsRating(self):
        res = []
        for r in self._model.getRatings():
            res.append(ft.dropdown.Option(r))   # sarà poi da convertire quando lo passo alla funzione buildGraph()
        return res

    def handleCreaGrafo(self, e):
        r1= self._view._ddrating1.value
        r2= self._view._ddrating2.value
        if r1 is None or r2 is None:
            self._view.txt_result.controls.append(ft.Text("Selezionare un range", color="red"))
            self._view.update_page()
            return
        try:
            r1=float(r1)   # è un decimale!!!
            r2=float(r2)
        except ValueError:
            self._view.txt_result.controls.append(ft.Text("Numeri non validi", color="red"))
            self._view.update_page()
            return
        if r1 > r2:
            self._view.txt_result.controls.append(ft.Text("I numeri devono essere crescenti", color="red"))
            self._view.update_page()
            return
        self._model.buildGraph(r1, r2)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {self._model.getNumNodi()}", color="green"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {self._model.getNumArchi()}", color="green"))

        top5, numero, massima = self._model.archiPesati()
        self._view.txt_result.controls.append(ft.Text(f"I cinque archi con peso maggiore: ", color="pink"))
        for u,v,peso in top5:
            self._view.txt_result.controls.append(ft.Text(f"{u} - {v} --> peso= {peso}"))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {numero} componenti connesse", color="pink"))
        self._view.txt_result.controls.append(ft.Text(f"La componente connessa più grande ha {len(massima)} nodi", color="pink"))
        for n in massima:
            self._view.txt_result.controls.append(ft.Text(f"{n}"))
        self._view.update_page()


    def handleCammino(self, e):
        cammino = self._model.bestCammino()
        if len(cammino)==0:
            self._view.txt_result.controls.append(ft.Text(f"Cammino semplice di lunghezza massima non trovato", color="red"))
            self._view.update_page()
        self._view.txt_result.controls.append(
            ft.Text(f"Attori del cammino semplice di lunghezza massima", color="orange"))
        for n in cammino:
            self._view.txt_result.controls.append(ft.Text(f"{n}"))
        self._view.update_page()