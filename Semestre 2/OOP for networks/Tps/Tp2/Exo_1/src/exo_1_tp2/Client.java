package exo_1_tp2;

import java.rmi.Naming;

public class Client {

	public static void main(String[] args) {
        String object_location = "rmi://localhost:1099/Date";
        try {
    		RmiInterface stub;
    		
        	stub = (RmiInterface) Naming.lookup(object_location);
        	
            String currentDate = stub.getDate();
            
            System.out.println("Current Date and Time from Server: " + currentDate);
		} 
        catch (Exception e) {
            System.err.println("Client exception: " + e.toString());
            e.printStackTrace();
		}
	}

}