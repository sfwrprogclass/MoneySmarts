package moneysmarts;

public class Loan {
    public String loanType;
    public int principal;
    public double interestRate;
    public int remaining;

    public Loan(String loanType, int principal, double interestRate, int remaining) {
        this.loanType = loanType;
        this.principal = principal;
        this.interestRate = interestRate;
        this.remaining = remaining;
    }
}
package moneysmarts;

public class Asset {
    public String assetType;
    public int value;

    public Asset(String assetType, int value) {
        this.assetType = assetType;
        this.value = value;
    }
}

