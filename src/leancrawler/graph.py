import networkx as nx

from leancrawler import LeanItemModel, DependanceModel

COLORS = {'theorem':   {'a': 1, 'r': 239, 'b': 66, 'g': 173},
          'lemma':   {'a': 1, 'r': 239, 'b': 66, 'g': 173},
          'definition': {'a': 1, 'r': 9, 'b': 236, 'g': 173},
          'structure': {'a': 1, 'r': 9, 'b': 236, 'g': 173},
          'constant': {'a': 1, 'r': 9, 'b': 236, 'g': 173},
          'axiom': {'a': 1, 'r': 9, 'b': 236, 'g': 173},
          'class': {'a': 1, 'r': 9, 'b': 236, 'g': 173},
          'inductive': {'a': 1, 'r': 9, 'b': 236, 'g': 173},
          'instance': {'a': 1, 'r': 9, 'b': 136, 'g': 253},
          'unknown': {'a': 1,  'r': 10, 'b': 10, 'g': 10}}


class ItemGraph(nx.DiGraph):
    @classmethod
    def from_db(cls, db, known_kind_only=True, **kwargs):
        graph = cls(**kwargs)
        for item in LeanItemModel.select():
            if known_kind_only and item.kind == 'unknown':
                continue
            graph.add_node(item)
            graph.nodes[item]['id'] = item.name
            graph.nodes[item]['label'] = item.name
            graph.nodes[item]['kind'] = item.kind
            graph.nodes[item]['viz'] = {'color': COLORS[item.kind]}

        for dep in DependanceModel.select():
            if known_kind_only and dep.used.kind == 'unknown':
                continue

            graph.add_edge(dep.used, dep.user)
        return graph
