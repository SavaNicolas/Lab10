import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._countries_all = DAO.getAllCountries()  # lista con tutte le nazioni, per avere l'id map
        # creo grafo
        self._grafo = nx.Graph()
        # mappa di oggetti
        self.idMapCountry = {}
        for f in self._countries_all:
            self.idMapCountry[f.CCode] = f

    def buildGraph(self,anno):
        self._countries = DAO.getAllCountries_anno(anno) #nazioni prese in base all'anno indicato
        # aggiungiamo i nodi(li ho nelle fermate)
        self._grafo.add_nodes_from(self._countries)
        # aggiungo archi
        self.addEdges(anno)

    def addEdges(self,anno):
        allEdges=DAO.getEdges(self.idMapCountry,anno) #lista di archi
        for edge in allEdges:
            self._grafo.add_edge(edge.country1, edge.country2)


    def getNumNodi(self):
        return len(self._grafo.nodes())

    def getNumArchi(self):
        return len(self._grafo.edges())

    @property
    def countries(self):
        return self._countries_all

    def getInfoConnessa(self,idInput):
        """
        restituisce i gradi di un nodo
        """
        source= self.idMapCountry[idInput] #se abbiamo solo id

        #prima di andare a calcolare i grafi vediamo prima se nel grafo c'è la source
        if self._grafo.has_node(source):
            gradi= self._grafo.degree(source)
            return gradi

    def getInfoConnessaGrafo(self):
        conn= nx.number_connected_components(self._grafo)
        return conn

    def hasNode(self,idInput):
        """
        per vedere se c'è il nodo scritto
        """
        return idInput in self._idMapCountry

    def getObjectFromId(self,id):
        return self.idMapCountry[id]

    def getDFSFromTree(self,nodo):
        stato= self.idMapCountry[nodo]
        tree=nx.dfs_tree(self._grafo,stato)
        nodi=list(tree.nodes())
        return nodi[1:]

    def nomeStato(self,id):
        return self.idMapCountry[id].StateNme



