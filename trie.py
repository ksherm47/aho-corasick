

class StateNode:

    def __init__(self, accepting_for: int = None):
        self.__accepting = [] if accepting_for is None else [accepting_for]
        self.__children = []

    def accepting_for(self) -> list[int]:
        return self.__accepting

    def add_accepting_id(self, pattern_id: int):
        self.__accepting.append(pattern_id)

    def add_child_node(self, state_node):
        self.__children.append(state_node)

    def get_children_nodes(self):
        return self.__children


class Trie:

    def __init__(self, patterns: list[str]):

        self.__transition_function = {}
        self.__root = StateNode()
        self.__node_edges = {}  # For conducting searches (get all edges labels for a node)
        self.__all_nodes = [self.__root]
        self.__patterns = {}

        for pattern_id, pattern in enumerate(patterns):
            self.add_pattern(pattern, pattern_id + 1)

    def add_pattern(self, pattern: str, pattern_id: int):
        self.__patterns[pattern_id] = pattern
        self.__add_pattern(self.__root, pattern, pattern_id)

    def __add_pattern(self, node: StateNode, pattern: str, pattern_id: int):

        if len(pattern) == 1:

            char = pattern[0]
            if (node, char) not in self.__transition_function:
                child_node = StateNode(accepting_for=pattern_id)
                node.add_child_node(child_node)
                self.__transition_function[(node, char)] = child_node

                if node not in self.__node_edges:
                    self.__node_edges[node] = [char]
                else:
                    self.__node_edges[node].append(char)

                self.__all_nodes.append(child_node)

            else:

                child_node = self.__transition_function[(node, char)]
                child_node.add_accepting_id(pattern_id)

        else:

            char = pattern[0]
            rest_of_pattern = pattern[1:]

            if (node, char) not in self.__transition_function:
                child_node = StateNode()
                node.add_child_node(child_node)
                self.__transition_function[(node, char)] = child_node

                if node not in self.__node_edges:
                    self.__node_edges[node] = [char]
                else:
                    self.__node_edges[node].append(char)

                self.__all_nodes.append(child_node)
            else:
                child_node = self.__transition_function[(node, char)]

            self.__add_pattern(child_node, rest_of_pattern, pattern_id)

    def get_node(self, curr_node: StateNode, char: str):
        if (curr_node, char) in self.__transition_function:
            return self.__transition_function[(curr_node, char)]
        return None

    def get_node_edges(self, node) -> list[str]:
        if node in self.__node_edges:
            return self.__node_edges[node]
        return []

    def get_initial_state(self) -> StateNode:
        return self.__root

    def get_all_nodes(self) -> list[StateNode]:
        return self.__all_nodes

    def get_pattern(self, pattern_id) -> str:
        return self.__patterns[pattern_id]
