package exo_1_tp2;

import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;
import java.text.SimpleDateFormat;
import java.util.Date;

public class InterfaceImpl extends UnicastRemoteObject implements RmiInterface {
    private static final long serialVersionUID = 1L;

    // Constructor
    public InterfaceImpl() throws RemoteException {
        super(); // This exports the remote object
    }
    
    @Override
	public String getDate() throws RemoteException{
        String dateActuelle = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(new Date());
        return dateActuelle;
	}
}