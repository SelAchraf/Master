package server;

import java.io.*;
import java.net.Socket;
import model.CSVReader;

public class ServerHandler implements Runnable {
    private Socket socket;
    private CSVReader csvReader;

    public ServerHandler(Socket socket) {
        this.socket = socket;
        this.csvReader = new CSVReader("resources/students.csv");
    }

    @Override
    public void run() {
        try (BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
             PrintWriter out = new PrintWriter(socket.getOutputStream(), true)) {
            
            String request = in.readLine();
            String[] parts = request.split(",", 3);
            String response = csvReader.getGrade(parts[0], parts[1], parts[2]);
            out.println(response);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}