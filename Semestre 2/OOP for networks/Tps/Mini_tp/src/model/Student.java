package model;

import java.util.Map;

public class Student {
    private String nom;
    private String prenom;
    private Map<String, String> notes;

    public Student(String nom, String prenom, Map<String, String> notes) {
        this.nom = nom;
        this.prenom = prenom;
        this.notes = notes;
    }

    // Getters
    public String getNom() { return nom; }
    public String getPrenom() { return prenom; }
    public Map<String, String> getNotes() { return notes; }
}