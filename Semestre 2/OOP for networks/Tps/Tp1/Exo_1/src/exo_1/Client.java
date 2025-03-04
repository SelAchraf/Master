package exo_1;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.Socket;

public class Client {

    public static void main(String[] args) {

        String serverAddress = "127.0.0.1"; 
        int port = 1234; 

        try (Socket socket = new Socket(serverAddress, port);
             BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()))) {

            // Lecture de la réponse du serveur
            String response = in.readLine();
            System.out.println("Réponse du serveur : " + response);

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}