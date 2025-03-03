package exemple_socket_tcp;
import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;

public class TCPServer {
    public static void main(String[] args) {
        final int PORT = 8080;

        try {
            ServerSocket serverSocket = new ServerSocket(PORT);
            System.out.println("Server waiting for connection...");

            // Wait for a client to connect
            Socket clientSocket = serverSocket.accept();
            System.out.println("Client connecté depuis : " + clientSocket.getInetAddress());

            // Create input/output streams
            BufferedReader reader = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
            PrintWriter writer = new PrintWriter(clientSocket.getOutputStream(), true);

            // Read the client's message
            String clientMessage = reader.readLine();
            System.out.println("Message du client : " + clientMessage);

            // Send a response to the client
            writer.println("Message reçu, merci !");

            // Close resources
            reader.close();
            writer.close();
            clientSocket.close();
            serverSocket.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}