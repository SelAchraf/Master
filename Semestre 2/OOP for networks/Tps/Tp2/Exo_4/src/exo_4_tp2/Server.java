package exo_4_tp2;

import java.rmi.Naming;
import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;

public class Server {

	public static void main(String[] args) {
		String object_location = "rmi//localhost:1099/Sum";
		
		try {
			LocateRegistry.createRegistry(1099);
			
			InterfaceImpl object = new InterfaceImpl();
			
			Naming.rebind(object_location, object);
			
            System.out.println("Server is ready.");
			
		} 
        catch (RemoteException e) {
            System.err.println("RemoteException occurred: " + e.getMessage());
        } 
        catch (Exception e) {
            System.err.println("Exception occurred: " + e.getMessage());
        }
	}

}