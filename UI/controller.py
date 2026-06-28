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
            res.append(ft.dropdown.Option(r))
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
        self._view.txt_result.clean()
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {self._model.getNumNodi()}", color="green"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {self._model.getNumArchi()}", color="green"))

        archiPesati, numComp, lenPiuLunga, listaNodi = self._model.getPesi()
        self._view.txt_result.controls.append(ft.Text(f"top 5 archi", color="pink"))
        for u,v,peso in archiPesati:
            self._view.txt_result.controls.append(ft.Text(f"{u} --> {v}   peso: {peso}"))

        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha  {numComp} componenti connesse", color="pink"))
        self._view.txt_result.controls.append(ft.Text(f"La più grande componente connessa è lunga {lenPiuLunga}", color="pink"))
        for n in listaNodi:
            self._view.txt_result.controls.append(ft.Text(f"{n}"))
        self._view.update_page()


    def handleCammino(self, e):
        pass