package exo_3_tp2;

import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;

public class InterfaceImpl extends UnicastRemoteObject implements RmiInterface{

	protected InterfaceImpl() throws RemoteException {
		super();
	}

	private static final long serialVersionUID = 1L;

	@Override
	public double getResult(double firstNumber, double secondNumber, String operation) throws RemoteException {
		double result = 0;
		
		switch (operation) {
	        case "+":
	            result = firstNumber + secondNumber;
	            break;
	        case "-":
	            result = firstNumber - secondNumber;
	            break;
	        case "*":
	            result = firstNumber * secondNumber;
	            break;
	        case "/":
	            if (secondNumber != 0) {
	                result = firstNumber / secondNumber;
	            } else {
	                result = Double.NaN;
	            }
	            break;
	        default:
	            System.out.println("Opération invalide !");
		}
		
		return result;
	}

}