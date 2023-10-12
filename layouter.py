import os
from PIL import Image

def create_layout(image_paths, output_folder, layouts_per_page):
    # Tamanho da folha A4 em polegadas (8.27 x 11.69 polegadas)
    a4_width_inches = 8.27
    a4_height_inches = 11.69

    # Resolução desejada para a folha A4 em DPI
    a4_dpi = 600

    # Converter as dimensões para pixels
    a4_width = int(a4_width_inches * a4_dpi)
    a4_height = int(a4_height_inches * a4_dpi)

    # Tamanho de cada imagem em pixels (63.5mm x 88.9mm a 1200 DPI)
    img_width = int(2.652 * a4_dpi)  # 63.5mm em polegadas
    img_height = int(3.494 * a4_dpi)  # 88.9mm em polegadas

    # Número total de imagens
    total_images = len(image_paths)

    # Número total de layouts desejados
    total_layouts = (total_images + layouts_per_page - 1) // layouts_per_page

    # Loop para criar layouts
    for layout_num in range(total_layouts):
        # Criar uma nova imagem branca (fundo da folha A4) com a resolução desejada
        final_image = Image.new("RGB", (a4_width, a4_height), "white")

        # Coordenadas iniciais para a imagem
        x, y = 10, 10

        # Loop para adicionar imagens ao layout
        for idx in range(layouts_per_page):
            image_index = layout_num * layouts_per_page + idx

            # Verificar se ainda há imagens para adicionar
            if image_index < total_images:
                # Abrir a imagem
                img = Image.open(image_paths[image_index])

                # Redimensionar a imagem para o tamanho desejado
                img = img.resize((img_width, img_height))

                # Colar a imagem na posição apropriada na folha A4
                final_image.paste(img, (x, y))

                # Atualizar as coordenadas para a próxima imagem
                x += img_width + 10  # 10 é a margem entre as imagens

                # Se atingir a extremidade direita, mova para a próxima linha
                if x + img_width > a4_width:
                    x = 10  # reiniciar a coordenada x
                    y += img_height + 10  # 10 é a margem entre as imagens

        # Caminho para o arquivo de saída
        output_path_pdf = os.path.join(output_folder, f"layout_{layout_num + 1}.pdf")

        # Salvar a imagem final como um arquivo PDF
        final_image.save(output_path_pdf, "PDF", dpi=(a4_dpi, a4_dpi))

        # Fechar a imagem final
        final_image.close()

        print(f"Layout {layout_num + 1} salvo em: {output_path_pdf}")

# Pasta de entrada (imagens)
input_folder = "cartas"

# Pasta de saída (layouts numerados)
output_folder = "layout"

# Criar a pasta 'layout' se não existir
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Número de layouts desejados por página
layouts_per_page = 9  # Altere conforme necessário

# Lista de caminhos para as imagens na pasta 'cartas'
image_paths = [os.path.join(input_folder, filename) for filename in os.listdir(input_folder) if filename.endswith(('.jpg', '.jpeg', '.png'))]

# Criar layouts para as imagens
create_layout(image_paths, output_folder, layouts_per_page)
