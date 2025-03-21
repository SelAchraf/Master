package controller;

import java.rmi.Naming;

public class ClientController {
    private GradeService gradeService;

    public ClientController() {
        try {
            // Look up the remote object using Naming.lookup
            gradeService = (GradeService) Naming.lookup("rmi://localhost:1099/GradeService");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public String getGrade(String nom, String prenom, String module) {
        try {
            return gradeService.getGrade(nom, prenom, module);
        } catch (Exception e) {
            return "Erreur de connexion";
        }
    }
}