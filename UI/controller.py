import flet as ft
from UI.view import View
from model.model import Model
import networkx as nx # <-- AGGIUNGI QUESTA RIGA


# ... (il resto del codice del Controller)


class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_grafo(self, e):
        """Callback per il pulsante 'Crea Grafo'."""
        try:
            anno = int(self._view.txt_anno.value)
        except:
            self._view.show_alert("Inserisci un numero valido per l'anno.")
            return
        if anno < 1950 or anno > 2024:
            self._view.show_alert("Anno fuori intervallo (1950-2024).")
            return

        self._model.build_weighted_graph(anno)
        self._view.lista_visualizzazione_1.controls.clear()
        self._view.lista_visualizzazione_1.controls.append(
            ft.Text(f"Grafo calcolato: {self._model.G.number_of_nodes()} nodi, {self._model.G.number_of_edges()} archi")
        )
        min_p, max_p = self._model.get_edges_weight_min_max()
        self._view.lista_visualizzazione_1.controls.append(ft.Text(f"Peso min: {min_p:.2f}, Peso max: {max_p:.2f}"))
        self._view.page.update()

    def handle_conta_archi(self, e):
        """Callback per il pulsante 'Conta Archi'."""
        try:
            soglia = float(self._view.txt_soglia.value)
        except:
            self._view.show_alert("Inserisci un numero valido per la soglia.")
            return

        min_p, max_p = self._model.get_edges_weight_min_max()
        if soglia < min_p or soglia > max_p:
            self._view.show_alert(f"Soglia fuori range ({min_p:.2f}-{max_p:.2f})")
            return

        minori, maggiori = self._model.count_edges_by_threshold(soglia)
        self._view.lista_visualizzazione_2.controls.clear()
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f"Archi < {soglia}: {minori}, Archi > {soglia}: {maggiori}"))
        self._view.page.update()

    """Implementare la parte di ricerca del cammino minimo"""
    # TODO
    def handle_cammino_minimo(self, e):
        # 1. Validazione della soglia S (omessa per brevità)
        try:
            soglia = float(self._view.txt_soglia.value)
        except:
            self._view.show_alert("Inserisci un numero valido nel campo Soglia S.")
            return

        min_p, max_p = self._model.get_edges_weight_min_max()
        if soglia < min_p or soglia > max_p:
            self._view.show_alert(f"Soglia fuori range ({min_p:.2f}-{max_p:.2f})")
            return

        path_nodes = self._model.find_shortest_path(soglia)

        # Usa lista_visualizzazione_3
        self._view.lista_visualizzazione_3.controls.clear()

        if not path_nodes:
            self._view.lista_visualizzazione_3.controls.append(
                ft.Text("Nessun cammino minimo trovato che rispetti i vincoli (peso > S e >= 2 archi).")
            )
        else:

            path_weight = nx.path_weight(self._model.G, path_nodes, weight='weight')



            # Riga 1: Titolo
            self._view.lista_visualizzazione_3.controls.append(
                ft.Text("Cammino minimo:")
            )

            # Itera per stampare ogni segmento del percorso
            for i in range(len(path_nodes) - 1):
                u = path_nodes[i]
                v = path_nodes[i+1]

                # Recupera il peso dell'arco
                edge_data = self._model.G.get_edge_data(u, v)

                peso = edge_data['weight']

                # Formatta la riga esattamente come specificato
                output_line = (
                    f"[{u.id}] {u.nome} ({u.localita}) --> "
                    f"[{v.id}] {v.nome} ({v.localita}) [peso: {peso:.1f}]" # Assumo .1f o .2f a seconda di come è formattato l'esempio
                )

                self._view.lista_visualizzazione_3.controls.append(
                    ft.Text(output_line)
                )



        self._view.page.update()