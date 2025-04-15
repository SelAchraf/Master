package exo1_tp3;

import javax.swing.*;
import java.util.ArrayList;
import java.util.List;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class CompositeCommande implements Commande, ActionListener {
    
    private String nom;
    private List<Commande> sousCommandes = new ArrayList<>();
    private JButton button;
    
    public CompositeCommande(String nom) {
        this.nom = nom;
        this.button = new JButton(nom);
        this.button.addActionListener(this);
    }

    public void add(Commande commande) {
        sousCommandes.add(commande);
    }

    public void remove(Commande commande) {
        sousCommandes.remove(commande);
    }

    @Override
    public void setEnabled(boolean enabled) {
        button.setEnabled(enabled);
        // Apply the same logic to the children commands
        for (Commande commande : sousCommandes) {
            commande.setEnabled(enabled);
        }
    }

    @Override
    public void actionPerformed(ActionEvent e) {
    	this.setEnabled(true);
    }

    public JButton getButton() {
        return button;
    }

    @Override
    public String toString() {
        return nom;
    }
}
