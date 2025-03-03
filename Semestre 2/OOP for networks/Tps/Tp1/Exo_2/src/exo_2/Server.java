package exo_2;

import java.io.*;

import java.net.*;



public class Server {

    public static void main(String[] args) {

        int port = 5011; // Port d'écoute du serveur

        try (ServerSocket serverSocket = new ServerSocket(port)) {

            System.out.println("Serveur en attente de connexions sur le port " + port + "...");



            while (true) {

                Socket socket = serverSocket.accept();

                System.out.println("Client connecté : " + socket.getInetAddress());



                // Création des flux d'entrée et sortie

                BufferedReader input = new BufferedReader(new InputStreamReader(socket.getInputStream()));

                PrintWriter output = new PrintWriter(socket.getOutputStream(), true);



                // Lecture du nombre envoyé par le client

                String receivedNumber = input.readLine();

                int number = Integer.parseInt(receivedNumber);

                int squared = number * number;



                // Envoi du résultat au client

                output.println(squared);

                System.out.println("Reçu: " + number + ", Carré envoyé: " + squared);



                // Fermeture de la connexion

                socket.close();

            }

        } catch (IOException e) {

            e.printStackTrace();

        }

    }

}

