import pysmile

import pysmile_license
class Tutorial3:
    def __init__(self):
        print("Hello")
    def print_node_info(self, net, node_handle):
        # Print the node's id and name
        print(f"Node id/name: {net.get_node_id(node_handle)}/{net.get_node_name(node_handle)}")
        
        # Print all possible outcomes of the node
        print(f" Outcomes: {' '.join(net.get_outcome_ids(node_handle))}")
        
        # Print parents and children, if any
        parent_ids = net.get_parent_ids(node_handle)
        if parent_ids:
            print(f" Parents: {' '.join(parent_ids)}")
        
        child_ids = net.get_child_ids(node_handle)
        if child_ids:
            print(f" Children: {' '.join(child_ids)}")
        
        # Print the CPT (Conditional Probability Table)
        self.print_cpt_matrix(net, node_handle)

    def print_cpt_matrix(self, net, node_handle):
        # Get the CPT (Conditional Probability Table) of the node
        cpt = net.get_node_definition(node_handle)
        
        # Get the parents of the node
        parents = net.get_parents(node_handle)
        
        # Set up dimensions for the CPT matrix
        dim_count = 1 + len(parents)
        dim_sizes = [0] * dim_count
        for i in range(len(parents)):
            dim_sizes[i] = net.get_outcome_count(parents[i])
        dim_sizes[-1] = net.get_outcome_count(node_handle)
        
        # Coordinates for each probability entry in the CPT
        coords = [0] * dim_count
        for elem_idx in range(len(cpt)):
            self.index_to_coords(elem_idx, dim_sizes, coords)
            
            # Print the conditional probability for the outcome
            outcome = net.get_outcome_id(node_handle, coords[-1])
            print(f" P({outcome}", end="")
            
            if dim_count > 1:
                print(" | ", end="")
                
            for parent_idx in range(len(parents)):
                if parent_idx > 0:
                    print(", ", end="")
                parent_handle = parents[parent_idx]
                print(f"{net.get_node_id(parent_handle)}="
                      f"{net.get_outcome_id(parent_handle, coords[parent_idx])}", end="")
            
            prob = cpt[elem_idx]
            print(f") = {prob:.4f}")

    def index_to_coords(self, index, dim_sizes, coords):
        # Convert a linear index to multidimensional coordinates
        prod = 1
        for i in range(len(dim_sizes) - 1, -1, -1):
            coords[i] = (index // prod) % dim_sizes[i]
            prod *= dim_sizes[i]

# Run the example
tutorial = Tutorial3()

print("Starting Tutorial3...")
net = pysmile.Network()
        
        # Load the network file
net.read_file("Brain_Tumor.xdsl")
        
        
print("Tutorial3 complete.")
tutorial.print_cpt_matrix(net,"SH")
