package exo_1_tp2;


import java.rmi.Remote;
import java.rmi.RemoteException;

public interface RmiInterface extends Remote {
	public String getDate() throws RemoteException;
}