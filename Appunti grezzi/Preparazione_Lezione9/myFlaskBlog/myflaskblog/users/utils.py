import os
import secrets



def save_image_file(image_file_data):
    # Estrae l'estensione del file immagine
    _, file_ext = os.path.splitext(image_file_data.filename)

    # Crea un nuovo nome univoco per il file immagine
    new_name = secrets.token_hex(8)
    new_file_name = new_name + file_ext

    # Percorso del file immagine nel server
    file_path = os.path.join(os.getcwd(), "myflaskblog", "static", "images", new_file_name)

    # Salva il file immagine nel server
    image_file_data.save(file_path)

    # TODO: rimuovere il vecchio file immagine (os)
    # TODO: ridurre le dimensioni del file immagine caricato (pillow)

    # Ritorna il nuovo nome del file immagine
    return new_file_name
