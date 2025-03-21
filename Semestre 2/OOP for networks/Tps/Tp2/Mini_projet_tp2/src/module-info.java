/**
 * 
 */
/**
 * 
 */
module Mini_projet_tp2 {
	requires javafx.graphics;
	
    // Required modules for JavaFX
    requires javafx.controls;
    requires javafx.fxml;

    // Required modules for RMI
    requires java.rmi;

    // Opens the 'view' package to JavaFX for reflection
    opens view to javafx.graphics, javafx.fxml;

    // Exports the 'controller' package for RMI (if needed)
    exports controller;
}