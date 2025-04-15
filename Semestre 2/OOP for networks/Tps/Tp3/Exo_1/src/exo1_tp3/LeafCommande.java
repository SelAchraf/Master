package exo1_tp3;

import javax.swing.*;

public class LeafCommande implements Commande {
    private String nom;
    private boolean enabled;
    private JButton button;

    public LeafCommande(String nom) {
        this.nom = nom;
        this.enabled = true; // default state
        this.button = new JButton(nom);
    }

    @Override
    public void setEnabled(boolean enabled) {
        this.enabled = enabled;
        button.setEnabled(enabled);
    }

    public boolean isEnabled() {
        return enabled;
    }

    public JButton getButton() {
        return button;
    }

    @Override
    public String toString() {
        return nom;
    }
}
