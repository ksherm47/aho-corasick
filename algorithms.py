from queue import SimpleQueue
from trie import Trie, StateNode


def match_trie(text: str, trie: Trie,
               failure_links: dict[StateNode, StateNode],
               output_links: dict[StateNode, StateNode],
               verbose=False):
    matches = []
    q = trie.get_initial_state()
    l = 0
    T = len(text)

    while l < T:
        if verbose and l % 1000 == 0:
            print(f'\rText matching progress: {l}/{T}', end='')

        while l < T and text[l] in trie.get_node_edges(q):
            q = trie.get_node(q, text[l])
            for pattern_id in q.accepting_for():
                pattern = trie.get_pattern(pattern_id)
                matches.append((l - len(pattern) + 1, pattern_id))
            if output_links[q]:
                for pattern_id in output_links[q].accepting_for():
                    pattern = trie.get_pattern(pattern_id)
                    matches.append((l - len(pattern) + 1, pattern_id))
            l += 1

        if q == trie.get_initial_state():
            l += 1

        q = failure_links[q]

    return matches


def get_failure_links(trie: Trie) -> dict[StateNode, StateNode]:
    f = {}
    visited_states = {}

    initial_state = trie.get_initial_state()
    f[initial_state] = initial_state
    state_queue = SimpleQueue()

    node_edges = trie.get_node_edges(initial_state)
    for edge in node_edges:
        child_node = trie.get_node(initial_state, edge)
        loop_info = (child_node, initial_state, edge)
        state_queue.put(loop_info)

    while not state_queue.empty():
        curr_state, parent, char = state_queue.get()
        visited_states[curr_state] = True

        r = f[parent]

        while r != initial_state and char not in trie.get_node_edges(r):
            r = f[r]

        r_edges = trie.get_node_edges(r)
        r_child = trie.get_node(r, char)

        if char in r_edges and r_child != curr_state:
            f[curr_state] = r_child
        else:
            f[curr_state] = initial_state

        node_edges = trie.get_node_edges(curr_state)
        for edge in node_edges:
            child_node = trie.get_node(curr_state, edge)
            if child_node not in visited_states:
                loop_info = (child_node, curr_state, edge)
                state_queue.put(loop_info)

    return f


def get_output_links(trie: Trie, failure_links: dict[StateNode, StateNode]) -> dict[StateNode, StateNode]:
    o = {node: None for node in trie.get_all_nodes()}
    visited_states = {}
    state_queue = SimpleQueue()

    initial_state = trie.get_initial_state()
    node_edges = trie.get_node_edges(initial_state)
    for edge in node_edges:
        state_queue.put(trie.get_node(initial_state, edge))

    while not state_queue.empty():
        node = state_queue.get()
        visited_states[node] = True

        f_node = failure_links[node]
        if len(f_node.accepting_for()) > 0:
            o[node] = f_node
        elif o[f_node]:
            o[node] = o[f_node]

        node_edges = trie.get_node_edges(node)
        for edge in node_edges:
            child_node = trie.get_node(node, edge)
            if child_node not in visited_states:
                state_queue.put(child_node)

    return o


def get_dna_reverse_complement(text) -> str:

    comp = {'a': 't', 't': 'a', 'c': 'g', 'g': 'c'}

    reverse_complement = ''.join([comp[char] for char in text])
    reverse_complement = reverse_complement[::-1]

    return reverse_complement
