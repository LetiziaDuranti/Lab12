import networkx as nx
from database.dao import DAO
from model.Rifugio import Rifugio
class Model:
    def __init__(self):
        """Definire le strutture dati utili"""
        # TODO
        self.G = nx.Graph()
        self._rifugi_map = {}
        self._min_weight = float('inf')
        self._max_weight = float('-inf')

    def _get_difficulty_factor(self, difficolta: str):
        """Restituisce il fattore di difficoltà in base al requisito."""
        if difficolta == 'facile':
            return 1.0
        elif difficolta == 'media':
            return 1.5
        elif difficolta == 'difficile':
            return 2.0
        return 1.0
    def build_weighted_graph(self, year: int):
        """
        Costruisce il grafo pesato dei rifugi considerando solo le connessioni con campo `anno` <= year passato
        come argomento.
        Il peso del grafo è dato dal prodotto "distanza * fattore_difficolta"
        """
        # TODO
        self.G.clear()
        self._rifugi_map.clear()
        self._min_weight = float('inf')
        self._max_weight = float('-inf')

        # 1. Carica i rifugi e crea la mappa ID -> DTO
        rifugi_data = DAO.readAllRifugi()
        for row in rifugi_data:
            rifugio_dto = Rifugio(row["id"], row["nome"], row["localita"], row["altitudine"], row["capienza"],
                                  row["aperto"])
            self._rifugi_map[row["id"]] = rifugio_dto

        # 2. Carica le connessioni filtrate per l'anno
        connessioni_data = DAO.readConnessioniByYear(year)

        nodi_coinvolti_id = set()
        for row in connessioni_data:
            # Calcolo del peso: peso = distanza x fattore_difficolta
            fattore = self._get_difficulty_factor(row['difficolta'])
            peso = float(row['distanza']) * fattore

            id1 = row['id_rifugio1']
            id2 = row['id_rifugio2']

            nodi_coinvolti_id.add(id1)
            nodi_coinvolti_id.add(id2)

            u = self._rifugi_map[id1]
            v = self._rifugi_map[id2]

            # Aggiunge l'arco con il peso (il grafo è non orientato)
            self.G.add_edge(u, v, weight=peso)

            # 3. Aggiorna min/max weight (usati per la validazione nel Controller)
            if peso < self._min_weight: self._min_weight = peso
            if peso > self._max_weight: self._max_weight = peso

        # Aggiunge i nodi coinvolti al grafo (NetworkX lo fa automaticamente, ma qui lo facciamo per i nodi non isolati)
        nodi_da_aggiungere = [self._rifugi_map[id] for id in nodi_coinvolti_id]
        self.G.add_nodes_from(nodi_da_aggiungere)

        if self.G.number_of_edges() == 0:
            self._min_weight = 0.0
            self._max_weight = 0.0


    def get_edges_weight_min_max(self):
        """
        Restituisce min e max peso degli archi nel grafo
        :return: il peso minimo degli archi nel grafo
        :return: il peso massimo degli archi nel grafo
        """
        # TODO
        return self._min_weight, self._max_weight
    def count_edges_by_threshold(self, soglia):
        """
        Conta il numero di archi con peso < soglia e > soglia
        :param soglia: soglia da considerare nel conteggio degli archi
        :return minori: archi con peso < soglia
        :return maggiori: archi con peso > soglia
        """
        # TODO
        minori = 0
        maggiori = 0

        # Iterazione sugli archi, accedendo ai dati (peso)
        for u, v, data in self.G.edges(data=True):
            peso = data.get('weight', 0)
            if peso < soglia:
                minori += 1
            elif peso > soglia:  # Non contiamo gli archi con peso == soglia
                maggiori += 1

        return minori, maggiori

    """Implementare la parte di ricerca del cammino minimo"""
    # TODO
    def find_shortest_path(self, soglia: float):
        """
        Ricerca il cammino più breve (Dijkstra) usando solo archi con peso > S.
        Il cammino deve avere >= 2 archi (3 nodi).
        """
        # 1. Crea un sottografo di lavoro con gli archi filtrati (peso > soglia)
        subgraph = nx.Graph()

        edges_to_keep = [
            (u, v, data['weight'])
            for u, v, data in self.G.edges(data=True)
            if data.get('weight', 0) > soglia
        ]

        if not edges_to_keep:
            return []

        # Aggiunge i nodi del grafo originale e gli archi filtrati
        subgraph.add_nodes_from(self.G.nodes)
        subgraph.add_weighted_edges_from(edges_to_keep)

        # 2. Ricerca del percorso più breve (Dijkstra) tra tutte le coppie
        shortest_path = []
        min_total_weight = float('inf')

        nodes = list(subgraph.nodes)

        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                start_node = nodes[i]
                end_node = nodes[j]

                try:

                    path = nx.shortest_path(subgraph, source=start_node, target=end_node, weight='weight')


                    if len(path) >= 3:
                        path_weight = nx.path_weight(subgraph, path, weight='weight')

                        if path_weight < min_total_weight:
                            min_total_weight = path_weight
                            shortest_path = path

                except nx.NetworkXNoPath:
                    continue


        return shortest_path