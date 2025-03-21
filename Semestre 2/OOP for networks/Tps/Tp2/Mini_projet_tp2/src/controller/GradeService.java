package controller;

import java.rmi.Remote;
import java.rmi.RemoteException;

public interface GradeService extends Remote {
    String getGrade(String nom, String prenom, String module) throws RemoteException;
}