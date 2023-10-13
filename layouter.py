import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image
from PyPDF2 import PdfMerger

# Programa simples com interface gráfica básica para gerar layouts para impressão em alta qualidade
# Backend para processar as imagens e gerar os layouts
def create_layout(image_paths, output_folder, selected_dpi, selected_format, merge_pdf):
    # Tamanho da folha A4 em polegadas (8.27 x 11.69 polegadas)
    a4_width_inches = 8.27
    a4_height_inches = 11.69

    # Resolução desejada para a folha A4 em DPI
    a4_dpi = selected_dpi

    # Converter as dimensões para pixels
    a4_width = int(a4_width_inches * a4_dpi)
    a4_height = int(a4_height_inches * a4_dpi)

    # Tamanho de cada imagem em pixels (63.5mm x 88.9mm a 1200 DPI)
    img_width = int(2.652 * a4_dpi)  # 63.5mm em polegadas
    img_height = int(3.494 * a4_dpi)  # 88.9mm em polegadas

    # Número total de imagens
    total_images = len(image_paths)

    # Número total de layouts desejados
    total_layouts = (total_images + 9 - 1) // 9

    # Loop para criar layouts
    for layout_num in range(total_layouts):
        # Criar uma nova imagem branca (fundo da folha A4) com a resolução desejada
        final_image = Image.new("RGB", (a4_width, a4_height), "white")

        # Coordenadas iniciais para a imagem
        x, y = 10, 10

        # Loop para adicionar imagens ao layout
        for idx in range(9):
            image_index = layout_num * 9 + idx

            # Verificar se ainda há imagens para adicionar
            if image_index < total_images:
                # Abrir a imagem
                img = Image.open(image_paths[image_index])

                # Redimensionar a imagem para o tamanho desejado
                img = img.resize((img_width, img_height))

                # Colar a imagem na posição apropriada na folha A4
                final_image.paste(img, (x, y))

                # Atualizar as coordenadas para a próxima imagem
                x += img_width + 1  # 10 é a margem entre as imagens

                # Se atingir a extremidade direita, mova para a próxima linha
                if x + img_width > a4_width:
                    x = 10  # reiniciar a coordenada x
                    y += img_height + 1  # 10 é a margem entre as imagens

        if selected_format == "PDF":
            # Caminho para o arquivo de saída
            output_path_pdf = os.path.join(output_folder, f"layout_{layout_num + 1}.pdf")

            # Salvar a imagem final como um arquivo PDF
            final_image.save(output_path_pdf, "PDF", dpi=(a4_dpi, a4_dpi))

            # Fechar a imagem final
            final_image.close()

            # Se o usuário escolheu mesclar os PDFs em um único arquivo
            if merge_pdf == "Sim":
                merger = PdfMerger()

                pdf_files = [f for f in os.listdir(output_folder) if f.endswith(".pdf")]

                for pdf_file in pdf_files:
                    pdf_path = os.path.join(output_folder, pdf_file)
                    merger.append(pdf_path)

                merger.write(os.path.join(output_folder, f"merged.pdf"))
                merger.close()

            print(f"Layout {layout_num + 1} salvo em: {output_path_pdf}")
        
        elif selected_format == "TIFF":
            # Caminho para o arquivo de saída
            output_path_tiff = os.path.join(output_folder, f"layout_{layout_num + 1}.tiff")

            # Salvar a imagem final como um arquivo TIFF com a resolução desejada
            final_image.save(output_path_tiff, dpi=(a4_dpi, a4_dpi))
            
            # Fechar a imagem final
            final_image.close()

            print(f"Layout {layout_num + 1} salvo em: {output_path_tiff}")

# Interface Gráfica:
def browse_folder(entry):
    folder_selected = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, folder_selected)

def show_completion_message(message):
    completion_label = tk.Label(root, text=message, font=("Helvetica", 16), fg="green")
    completion_label.grid(row=7, column=0, columnspan=3, pady=10)
    exit_button = tk.Button(root, text="Sair", command=root.destroy, font=("Helvetica", 12))
    exit_button.grid(row=8, column=0, columnspan=3, pady=10)

def run_layout_generator():
    input_folder = input_entry.get()
    output_folder = output_entry.get()
    selected_dpi = int(dpi_var.get())
    selected_format = format_var.get()
    merge_pdf = merge_var.get()

    if not os.path.exists(input_var.get()) or not os.listdir(input_var.get()):
        show_completion_message("Não há cartas para gerar o layout!")

    # Checar se existe a pasta destino, caso não, criá-la
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Lista de caminhos para as imagens na pasta 'cartas'
    image_paths = [os.path.join(input_folder, filename) for filename in os.listdir(input_folder) if filename.endswith(('.jpg', '.jpeg', '.png'))]

    create_layout(image_paths, output_folder, selected_dpi, selected_format, merge_pdf)

    show_completion_message("Concluído")

# Montar a interface gráfica
root = tk.Tk()
root.title("Gerador de layout")

# Seletor de DPI
dpi_label = tk.Label(root, text="DPI:")
dpi_label.grid(row=0, column=0, padx=10, pady=5)
dpi_var = tk.StringVar(value="600")
dpi_entry = tk.Entry(root, textvariable=dpi_var)
dpi_entry.grid(row=0, column=1, padx=10, pady=5)

# Seletor de pasta das imagens das cartas
input_label = tk.Label(root, text="Selecine a pasta das imagens:")
input_label.grid(row=2, column=0, padx=10, pady=5)
input_var = tk.StringVar(value=os.path.join(os.path.dirname(__file__), "cartas"))
input_entry = tk.Entry(root, textvariable=input_var)
input_entry.grid(row=2, column=1, padx=10, pady=5)
input_button = tk.Button(root, text="Navegar", command=lambda: browse_folder(input_entry))
input_button.grid(row=2, column=2, padx=10, pady=5)

# Seletor de pasta destino para os layouts
output_label = tk.Label(root, text="Selecione a pasta para salvar os layouts:")
output_label.grid(row=3, column=0, padx=10, pady=5)
output_var = tk.StringVar(value=os.path.join(os.path.dirname(__file__), "layouts"))
output_entry = tk.Entry(root, textvariable=output_var)
output_entry.grid(row=3, column=1, padx=10, pady=5)
output_button = tk.Button(root, text="Navegar", command=lambda: browse_folder(output_entry))
output_button.grid(row=3, column=2, padx=10, pady=5)

# Seletor de formato de arquivo
format_label = tk.Label(root, text="Selecione o formato de arquivo desejado:")
format_label.grid(row=4, column=0, padx=10, pady=5)
format_var = tk.StringVar(value="PDF")
format_dropdown = tk.OptionMenu(root, format_var, "PDF", "TIFF")
format_dropdown.grid(row=4, column=1, padx=10, pady=5)

# Opção para mesclar em um único PDF ou manter PDFs separados
merge_label = tk.Label(root, text="Mesclar em um único PDF:")
merge_label.grid(row=5, column=0, padx=10, pady=5)
merge_var = tk.StringVar(value="Não")
merge_dropdown = tk.OptionMenu(root, merge_var, "Sim", "Não")
merge_dropdown.grid(row=5, column=1, padx=10, pady=5)

# Botão executar
run_button = tk.Button(root, text="Executar", command=run_layout_generator)
run_button.grid(row=6, column=0, columnspan=2, pady=10)

# Etiqueta de status
status_var = tk.StringVar(value="")
status_label = tk.Label(root, textvariable=status_var, wraplength=400, justify="left")
status_label.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()
