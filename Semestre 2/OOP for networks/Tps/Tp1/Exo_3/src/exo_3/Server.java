package exo_3;

import java.io.*;

import java.net.*;



public class Server {

    public static void main(String[] args) {

        int port = 8080; 

        try (ServerSocket serverSocket = new ServerSocket(port)) {

            System.out.println("Serveur démarré sur le port " + port + "...");



            while (true) {

                Socket socket = serverSocket.accept(); 

                System.out.println("Client connecté : " + socket.getRemoteSocketAddress());



               

                BufferedReader input = new BufferedReader(new InputStreamReader(socket.getInputStream()));



              

                double num1 = Double.parseDouble(input.readLine());

                double num2 = Double.parseDouble(input.readLine());

                String operation = input.readLine();



              

                double result = 0;

                switch (operation) {

                    case "+":

                        result = num1 + num2;

                        break;

                    case "-":

                        result = num1 - num2;

                        break;

                    case "*":

                        result = num1 * num2;

                        break;

                    case "/":

                        if (num2 != 0) {

                            result = num1 / num2;

                        } else {

                            result = Double.NaN; 

                        }

                        break;

                    default:

                        System.out.println("Opération invalide !");

                }



              

                PrintWriter output = new PrintWriter(socket.getOutputStream(), true);

                output.println(result); 



                System.out.println("Calcul reçu : " + num1 + " " + operation + " " + num2 + " = " + result);



               

                socket.close();

            }

        } catch (IOException e) {

            e.printStackTrace();

        }

    }

}