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
            r1=float(r1)
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

        lista, numero, piuGrande = self._model.getArchiPesati()
        self._view.txt_result.controls.append(ft.Text("I 5 archi con peso maggiore", color="orange"))
        for u,v,peso in lista:
            self._view.txt_result.controls.append(ft.Text(f"{str(u)} -- {str(v)}     (peso={peso})"))
        self._view.txt_result.controls.append(ft.Text((f"Il grafo ha {numero} componenti connesse"), color="orange"))
        self._view.txt_result.controls.append(ft.Text(f"Nodi della componente connessa più grande ({len(piuGrande)} nodi)", color="orange"))
        for n in piuGrande:
            self._view.txt_result.controls.append(ft.Text(f"{str(n)}"))
        self._view.update_page()


    def handleCammino(self, e):
        bestPath = self._model.bestPath()
        if len(bestPath) == 0:
            self._view.txt_result.controls.append(ft.Text("Cammino non trovato", color="orange"))
            self._view.update_page()
            return
        self._view.txt_result.controls.append(ft.Text("Cammino semplie di lunghezza massima", color="pink"))
        self._view.txt_result.controls.append(ft.Text(f"Il cammino ha {len(bestPath)} nodi", color="pink"))
        for n in bestPath:
            self._view.txt_result.controls.append(ft.Text(f"{str(n)}"))
        self._view.update_page()