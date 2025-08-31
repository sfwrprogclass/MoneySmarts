package moneysmarts;

import javafx.scene.control.Button;
import javafx.scene.text.Font;

public class GameButton extends Button {
    public GameButton(String text, int fontSize) {
        super(text);
        setFont(new Font("Arial", fontSize));
        // TODO: Add color, hover effects, and action handling
    }
}

