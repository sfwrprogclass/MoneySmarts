package moneysmarts;

import java.util.logging.*;

public class MoneySmartzMain {
    // GUI Constants
    public static final int SCREEN_WIDTH = 1024;
    public static final int SCREEN_HEIGHT = 768;
    public static final int FPS = 60;
    // Colors (RGB)
    public static final int[] WHITE = {255, 255, 255};
    public static final int[] BLACK = {0, 0, 0};
    public static final int[] GRAY = {200, 200, 200};
    public static final int[] LIGHT_GRAY = {230, 230, 230};
    public static final int[] DARK_GRAY = {100, 100, 100};
    public static final int[] BLUE = {0, 120, 255};
    public static final int[] LIGHT_BLUE = {100, 180, 255};
    public static final int[] GREEN = {0, 200, 0};

    public static void main(String[] args) {
        // Set up logging
        Logger logger = Logger.getLogger("MoneySmartzLogger");
        try {
            FileHandler fh = new FileHandler("money_smarts.log");
            fh.setFormatter(new SimpleFormatter());
            logger.addHandler(fh);
            logger.setLevel(Level.SEVERE);
        } catch (Exception e) {
            System.out.println("Logging setup failed.");
        }

        try {
            // TODO: Initialize game window and assets using Java game library
            // Game game = new Game();
            // GUIManager guiManager = new GUIManager(game);
            // guiManager.setScreen(new TitleScreen(game));
            // guiManager.run();
        } catch (Exception e) {
            logger.severe("Uncaught exception: " + e.getMessage());
            System.out.println("An unexpected error occurred. Please check money_smarts.log for details.");
            e.printStackTrace();
        }
    }
}
