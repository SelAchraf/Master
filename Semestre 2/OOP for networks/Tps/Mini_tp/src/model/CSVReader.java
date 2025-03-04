package model;

import java.io.*;
import java.util.*;

public class CSVReader {
    private List<Student> students = new ArrayList<>();

    public CSVReader(String filePath) {
        try (BufferedReader br = new BufferedReader(new FileReader(filePath))) {
            String[] headers = br.readLine().split(",");
            String line;
            while ((line = br.readLine()) != null) {
                String[] data = line.split(",");
                Map<String, String> notes = new HashMap<>();
                notes.put(headers[2], data[2]);
                notes.put(headers[3], data[3]);
                notes.put(headers[4], data[4]);
                students.add(new Student(data[0], data[1], notes));
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public String getGrade(String nom, String prenom, String module) {
        return students.stream()
            .filter(s -> s.getNom().equalsIgnoreCase(nom) && s.getPrenom().equalsIgnoreCase(prenom))
            .map(s -> s.getNotes().getOrDefault(module, "Non trouvé"))
            .findFirst()
            .orElse("Étudiant non trouvé");
    }
}