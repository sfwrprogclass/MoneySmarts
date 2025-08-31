package moneysmarts;

public class Utils {
    public static int computeNetWorth(Player player) {
        int netWorth = player.cash;
        // Add asset values
        for (Asset asset : player.assets) {
            netWorth += asset.value;
        }
        // TODO: Add bank accounts, cards, loans if Player is extended
        // Example:
        // for (BankAccount account : player.bankAccounts) {
        //     netWorth += account.balance;
        // }
        // for (Card card : player.cards) {
        //     netWorth -= card.balance;
        // }
        // for (Loan loan : player.loans) {
        //     netWorth -= loan.remaining;
        // }
        return netWorth;
    }
}
package moneysmarts;

public class Event {
    public String name;
    public String description;
    public int cashEffect;

    public Event(String name, String description, int cashEffect) {
        this.name = name;
        this.description = description;
        this.cashEffect = cashEffect;
    }
}
