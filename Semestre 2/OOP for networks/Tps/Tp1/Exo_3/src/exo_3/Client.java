package exo_3;

import java.io.*;
import java.net.*;
import java.util.Scanner;

public class Client {

    public static void main(String[] args) {

        String serverAddress = "127.0.0.1"; 
        int port = 8080; 

        try (Socket socket = new Socket(serverAddress, port);
             PrintWriter output = new PrintWriter(socket.getOutputStream(), true);
             BufferedReader input = new BufferedReader(new InputStreamReader(socket.getInputStream()));
             Scanner scanner = new Scanner(System.in)) {

            // Saisie des nombres et de l'opération par l'utilisateur
            System.out.print("Entrez le premier nombre : ");
            double num1 = scanner.nextDouble();
            System.out.print("Entrez le deuxième nombre : ");
            double num2 = scanner.nextDouble();
            System.out.print("Entrez l'opération (+, -, *, /) : ");
            String operation = scanner.next();

            // Envoi des données au serveur
            output.println(num1);
            output.println(num2);
            output.println(operation);

            // Réception et affichage du résultat du serveur
            String result = input.readLine();
            System.out.println("Résultat reçu du serveur : " + result);

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}