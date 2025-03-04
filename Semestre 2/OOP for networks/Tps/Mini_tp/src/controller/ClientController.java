package controller;

import java.io.*;
import java.net.Socket;

public class ClientController {
    public String getGrade(String nom, String prenom, String module) {
        try (Socket socket = new Socket("localhost", 1234);
             PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
             BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()))) {
            
            String request = String.join(",", nom, prenom, module);
            out.println(request);
            return in.readLine();
        } catch (IOException e) {
            return "Erreur de connexion";
        }
    }
}