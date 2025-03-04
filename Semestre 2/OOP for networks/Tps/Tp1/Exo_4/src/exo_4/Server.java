package exo_4;

import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.net.ServerSocket;
import java.net.Socket;

public class Server {
    public static void main(String[] args) {
        int port = 8082;

        try (ServerSocket serverSocket = new ServerSocket(port)) {
            System.out.println("Serveur en attente de connexions sur le port " + port + "...");

            while (true) {
                // Attente d'une connexion client
                Socket clientSocket = serverSocket.accept();
                System.out.println("Client connecté : " + clientSocket.getInetAddress());

                // Création des flux d'entrée et de sortie pour les objets
                ObjectInputStream in = new ObjectInputStream(clientSocket.getInputStream());
                ObjectOutputStream out = new ObjectOutputStream(clientSocket.getOutputStream());

                // Lecture du tableau envoyé par le client
                int[] tableau = (int[]) in.readObject();
                System.out.println("Tableau reçu : " + arrayToString(tableau));

                // Calcul de la somme des éléments du tableau
                int somme = calculerSomme(tableau);

                // Envoi de la somme au client
                out.writeObject(somme);
                out.flush();
                System.out.println("Somme envoyée : " + somme);

                // Fermeture de la connexion avec le client
                clientSocket.close();
                System.out.println("Connexion fermée.");
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    // Méthode pour calculer la somme des éléments d'un tableau
    private static int calculerSomme(int[] tableau) {
        int somme = 0;
        for (int num : tableau) {
            somme += num;
        }
        return somme;
    }

    // Méthode pour convertir un tableau en chaîne de caractères
    private static String arrayToString(int[] array) {
        StringBuilder sb = new StringBuilder("[ ");
        for (int num : array) {
            sb.append(num).append(" ");
        }
        sb.append("]");
        return sb.toString();
    }
}