package moneysmarts;

import java.util.*;

public class Game {
    public Player player;
    public int currentMonth = 1;
    public int currentYear = 0; // offset from 2023
    public boolean gameOver = false;
    public Map<String, List<Event>> events;
    public GUIManager guiManager;
    public boolean paused = false;
    public QuestManager quests;
    public List<String> questNotifications = new ArrayList<>();
    public boolean metMentor = false;

    public Game() {
        this.events = initializeEvents();
        this.quests = new QuestManager(this);
    }

    public int computeNetWorth() {
        if (player == null) return 0;
        return Utils.computeNetWorth(player);
    }

    private Map<String, List<Event>> initializeEvents() {
        Map<String, List<Event>> eventMap = new HashMap<>();
        eventMap.put("positive", Arrays.asList(
            new Event("Tax Refund", "You received a tax refund!", EventEffects.taxRefundEffect()),
            new Event("Birthday Gift", "You received money as a birthday gift!", EventEffects.birthdayGiftEffect()),
            new Event("Found Money", "You found money on the ground!", EventEffects.foundMoneyEffect()),
            new Event("Bonus", "You received a bonus at work!", EventEffects.bonusEffect(this))
        ));
        eventMap.put("negative", Arrays.asList(
            new Event("Car Repair", "Your car needs repairs.", EventEffects.carRepairEffect(this)),
            new Event("Medical Bill", "Unexpected medical expenses.", EventEffects.medicalBillEffect()),
            new Event("Lost Wallet", "You lost your wallet!", EventEffects.lostWalletEffect(this)),
            new Event("Phone Repair", "Phone screen cracked.", EventEffects.phoneRepairEffect())
        ));
        return eventMap;
    }
}

