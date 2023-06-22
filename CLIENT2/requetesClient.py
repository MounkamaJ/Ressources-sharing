import os
import socket
import struct
from tkinter import messagebox, filedialog, simpledialog


def partage(client_socket, filename):
    port = 43000
    data = struct.pack('!i', port)

    client_socket.sendall(filename.encode("utf-8"))
    client_socket.sendall(data)


def telechargement(address, num_port, filename):
     # Création d'une socket cliente
    sock_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Connexion au serveur
        sock_fd.connect((str(address), int(num_port)))
        print(f"Connecté au serveur {address}:{num_port}")

        # Envoi du nom de fichier au serveur
        sock_fd.sendall(filename.encode("utf-8"))

        # Réception des données du fichier
        response = sock_fd.recv(1024)
        if response.decode("utf-8") == "FOUND":
            save_directory = "DOWNLOADS/"
            if not os.path.exists(save_directory):
                os.makedirs(save_directory)
            save_path = os.path.join(save_directory, filename)
            
            filesize = int(sock_fd.recv(1024).decode("utf-8")) # Recevoir la taille du fichier à télécharger
            totalrecv = 0
            with open(save_path, 'wb') as file:
                while True:
                    data = sock_fd.recv(1024)
                    if data == b"END": # Vérifier si le message de fin est reçu
                        print("Message de fin")
                        break
                    else:
                        file.write(data) # Écrire les données dans le fichier
                        totalrecv += len(data)
                        print(f"Reçu {len(data)} octets   Total reçu: {totalrecv} / {filesize}")
                    if totalrecv >= filesize: # Vérifier si la taille du fichier est atteinte
                        print("Taille du fichier atteinte")
                        break
        
            messagebox.showinfo("Téléchargement", f"Le fichier {filename} a été téléchargé avec succès.")
        else:
            messagebox.showinfo("Téléchargement", f"Le fichier {filename} est introuvable.")

    except ConnectionRefusedError:
        print("La connexion au serveur a été refusée.")
    
    except Exception as e:
        print(f"Une erreur s'est produite lors du telechargement : {str(e)}")
    
    finally:
        # Fermeture de la connexion
        sock_fd.close()



def recherche(client_socket, keyword):
    client_socket.sendall(keyword.encode("utf-8"))

    response = client_socket.recv(1024).decode("utf-8")
    print(f"{response}")
    
    if response == "NOT FOUND":
        messagebox.showinfo("Résultat de la recherche", "Aucun fichier correspondant trouvé.")
        
    else:
        choice = messagebox.askquestion("Résultat de la recherche", "Fichier trouvé. Souhaitez-vous le télécharger ?")
        if choice == 'yes':
            
            filename, address, num_port = response.split(", ")                       
            print(f"Nom du fichier: {filename}\n")
            print(f"Adresse du client: {address}\n")
            print(f"Numero de port: {num_port}\n")
            
            telechargement(address, num_port, filename)
        




    
    
