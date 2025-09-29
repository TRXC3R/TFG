from PIL import Image, ImageTk
import os
import tkinter as tk
import requests
from avatar_generator import AvatarGenerator


def client(): #El cliente genera y envia imagenes al servidor
    generator = AvatarGenerator("./images")
    generator.generate_avatar() # Genera solamente un avatar
    img_path = './uploads/avatar.png'
    
    # Enviar al servidor
    with open(img_path, 'rb') as f:
        requests.post('http://localhost:5000/subir', files={'imagen': f})
    
    # Actualizar imagen en la interfaz
    img = Image.open(img_path)
    tk_img = ImageTk.PhotoImage(img)
    label.config(image=tk_img)
    label.image = tk_img  # Previene el garbage collector

root = tk.Tk()
if os.path.exists('./uploads/avatar.png'):
    img_inicial = Image.open('./uploads/avatar.png')  # Debe existir al comenzar
else:
    img_inicial = Image.new("RGBA", (24, 24), (255, 255, 255))  # Imagen en blanco si no existe

tk_img_inicial = ImageTk.PhotoImage(img_inicial)
label = tk.Label(root, image=tk_img_inicial)
label.pack()
boton = tk.Button(root, text='Generar y subir', command=client)
boton.pack()
root.mainloop() #La imagen se actualiza al pulsar el boton de generar y al subirla al servidor