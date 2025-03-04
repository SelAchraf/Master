package exo_4;

import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.net.Socket;
import java.util.Scanner;

public class Client {
    public static void main(String[] args) {
        String serverAddress = "127.0.0.1";
        int port = 8082;

        // Create a Scanner object to read user input
        Scanner scanner = new Scanner(System.in);

        // Ask the user for the size of the array
        System.out.print("Entrez la taille du tableau : ");
        int size = scanner.nextInt();

        // Create an array of the specified size
        int[] tableau = new int[size];

        // Ask the user to enter the elements of the array
        System.out.println("Entrez les éléments du tableau :");
        for (int i = 0; i < size; i++) {
            System.out.print("Élément " + (i + 1) + " : ");
            tableau[i] = scanner.nextInt();
        }

        try (Socket socket = new Socket(serverAddress, port);
             ObjectOutputStream out = new ObjectOutputStream(socket.getOutputStream());
             ObjectInputStream in = new ObjectInputStream(socket.getInputStream())) {

            System.out.println("Connexion au serveur réussie !");

            // Envoi du tableau au serveur
            out.writeObject(tableau);
            out.flush();
            System.out.println("Tableau envoyé au serveur.");

            // Réception de la somme calculée par le serveur
            int somme = (int) in.readObject();
            System.out.println("Somme reçue du serveur : " + somme);

        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            // Close the scanner to avoid resource leaks
            scanner.close();
        }
    }
}