package exo_2_tp2;

import java.rmi.Remote;
import java.rmi.RemoteException;

public interface RmiInterface extends Remote{
	public Integer getSquare(int number) throws RemoteException;
}
