package controller;

import java.rmi.server.UnicastRemoteObject;
import java.rmi.RemoteException;
import model.CSVReader;

public class GradeServiceImpl extends UnicastRemoteObject implements GradeService {
    private static final long serialVersionUID = 1L;
	private CSVReader csvReader;

    public GradeServiceImpl() throws RemoteException {
        super();
        this.csvReader = new CSVReader("resources/students.csv");
    }

    @Override
    public String getGrade(String nom, String prenom, String module) throws RemoteException {
        return csvReader.getGrade(nom, prenom, module);
    }
}