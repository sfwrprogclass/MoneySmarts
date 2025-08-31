package moneysmarts;

import java.util.Random;

public class EventEffects {
    private static final Random rand = new Random();

    public static int taxRefundEffect() {
        return rand.nextInt(901) + 100;
    }
    public static int birthdayGiftEffect() {
        return rand.nextInt(181) + 20;
    }
    public static int foundMoneyEffect() {
        return rand.nextInt(46) + 5;
    }
    public static int bonusEffect(Game game) {
        return (game.player != null && game.player.salary > 0) ? (int)(game.player.salary * (0.01 + rand.nextDouble() * 0.09)) : 0;
    }
    public static int carRepairEffect(Game game) {
        return (game.player != null && game.player.hasCar()) ? -1 * (rand.nextInt(1901) + 100) : 0;
    }
    public static int medicalBillEffect() {
        return -1 * (rand.nextInt(4951) + 50);
    }
    public static int lostWalletEffect(Game game) {
        return (game.player != null) ? -1 * Math.min(50, game.player.cash) : 0;
    }
    public static int phoneRepairEffect() {
        return -1 * (rand.nextInt(251) + 50);
    }
}

