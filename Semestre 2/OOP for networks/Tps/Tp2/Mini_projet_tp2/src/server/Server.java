package server;

import java.rmi.Naming;
import java.rmi.registry.LocateRegistry;

import controller.GradeServiceImpl;

public class Server {
    public static void main(String[] args) {
        try {
            // Create the remote object
            GradeServiceImpl gradeService = new GradeServiceImpl();
            
            LocateRegistry.createRegistry(1099);

            // Bind the remote object to the RMI registry using Naming.rebind
            Naming.rebind("rmi://localhost:1099/GradeService", gradeService);

            System.out.println("Server is running and GradeService is bound in the registry...");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}