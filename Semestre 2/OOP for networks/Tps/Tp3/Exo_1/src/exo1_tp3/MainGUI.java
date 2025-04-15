package exo1_tp3;

import javax.swing.*;
import java.awt.*;
import java.util.Hashtable;

public class MainGUI {

    public static void main(String[] args) {
        // === Create leaf commandes ===
        LeafCommande stocker = new LeafCommande("Stocker");
        LeafCommande jeter = new LeafCommande("Jeter");
        LeafCommande nettoyer = new LeafCommande("Nettoyer");

        // === Create composite commandes with names ===
        CompositeCommande empaqueter = new CompositeCommande("Empaqueter");
        CompositeCommande decouper = new CompositeCommande("Découper");
        CompositeCommande diagnostique = new CompositeCommande("Diagnostique");

        // === Build command hierarchy ===
        empaqueter.add(stocker);
        decouper.add(jeter);
        decouper.add(empaqueter);
        diagnostique.add(nettoyer);

        // === GUI Setup ===
        JFrame frame = new JFrame("Commande Machine");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(500, 400);
        frame.setLayout(new BorderLayout());

        // === Slider Panel ===
        JPanel sliderPanel = new JPanel(new BorderLayout());
        JLabel label = new JLabel("État de la machine", SwingConstants.CENTER);

        JSlider slider = new JSlider(0, 1, 1); // 0 = En marche, 1 = À l'arrêt
        slider.setPaintTicks(false);
        slider.setPaintLabels(true);
        slider.setMajorTickSpacing(1);

        Hashtable<Integer, JLabel> labelTable = new Hashtable<>();
        labelTable.put(0, new JLabel("En marche"));
        labelTable.put(1, new JLabel("À l'arrêt"));
        slider.setLabelTable(labelTable);

        sliderPanel.add(label, BorderLayout.NORTH);
        sliderPanel.add(slider, BorderLayout.CENTER);

        // === Buttons ===
        JButton btnDecouper = decouper.getButton();
        JButton btnDiagnostique = diagnostique.getButton();
        JButton btnEmpaqueter = empaqueter.getButton();
        JButton btnJeter = jeter.getButton();
        JButton btnNettoyer = nettoyer.getButton();
        JButton btnStocker = stocker.getButton();

        // === Layout Hierarchy ===
        JPanel hierarchyPanel = new JPanel(new GridLayout(3, 1));

        JPanel row1 = new JPanel(new FlowLayout(FlowLayout.CENTER, 40, 5));
        JPanel row2 = new JPanel(new FlowLayout(FlowLayout.CENTER, 40, 5));
        JPanel row3 = new JPanel(new FlowLayout(FlowLayout.CENTER, 40, 5));

        row1.add(btnDecouper);
        row1.add(btnDiagnostique);

        row2.add(btnEmpaqueter);
        row2.add(btnJeter);
        row2.add(btnNettoyer);

        row3.add(btnStocker);

        hierarchyPanel.add(row1);
        hierarchyPanel.add(row2);
        hierarchyPanel.add(row3);

        // === Slider Logic ===
        slider.addChangeListener(e -> {
            boolean machineOn = slider.getValue() == 0;

            // Enable only top-level composite commands
            btnDecouper.setEnabled(machineOn);
            btnDiagnostique.setEnabled(!machineOn);

            // Disable all others initially
            btnEmpaqueter.setEnabled(false);
            btnJeter.setEnabled(false);
            btnNettoyer.setEnabled(false);
            btnStocker.setEnabled(false);
        });

        // === Initial State ===
        btnDecouper.setEnabled(false);
        btnDiagnostique.setEnabled(true);
        btnEmpaqueter.setEnabled(false);
        btnJeter.setEnabled(false);
        btnNettoyer.setEnabled(false);
        btnStocker.setEnabled(false);

        // === Assemble GUI ===
        frame.add(sliderPanel, BorderLayout.NORTH);
        frame.add(hierarchyPanel, BorderLayout.CENTER);
        frame.setVisible(true);
    }
}
