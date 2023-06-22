import socket
import threading
import datetime
import struct
import tkinter as tk
from tkinter import Tk, Button, messagebox


def gestion_client(client_socket, client_address):
    print(f"Connexion établie avec {client_address}")

    # Enregistrement de la connexion dans les logs
    with open('LOGS/log.txt', 'a') as logs_file:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logs_file.write(f"{current_time} - Nouvelle connexion établie avec {client_address[0]}:{client_address[1]}\n")

    try:
        while True:
            choice = int.from_bytes(client_socket.recv(4), byteorder='big')

            if choice == 1:  # PARTIE PARTAGE
                filename = client_socket.recv(1024).decode("utf-8", errors='replace')
                port = int.from_bytes(client_socket.recv(4), byteorder='big')
                # Enregistrer les données dans le répertoire centralisé
                with open('REP_CENTRALISE/files.txt', "a") as file:
                    file.write(f"{filename}, {client_address[0]}, {port}\n")

                print(f"Fichier {filename} reçu du client {client_address[0]}:{client_address[1]}\n")
            
                with open('LOGS/log.txt', 'a') as logs_file:
                    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    logs_file.write(f"{current_time} - Fichier {filename} reçu du client {client_address[0]}:{client_address[1]}\n")

            elif choice == 2:  # PARTIE RECHERCHE
                keyword = client_socket.recv(1024).decode('utf-8')
                
                with open('LOGS/log.txt', 'a') as logs_file:
                    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    logs_file.write(f"{current_time} - du mot clé: {keyword}\n")

                found = False
                with open('REP_CENTRALISE/files.txt', "r") as file:
                    for line in file:
                        if keyword.lower() in line.lower():    #compare en ignorant la casse
                            found = True
                            client_socket.send(line.encode("utf-8"))
                            print(f"{line}")

                            with open('LOGS/log.txt', 'a') as logs_file:
                                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                logs_file.write(f"{current_time} - Fichier trouvé pour le mot clé: {keyword}\n")
        
                    if not found:
                        msg = "NOT FOUND"
                        client_socket.sendall(msg.encode("utf-8"))
                        print("Fichier introuvable")
                        
                        with open('LOGS/log.txt', 'a') as logs_file:
                            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            logs_file.write(f"{current_time} - Fichier introuvable pour le mot clé: {keyword}\n") 

                    print("Recherche terminée\n")    
    except Exception as e:
        print(f"Erreur lors du traitement de la connexion du client {client_address[0]}: {str(e)}")
    except UnicodeDecodeError as e:
        print(f"Erreur de décodage des données du client {client_address[0]}: {str(e)}")
    
    client_socket.close()




def start_server():
    host = '127.0.0.1'
    port = 8000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Serveur en attente de connexions sur le port {port}")

    while True:
        client_socket, client_address = server_socket.accept()

        client_thread = threading.Thread(target=gestion_client, args=(client_socket, client_address))
        client_thread.start()


def afficher_rep():
    try:
        with open('REP_CENTRALISE/files.txt', 'r') as file:
            content = file.read()
            messagebox.showinfo("Contenu du répertoire centralisé", content)
    except FileNotFoundError:
        messagebox.showinfo("Erreur", "Le répertoire centralisé n'existe pas.")

def afficher_logs():
    try:
        with open('LOGS/log.txt', 'r') as file:
            content = file.read()
            messagebox.showinfo("Contenu des LOGS", content)
    except FileNotFoundError:
        messagebox.showinfo("Erreur", "Le fichier LOGS n'existe pas.")

def start_server_gui():
    window = tk.Tk()
    window.title("Application Serveur")
    window.geometry("300x200")
    window.configure(bg="#191970")
    button_color = "black"
    button_text_color = "white"

    # Création des boutons
    directory_button = tk.Button(window, text="Afficher contenu répertoire", command=afficher_rep, bg=button_color, fg=button_text_color)
    directory_button.pack()

    logs_button = tk.Button(window, text="Afficher contenu des LOGS", command=afficher_logs, bg=button_color, fg=button_text_color)
    logs_button.pack()

    # Lancement de la boucle principale
    window.mainloop()
start_server_thread = threading.Thread(target=start_server)
start_server_thread.start()

start_server_gui()
