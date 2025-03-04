package exo_3;

import java.io.*;
import java.net.*;

public class Server {

    public static void main(String[] args) {

        int port = 8080; 

        try (ServerSocket serverSocket = new ServerSocket(port)) {

            System.out.println("Serveur démarré sur le port " + port + "...");

            while (true) {

                Socket socket = serverSocket.accept(); 
                System.out.println("Client connecté : " + socket.getRemoteSocketAddress());

                // Création du flux d'entrée pour lire les données du client
                BufferedReader input = new BufferedReader(new InputStreamReader(socket.getInputStream()));

                // Lecture des deux nombres et de l'opération
                double num1 = Double.parseDouble(input.readLine());
                double num2 = Double.parseDouble(input.readLine());
                String operation = input.readLine();

                // Calcul du résultat en fonction de l'opération
                double result = 0;
                switch (operation) {
                    case "+":
                        result = num1 + num2;
                        break;
                    case "-":
                        result = num1 - num2;
                        break;
                    case "*":
                        result = num1 * num2;
                        break;
                    case "/":
                        if (num2 != 0) {
                            result = num1 / num2;
                        } else {
                            result = Double.NaN; // Division par zéro
                        }
                        break;
                    default:
                        System.out.println("Opération invalide !");
                }

                // Envoi du résultat au client
                PrintWriter output = new PrintWriter(socket.getOutputStream(), true);
                output.println(result); 

                // Affichage du calcul effectué
                System.out.println("Calcul reçu : " + num1 + " " + operation + " " + num2 + " = " + result);

                // Fermeture de la connexion avec le client
                socket.close();
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}