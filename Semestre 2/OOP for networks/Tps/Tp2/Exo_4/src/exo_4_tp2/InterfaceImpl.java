package exo_4_tp2;

import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;

public class InterfaceImpl extends UnicastRemoteObject implements RmiInterface {

	protected InterfaceImpl() throws RemoteException {
		super();
	}

	private static final long serialVersionUID = 1L;

	@Override
	public int getSum(int[] tableau) throws RemoteException {
        int somme = 0;
        for (int num : tableau) {
            somme += num;
        }
        return somme;
	}

}