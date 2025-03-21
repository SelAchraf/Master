package exo_3_tp2;

import java.rmi.Remote;
import java.rmi.RemoteException;

public interface RmiInterface extends Remote{
	public double getResult(double firstNumber, double secondNumber, String operation) throws RemoteException;
}