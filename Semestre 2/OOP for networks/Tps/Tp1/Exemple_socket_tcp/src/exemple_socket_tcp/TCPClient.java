package exemple_socket_tcp;
import java.io.*;
import java.net.Socket;

public class TCPClient {
    public static void main(String[] args) {
        final String SERVER_IP = "127.0.0.1";
        final int SERVER_PORT = 8080;

        try {
            // Connect to the server
            Socket socket = new Socket(SERVER_IP, SERVER_PORT);
            System.out.println("Connecté au serveur.");

            // Create input/output streams
            BufferedReader reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            PrintWriter writer = new PrintWriter(socket.getOutputStream(), true);

            // Send a message to the server
            writer.println("Bonjour, serveur !");
            System.out.println("aaaaaaaaaaaaaaaaaaaa: ");

            // Read the server's response
            String serverResponse = reader.readLine();
            System.out.println("Réponse du serveur : " + serverResponse);

            // Close resources
            reader.close();
            writer.close();
            socket.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}