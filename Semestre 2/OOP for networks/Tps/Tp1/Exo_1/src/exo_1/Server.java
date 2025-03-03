package exo_1;

import java.io.PrintWriter;

import java.net.ServerSocket;

import java.net.Socket;

import java.text.SimpleDateFormat;

import java.util.Date;



public class Server {

    public static void main(String[] args) {

        int port = 1234; // Port d'écoute du serveur



        try (ServerSocket serverSocket = new ServerSocket(port)) {

            System.out.println("Serveur en attente de connexion sur le port " + port + "...");



            while (true) {

                // Attente d'une connexion client

                Socket clientSocket = serverSocket.accept();

                System.out.println("Client connecté : " + clientSocket.getInetAddress());



                // Obtention de la date actuelle

                String dateActuelle = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(new Date());



                // Envoi de la date au client

                PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true);

                out.println("Date et heure actuelles : " + dateActuelle);



                // Fermeture de la connexion avec le client

                clientSocket.close();

                System.out.println("Date envoyée, connexion fermée.");

            }



        } catch (Exception e) {

            e.printStackTrace();

        }

    }

}

