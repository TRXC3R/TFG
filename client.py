from PIL import Image, ImageTk
import os
import tkinter as tk
import requests
from avatar_generator import AvatarGenerator
    
# Configuración inicial, variables globales
img_path = './uploads/avatar.png'
photo_image = None


# Función para generar imagen y enviarla al servidor, llama a la clase AvatarGenerator, crea la imagen y la guarda en img_path
def generar_imagen(): #El cliente genera y envia imagenes al servidor
    generator = AvatarGenerator("./images")
    generator.generate_avatar() # Genera solamente un avatar

#Envia la imagen generada al servidor junto con el nombre y la rareza de la imagen
def enviar_datos_al_servidor(name, rarity):
    with open(img_path, 'rb') as f:
        #Se podrían pasar los datos como json pero es más sencillo así, igual para más datos se usaría json
        response = requests.post('http://localhost:5000/subir',files={'imagen': f}, data={'nombre': name, 'rareza': rarity}) 
        #response = requests.post('http://localhost:5000/subir',files={'imagen': f}) 
    if response.status_code == 200:
        print("Datos enviados correctamente al servidor.")
    else:
        print("Error al enviar datos al servidor.")


# Interfaz gráfica con Tkinter, ventana para ingresar nombre y rareza, y mostrar la imagen generada, estos datos se deben enviar al servidor y guardar en una base de datos junto con la imagen
def ventana_datos():
    frame = tk.Tk()
    frame.title("Ventana de Datos")

    frame1 = tk.Frame(frame, width=400, height=400)
    frame1.pack()

    frame2 = tk.Frame(frame, width=400, height=400) 
    frame2.pack()

    #Variables
    hairProbVal = tk.StringVar()
    accProbVal = tk.IntVar()

    if not os.path.exists('./uploads/avatar.png'):
        img_inicial = Image.new("RGBA", (24, 24), (255, 255, 255))  # Imagen en blanco si no existe
    else:
        img_inicial = Image.open('./uploads/avatar.png')

    resized_photo = img_inicial.resize((120, 120))
    photo_image = ImageTk.PhotoImage(resized_photo)
    photo_label = tk.Label(frame, image=photo_image, width=200, height=200)
    photo_label.pack()

    WhatsUrNamelabel = tk.Label(frame1, text="Escribe tu nombre:")
    WhatsUrNamelabel.pack()

    nameEntry = tk.Entry(frame1, textvariable=hairProbVal)
    nameEntry.pack()

    WhatsUrProbability = tk.Label(frame1, text="Selecciona la Rareza (0.01(Muy Raro) - 1(Común)):")
    WhatsUrProbability.pack()
    accProbEntry= tk.Entry(frame2, textvariable=accProbVal)
    accProbEntry.pack()

    def recoger_valores():
        name_value = nameEntry.get()
        acc_value = accProbEntry.get()
        return name_value, acc_value

    btnEnter = tk.Button(frame, text="Enter", command=lambda: btnEnter())
    btnEnter.pack()

    def btnEnter():
        generar_imagen()
        name, rarity = recoger_valores()
        enviar_datos_al_servidor(name, rarity)
        actualizar_imagen()

    # Función para actualizar la imagen en la interfaz gráfica cuando se haya generado
    def actualizar_imagen():
        global photo_image
        if os.path.exists(img_path):
            nueva_img = Image.open(img_path)
            resized_photo = nueva_img.resize((120, 120))
            photo_image = ImageTk.PhotoImage(resized_photo)
            photo_label.configure(image=photo_image)
    
    frame.mainloop()

if __name__ == "__main__":
    ventana_datos()
