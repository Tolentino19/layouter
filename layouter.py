import os
from PIL import Image

# Criar a pasta 'layout' se não existir
output_folder = "layout"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Tamanho da folha A4 em polegadas (8.27 x 11.69 polegadas)
a4_width_inches = 8.27
a4_height_inches = 11.69

# Resolução desejada para a folha A4 em DPI
a4_dpi = 1200

# Converter as dimensões para pixels
a4_width = int(a4_width_inches * a4_dpi)
a4_height = int(a4_height_inches * a4_dpi)

# Tamanho de cada imagem em pixels (63.5mm x 88.9mm a 1200 DPI)
img_width = int(2.652 * a4_dpi)  # 63.5mm em polegadas
img_height = int(3.494 * a4_dpi)  # 88.9mm em polegadas

# Criar uma nova imagem branca (fundo da folha A4) com a resolução desejada
final_image = Image.new("RGB", (a4_width, a4_height), "white")

# Lista de caminhos para as suas 9 imagens
input_folder = "cartas"
image_paths = [os.path.join(input_folder, filename) for filename in os.listdir(input_folder) if filename.endswith(('.jpg', '.jpeg', '.png'))]

# Coordenadas iniciais para a primeira imagem
x, y = 10, 10

for img_path in image_paths:
    # Abrir a imagem
    img = Image.open(img_path)
    
    # Redimensionar a imagem para o tamanho desejado
    img = img.resize((img_width, img_height))
    
    # Colar a imagem na posição apropriada na folha A4
    final_image.paste(img, (x, y))
    
    # Atualizar as coordenadas para a próxima imagem (pode precisar ajustar isso com base no seu layout desejado)
    x += img_width + 10  # 10 é a margem entre as imagens

    # Se atingir a extremidade direita, mova para a próxima linha
    if x + img_width > a4_width:
        x = 10  # reiniciar a coordenada x
        y += img_height + 10  # 10 é a margem entre as imagens

# Caminho para o arquivo de saída
output_path = os.path.join(output_folder, "folha_a4.tiff")

# Salvar a imagem final como um arquivo TIFF com a resolução desejada
final_image.save(output_path, dpi=(a4_dpi, a4_dpi))

# Fechar a imagem final
final_image.close()

print(f"Layout final salvo em: {output_path}")
