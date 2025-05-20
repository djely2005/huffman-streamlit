import streamlit as st
import heapq
from graphviz import Digraph

class Node:
    def __init__(self, symbol, prob, left=None, right=None):
        self.symbol = symbol
        self.prob = prob
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.prob < other.prob

def build_huffman_tree(symbols_probs):
    heap = [Node(symbol, prob) for symbol, prob in symbols_probs]
    heapq.heapify(heap)

    while len(heap) > 1:
        n1 = heapq.heappop(heap)
        n2 = heapq.heappop(heap)
        merged = Node(None, n1.prob + n2.prob, n1, n2)
        heapq.heappush(heap, merged)

    return heap[0]

def generate_codes(node, prefix="", codebook={}):
    if node is not None:
        if node.symbol is not None:
            codebook[node.symbol] = prefix
        generate_codes(node.left, prefix + "0", codebook)
        generate_codes(node.right, prefix + "1", codebook)
    return codebook

def draw_tree(node, dot=None, node_id=0):
    if dot is None:
        dot = Digraph()
        dot.attr('node', shape='circle')

    current_id = str(node_id)
    label = f"{node.symbol}" if node.symbol else f"{node.prob:.2f}"
    dot.node(current_id, label, color="red" if node.symbol else "black", height="1", width="1")

    if node.left:
        left_id = str(node_id * 2 + 1)
        dot.edge(current_id, left_id, label="0")
        draw_tree(node.left, dot, node_id * 2 + 1)
    if node.right:
        right_id = str(node_id * 2 + 2)
        dot.edge(current_id, right_id, label="1")
        draw_tree(node.right, dot, node_id * 2 + 2)

    return dot
