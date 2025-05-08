import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCalcola(self, e):
        self._view._txt_result.controls.clear()
        #prendo anno dall'input
        anno= self._view._txtAnno.value
        #controlli
        if anno == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("inserisci un valore"))
            self._view.update_page()
            return

        #converto in intero
        try:
            anno= int(anno)
        except ValueError:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("inserisci un numero"))
            self._view.update_page()
            return

        #vedo se è nel range 1816-2016
        if anno <1816 or anno >2016:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("inserisci un valore compreso tra 1816 e 2016"))
            self._view.update_page()
            return

        #creo grafo
        self._model.buildGraph(anno)

        #posso abilitare bottoni
        self._view._raggiungibili.disabled=False
        self._view._trova.disabled = False


        #stampo txt result
        self._view._txt_result.controls.append(ft.Text("grafo correttamente creato"))
        self._view._txt_result.controls.append(ft.Text(f"il grafo ha {self._model.getInfoConnessaGrafo()} componenti connesse"))
        self._view.update_page()

        #stampo ogni nodo e il suo numero di stati confinanti
        stati= self._model.countries
        stati.sort(key=lambda x: x.StateNme)
        for country in stati:
            codice=country.CCode
            numero= self._model.getInfoConnessa(codice)
            if numero != None:
                self._view._txt_result.controls.append(ft.Text(f"{country} -- {numero} vicini"))
                self._view.update_page()
        #self._btnCalcola

    def fill_country(self):
        for country in self._model.countries:  # sto appendendo al dropdown l'oggetto reatiler
            self._view._raggiungibili.options.append(
                ft.dropdown.Option(key=country.CCode,  # 🔑 Chiave univoca dell'opzione
                                   text=country.StateNme,  # 🏷️ Testo visibile nel menu a tendina
                                   data=country,
                                   # 📦 Oggetto completo, utile per accedere a tutti gli attributi dopo la selezione
                                   on_click=self.read_country))  # salvati l'oggetto da qualche parte

    def read_country(self, e):
        self._raggiungibili = e.control.data  # l'abbiamo inizializzata a None
        # e.control.data è il risultato di onclick sopra

    def handleStatiRaggiungibili(self, e):
        self._view._txt_result.controls.clear()
        # prendo stato dall'input
        stato = self._view._raggiungibili.value #value restituisce sempre una stringa
        stato= int(stato) #id
        nomeStato= self._model.nomeStato(stato)
        #creo tree dall'input
        nodi = self._model.getDFSFromTree(stato) #qui abbiamo lista di nodi
        if nodi == []:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text(f"non posso raggiungere nessun nodo da {nomeStato} "))
            self._view.update_page()
        else:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text(f"stati raggiungibili da {nomeStato} : "))
            for i in nodi:
                self._view._txt_result.controls.append(ft.Text(f"{i}"))

            self._view.update_page()






