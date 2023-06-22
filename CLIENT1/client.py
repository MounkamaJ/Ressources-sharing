import os
import tkinter as tk
from tkinter import Tk, messagebox, Canvas, Entry, Text, Button, PhotoImage,filedialog, simpledialog
from PIL import ImageTk, Image
import socket
import struct
import subprocess
import requetesClient

repertoire_courant = os.path.dirname(os.path.abspath(__file__))
def mode_serveur():
    chemin_relatif = os.path.join(repertoire_courant, "modeServeur.py")
    subprocess.Popen(["python3", chemin_relatif])


def send_request(choice):
    data = struct.pack('!i', choice)
    client_socket.sendall(data)


def share_file():
    initial_directory = "/home/jordy"
    selected_file = filedialog.askopenfilename(title = "Sélectionnez le fichier à partager", initialdir=initial_directory)
    if selected_file:
        filename = os.path.basename(selected_file)
        send_request(1)
        requetesClient.partage(client_socket, filename)
        messagebox.showinfo("Partager", "Le partage a été éffectué avec succès")

def search_file():
    keyword = simpledialog.askstring("Rechercher", "Entrez le mot-clé de recherche")
    if keyword:
        send_request(2)
        requetesClient.recherche(client_socket, keyword)
def quitter():
    client_socket.close()
    window.quit()


if __name__ == '__main__':
    mode_serveur()

    # Connexion au serveur distant
    server_host = '127.0.0.1'
    server_port = 8000

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))

    
    window = Tk()

    window.geometry("640x320")
    window.configure(bg = "#FFFFFF")
    image_path = "./fond.jpg"
    image = Image.open(image_path)
    background_image = ImageTk.PhotoImage(image)
    button_color = "black"
    button_text_color = "white"

    canvas = tk.Canvas(
        window,
        bg = "#FFFFFF",
        height = 320,
        width = 640,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )
    canvas.pack()
    
    canvas.create_image(
        0,
        0,
        image=background_image,
        anchor = tk.NW
    )
    
    canvas.create_text(
        260.0,
        50.0,
        anchor="nw",
        text="WELCOME",
        fill="#FFFFFF",
        font=("Inter ExtraBold", 24 * -1)
    )
    button1 = tk.Button(canvas, text="PARTAGER", width=10, height=2, command= share_file, bd=0, highlightthickness=0, bg=button_color, fg=button_text_color)
    button1_window = canvas.create_window(280, 100, anchor = tk.NW, window = button1)

    button2 = tk.Button(canvas, text="RECHERCHER", width=10, height=2,command= search_file,bd=0, highlightthickness=0, bg=button_color, fg=button_text_color)
    button2_window = canvas.create_window(280, 150, anchor = tk.NW, window = button2)

    button3 = tk.Button(canvas, text="QUITTER",width=10, height=2, command=quitter, bd=0, highlightthickness=0,bg=button_color, fg=button_text_color)
    button3_window = canvas.create_window(280, 200, anchor = tk.NW, window = button3)

    window.resizable(False, False)
    window.mainloop()


    client_socket.close()
