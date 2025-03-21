package exo_2_tp2;

import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;

public class InterfaceImpl extends UnicastRemoteObject implements RmiInterface {

	protected InterfaceImpl() throws RemoteException {
		super();
	}

	private static final long serialVersionUID = 1L;

	@Override
	public Integer getSquare(int number) throws RemoteException {
		Integer Square = number * number;
		return Square;
	}
	
}