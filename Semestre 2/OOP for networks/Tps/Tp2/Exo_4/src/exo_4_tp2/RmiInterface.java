package exo_4_tp2;

import java.rmi.Remote;
import java.rmi.RemoteException;

public interface RmiInterface extends Remote{
	public int getSum(int[] tableau) throws RemoteException;
}