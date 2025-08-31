package moneysmarts;

import java.util.*;

public class Player {
    public String name;
    public int cash;
    public int salary;
    public List<Asset> assets;

    public Player(String name) {
        this.name = name;
        this.cash = 0;
        this.salary = 0;
        this.assets = new ArrayList<>();
    }

    public boolean hasCar() {
        for (Asset asset : assets) {
            if ("Car".equals(asset.assetType)) {
                return true;
            }
        }
        return false;
    }
}

