import os
import socket
import time
import threading

def gestion_client(client_socket, client_address):
    print(f"Connexion établie avec {client_address}")

    # Recevoir le nom de fichier du client
    filename = client_socket.recv(1024).decode("utf-8")
    print("Recherche du fichier:", filename)
 
    # Vérifier si le fichier existe
    directory = "FICHIERS PARTAGES/"
    chemin_fichier = os.path.join(repertoire_courant, filename)
    if os.path.isfile(chemin_fichier):
        client_socket.send("FOUND".encode("utf-8"))

        # Envoyer le fichier au client
        with open(chemin_fichier, 'rb') as file:

            #Récupérer la taille du fichier et l'envoyer au client
            filesize = os.path.getsize(chemin_fichier)
            client_socket.sendall(str(filesize).encode("utf-8")) 
        
            time.sleep(0.5) 

            while True:
                data = file.read(1024)
                if not data:
                    break
                client_socket.sendall(data)   

            client_socket.sendall(b"END") # Envoyer un message de fin encodé en octets au serveur
            client_socket.shutdown(socket.SHUT_WR)  #indique qu'on a fini d'envoyer les données
            print("Téléchargement terminé")
    else:
        # Envoyer un message "fichier introuvable"
        message = "fichier introuvable"
        client_socket.send(message.encode("utf-8"))
        print("Fichier introuvable")
    
    
        

def start_server():
    # Paramètres du serveur
    host = '127.0.0.1'
    port = 43000

    # Création du socket serveur
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Serveur en attente de connexions sur le port {port}")

    while True:
        client_socket, client_address = server_socket.accept()

        # Démarrer un thread pour gérer le client
        client_thread = threading.Thread(target=gestion_client, args=(client_socket, client_address))
        client_thread.start()

start_server()

