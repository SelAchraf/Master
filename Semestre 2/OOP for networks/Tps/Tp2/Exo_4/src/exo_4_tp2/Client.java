package exo_4_tp2;

import java.rmi.Naming;
import java.util.Scanner;

public class Client {

	public static void main(String[] args) {
		String object_location = "rmi//localhost:1099/Sum";

		try (Scanner scanner = new Scanner(System.in)){
			RmiInterface stub = (RmiInterface) Naming.lookup(object_location);

	        System.out.print("Entrez la taille du tableau: ");
	        int size = scanner.nextInt();
	        
	        int[] tableau = new int[size];

	        System.out.println("Entrez les éléments du tableau:");
	        for (int i = 0; i < size; i++) {
	            System.out.print("Élément " + (i + 1) + ": ");
	            tableau[i] = scanner.nextInt();
	        }
	        
            int sum = stub.getSum(tableau);
            System.out.println("The sum of table elements is: " + sum);
	        
		} 
        catch (Exception e) {
            System.err.println("Client exception: " + e.toString());
            e.printStackTrace();
		}
	}

}