from PIL import Image
import os


def combine_images(order):
    """
    Kombiniert 9 Bilder (clock_1.png bis clock_9.png) zu einem 3x3 Grid.
    Jedes Bild ist 885x885 Pixel gross.

    Args:
        order: Liste mit 9 Zahlen (0-8), die die Reihenfolge der Bilder bestimmt.
               0 entspricht clock_1.png, 1 entspricht clock_2.png, etc.
               Beispiel: [6, 7, 1, 4, 3, 5, 2, 8, 0]
    """
    # Bildgrösse
    img_width = 885
    img_height = 885

    # Grid-Dimensionen
    grid_cols = 3
    grid_rows = 3

    # Validierung
    if len(order) != 9:
        raise ValueError("Die order-Liste muss genau 9 Elemente enthalten!")

    # Grösse des kombinierten Bildes
    total_width = img_width * grid_cols
    total_height = img_height * grid_rows

    # Neues leeres Bild erstellen
    combined_image = Image.new('RGB', (total_width, total_height))

    # Bilder einfügen gemäss der order-Liste
    for position, image_index in enumerate(order):
        # Bildnummer berechnen (0-8 -> 1-9)
        image_number = image_index + 1

        # Bildpfad
        img_path = f'images/clock_{image_number}.png'

        # Überprüfen ob Datei existiert
        if not os.path.exists(img_path):
            print(f"Warnung: {img_path} nicht gefunden!")
            continue

        # Bild laden
        img = Image.open(img_path)

        # Position im Grid berechnen
        row = position // grid_cols
        col = position % grid_cols

        x = col * img_width
        y = row * img_height

        # Bild einfügen
        combined_image.paste(img, (x, y))


    # Kombiniertes Bild speichern
    output_path = 'images/combined_clocks.png'
    combined_image.save(output_path)
    print(f"\nFertig! Kombiniertes Bild gespeichert als: {output_path}")



