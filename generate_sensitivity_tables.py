from derive_senstivity_function import get_all_functions
from load_params import load_params
from show_table import format_sensitivity_table_list, save_table_as_image
import os

def generate_sensitivity_tables(net_xdls):

    input_folder="split_outputs_high"
    csv_output_folder="high_sensitivity_csv"
    png_output_folder="high_sensitivity_png"
    os.makedirs(csv_output_folder, exist_ok=True)
    os.makedirs(png_output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            filepath = os.path.join(input_folder, filename)
            base_name = os.path.splitext(filename)[0]

            params = load_params(filepath)
            functions = [(par[2], get_all_functions(net_xdls, par, plots=False)) for par in params]
            df = format_sensitivity_table_list(functions)

            csv_path = os.path.join(csv_output_folder, f"{base_name}.csv")
            png_path = os.path.join(png_output_folder, f"{base_name}.png")

            df.to_csv(csv_path, index=False)
            save_table_as_image(df, png_path)
