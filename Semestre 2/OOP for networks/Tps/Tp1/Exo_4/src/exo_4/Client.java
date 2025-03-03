package exo_4;

import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.net.Socket;

public class Client {
    public static void main(String[] args) {
        String serverAddress = "127.0.0.1";
        int port = 8080;

       
        int[] tableau = {10, 15, 30, 4, 5};

        try (Socket socket = new Socket(serverAddress, port);
             ObjectOutputStream out = new ObjectOutputStream(socket.getOutputStream());
             ObjectInputStream in = new ObjectInputStream(socket.getInputStream())) {

            System.out.println("Connexion au serveur réussie !");

         
            out.writeObject(tableau);
            out.flush();
            System.out.println("Tableau envoyé au serveur.");

           
            int somme = (int) in.readObject();
            System.out.println("Somme reçue du serveur : " + somme);

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
