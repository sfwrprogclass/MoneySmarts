package moneysmarts;

public class Card {
    public String cardType;
    public int limit;
    public int balance;

    public Card(String cardType, int limit, int balance) {
        this.cardType = cardType;
        this.limit = limit;
        this.balance = balance;
    }
}

