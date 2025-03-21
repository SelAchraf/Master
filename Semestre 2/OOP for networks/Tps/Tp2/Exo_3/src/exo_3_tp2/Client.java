package exo_3_tp2;

import java.rmi.Naming;
import java.util.Scanner;

public class Client {

	public static void main(String[] args) {
		String object_location = "rmi//localhost:1099/Result";
		try (Scanner scanner = new Scanner(System.in)) {
			RmiInterface stub = (RmiInterface) Naming.lookup(object_location);
			
            System.out.print("Enter the first number: ");
            double firstNumber = scanner.nextDouble();
            
            System.out.print("Enter the second number: ");
            double secondNumber = scanner.nextDouble();
            
            System.out.print("Enter the operation (+, -, *, /): ");
            String operation = scanner.next();
			
            double result = stub.getResult(firstNumber, secondNumber, operation);
            System.out.println("The result of ( " + firstNumber + " " + operation + " " + secondNumber + " ) is: " + result);

		} 
        catch (Exception e) {
            System.err.println("Client exception: " + e.toString());
            e.printStackTrace();
		}
	}

}