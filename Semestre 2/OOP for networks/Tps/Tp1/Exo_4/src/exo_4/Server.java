package exo_4;

import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.net.ServerSocket;
import java.net.Socket;

public class Server {
    public static void main(String[] args) {
        int port = 8080;

        try (ServerSocket serverSocket = new ServerSocket(port)) {
            System.out.println("Serveur en attente de connexions sur le port " + port + "...");

            while (true) {
             
                Socket clientSocket = serverSocket.accept();
                System.out.println("Client connecté : " + clientSocket.getInetAddress());

           
                ObjectInputStream in = new ObjectInputStream(clientSocket.getInputStream());
                ObjectOutputStream out = new ObjectOutputStream(clientSocket.getOutputStream());

             
                int[] tableau = (int[]) in.readObject();
                System.out.println("Tableau reçu : " + arrayToString(tableau));

           
                int somme = calculerSomme(tableau);

             
                out.writeObject(somme);
                out.flush();
                System.out.println("Somme envoyée : " + somme);

               
                clientSocket.close();
                System.out.println("Connexion fermée.");
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

 
    private static int calculerSomme(int[] tableau) {
        int somme = 0;
        for (int num : tableau) {
            somme += num;
        }
        return somme;
    }

 
    private static String arrayToString(int[] array) {
        StringBuilder sb = new StringBuilder("[ ");
        for (int num : array) {
            sb.append(num).append(" ");
        }
        sb.append("]");
        return sb.toString();
    }
}