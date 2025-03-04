package exo_2;

import java.io.*;
import java.net.*;
import java.util.Scanner;

public class Client {

    public static void main(String[] args) {

        String serverAddress = "127.0.0.1"; 
        int port = 5011;

        try (Socket socket = new Socket(serverAddress, port);
             PrintWriter output = new PrintWriter(socket.getOutputStream(), true);
             BufferedReader input = new BufferedReader(new InputStreamReader(socket.getInputStream()));
             Scanner scanner = new Scanner(System.in)) {

            System.out.print("Entrez un nombre : ");
            int number = scanner.nextInt();

            // Envoi du nombre au serveur
            output.println(number);

            // Réception et affichage du carré du nombre
            String response = input.readLine();
            System.out.println("Le carré de " + number + " est : " + response);

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}