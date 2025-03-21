package view;

import javafx.application.Application;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;
import javafx.scene.text.FontWeight;
import javafx.stage.Stage;
import controller.ClientController;

public class ClientGUI extends Application {
    private ClientController controller = new ClientController();

    @Override
    public void start(Stage stage) {
        // Create form components
        Label titleLabel = new Label("Consultation des Notes");
        titleLabel.setFont(Font.font("Arial", FontWeight.BOLD, 20));
        titleLabel.setTextFill(Color.DARKBLUE);

        Label nomLabel = new Label("Nom:");
        TextField nomField = new TextField();
        nomField.setPromptText("Entrez votre nom");

        Label prenomLabel = new Label("Prénom:");
        TextField prenomField = new TextField();
        prenomField.setPromptText("Entrez votre prénom");

        Label moduleLabel = new Label("Module:");
        ComboBox<String> moduleCombo = new ComboBox<>();
        moduleCombo.getItems().addAll(
            "Processeurs embarqués",
            "Systèmes distribués",
            "Qualité du logiciel"
        );
        moduleCombo.setPromptText("Sélectionnez un module");
        moduleCombo.setStyle("-fx-background-color: #f0f0f0;");

        Button btn = new Button("Afficher la note");
        btn.setStyle("-fx-background-color: #4CAF50; -fx-text-fill: white; -fx-font-weight: bold;");
        btn.setPrefWidth(200);
        
        Label resultLabel = new Label();
        resultLabel.setFont(Font.font("Arial", FontWeight.BOLD, 14));
        resultLabel.setPadding(new Insets(10, 0, 0, 0));

        // Form layout using GridPane
        GridPane formGrid = new GridPane();
        formGrid.setAlignment(Pos.CENTER);
        formGrid.setHgap(10);
        formGrid.setVgap(10);
        formGrid.setPadding(new Insets(20));
        
        formGrid.add(nomLabel, 0, 0);
        formGrid.add(nomField, 1, 0);
        formGrid.add(prenomLabel, 0, 1);
        formGrid.add(prenomField, 1, 1);
        formGrid.add(moduleLabel, 0, 2);
        formGrid.add(moduleCombo, 1, 2);

        // Main container
        VBox mainContainer = new VBox(20);
        mainContainer.setAlignment(Pos.TOP_CENTER);
        mainContainer.setPadding(new Insets(25, 25, 25, 25));
        mainContainer.setStyle("-fx-background-color: #ffffff;");
        
        // Button container
        HBox buttonContainer = new HBox();
        buttonContainer.setAlignment(Pos.CENTER);
        buttonContainer.getChildren().add(btn);

        mainContainer.getChildren().addAll(
            titleLabel,
            formGrid,
            buttonContainer,
            resultLabel
        );

        // Event handling
        btn.setOnAction(e -> {
            if (validateInput(nomField, prenomField, moduleCombo)) {
                String note = controller.getGrade(
                    nomField.getText().trim(),
                    prenomField.getText().trim(),
                    moduleCombo.getValue()
                );
                updateResultLabel(resultLabel, note);
            }
        });

        // Scene setup
        Scene scene = new Scene(mainContainer, 400, 400);
        stage.setScene(scene);
        stage.setTitle("Système de Gestion des Notes");
        stage.setMinWidth(400);
        stage.setMinHeight(400);
        stage.show();
    }

    private boolean validateInput(TextField nom, TextField prenom, ComboBox<?> module) {
        if (nom.getText().trim().isEmpty() || 
            prenom.getText().trim().isEmpty() || 
            module.getValue() == null) {
            
            showAlert("Erreur", "Veuillez remplir tous les champs obligatoires");
            return false;
        }
        return true;
    }

    private void updateResultLabel(Label label, String note) {
        try {
            double numericNote = Double.parseDouble(note);
            label.setTextFill(numericNote >= 10 ? Color.GREEN : Color.RED);
            label.setText(String.format("Note: %.2f/20", numericNote));
        } catch (NumberFormatException e) {
            label.setTextFill(Color.RED);
            label.setText(note);
        }
    }

    private void showAlert(String title, String message) {
        Alert alert = new Alert(Alert.AlertType.WARNING);
        alert.setTitle(title);
        alert.setHeaderText(null);
        alert.setContentText(message);
        alert.showAndWait();
    }

    public static void main(String[] args) {
        launch(args);
    }
}