import pgmpy.readwrite
import matplotlib.pyplot as plt
import yodo

bn = pgmpy.readwrite.BIFReader("Brain_tumor_original.bif").get_model()
print('Number of nodes:', len(bn.nodes))
print('Number of arcs:', len(bn.edges))


analysis = yodo.yodo(bn, probability={'MC': 'True'})


for node in bn.nodes():
    print(f"Node: {bn.variable(node).name}")  # Correct method
    print(bn.cpt(node))  # Prints the full CPT for the node
    print("\n")
