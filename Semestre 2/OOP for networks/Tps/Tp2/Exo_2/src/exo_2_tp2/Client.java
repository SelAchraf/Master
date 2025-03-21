package exo_2_tp2;

import java.rmi.Naming;
import java.util.Scanner;

public class Client {

	public static void main(String[] args) {
		String object_location = "rmi://localhost:1099/Square";
		
		try (Scanner scanner = new Scanner(System.in)) {
			
			RmiInterface stub = (RmiInterface) Naming.lookup(object_location);
			
            System.out.print("Enter a number to find its square: ");

			int number = scanner.nextInt();
			
			int square = stub.getSquare(number);
			
			System.out.println("The square of " + number + " is: " + square);
			
		}
        catch (Exception e) {
            System.err.println("Client exception: " + e.toString());
            e.printStackTrace();
		}
	}

}