# MoneySmarts: Financial Life Simulator

MoneySmarts is an educational and entertaining financial life simulator game. Players make real-world financial decisions, manage budgets, purchase homes and vehicles, handle life events, and learn about personal finance in a fun, interactive way.

## Game Overview

In MoneySmarts, you'll navigate the financial challenges and opportunities of life:

- Start as a high school student getting your first bank account
- Make education decisions (college, trade school, or start working)
- Apply for credit cards and build your credit score
- Buy vehicles and manage transportation costs
- Find jobs and advance your career
- Purchase a home and manage a mortgage
- Start a family and handle the associated expenses
- Deal with random life events (both positive and negative)
- Save for retirement and build wealth

## Features

- Buy homes and vehicles with realistic financial constraints
- Shop for everyday items and manage recurring bills
- Experience random and planned life events
- Track your cash, bank, and credit balances
- Inventory and recurring bill management
- Pixel art graphics and engaging UI
- Save/load game progress

## How to Play

1. Make sure you have Python installed on your computer
2. Install Pygame: `pip install pygame`
3. Run the game by executing: `python main.py`
4. Use your mouse to navigate the graphical interface and make decisions
5. Try to maximize your net worth and achieve financial security by retirement

## GUI Features

- **Intuitive Interface**: Easy-to-navigate screens with buttons and visual feedback
- **Financial Dashboard**: Visual representation of your financial status
- **Interactive Decisions**: Make life choices through a point-and-click interface
- **Visual Feedback**: Color-coded indicators for positive and negative events
- **End Game Summary**: Visual breakdown of your financial success

## Game Features

- **Banking System**: Open accounts, make deposits and withdrawals, earn interest
- **Credit System**: Apply for credit cards, make payments, build credit score
- **Loan Management**: Take out loans for education, vehicles, and housing
- **Career Progression**: Find better jobs as you gain education and experience
- **Asset Management**: Purchase and maintain assets like vehicles and homes
- **Family Planning**: Get married, have children, and manage family expenses
- **Random Events**: Experience unexpected financial events (medical bills, bonuses, etc.)

## Financial Education

This game teaches important financial concepts:
- Budgeting and saving
- Credit management
- Loan amortization
- Asset depreciation and appreciation
- Investment growth
- Income progression
- Financial planning

## Project Structure

The project follows a modular architecture with the Model-View-Controller (MVC) pattern:

- **Models** (`moneySmarts/models.py`): Data structures for game entities (Player, BankAccount, Card, Loan, Asset)
- **Views** (`moneySmarts/ui.py` and `moneySmarts/screens/`): UI components and screen classes
- **Controller** (`moneySmarts/game.py`): Game logic and state management

### Directory Structure:
```
moneySmartz2/
├── docs/
│   └── tasks.md         # Development tasks and roadmap
├── moneySmarts/
│   ├── screens/         # Screen classes organized by category
│   ├── __init__.py      # Package initialization
│   ├── constants.py     # Game constants and configuration
│   ├── game.py          # Game logic (controller)
│   ├── models.py        # Data models
│   └── ui.py            # UI components
├── main.py              # Entry point
├── moneySmartz.py       # Legacy monolithic file (being migrated)
└── README.md            # This file
```

## Development Status

This project is under active development. Current progress:

- ✅ Basic game functionality implemented
- ✅ Modular architecture started
- ✅ MVC pattern partially implemented
- 🔄 Migration from monolithic to modular structure in progress
- 📝 Documentation improvements ongoing
- 🚧 Many features planned (see `docs/tasks.md`)

## Getting Started
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Run the game:**
   ```bash
   python main.py
   ```

## Controls
- Use your mouse to interact with buttons and menus
- Keyboard shortcuts: ESC or Backspace to go back

## Assets
All game assets (images, sounds, fonts) are located in the `assets/` folder.

## How to Contribute

Contributions are welcome! Here's how you can help:

1. Check the `docs/tasks.md` file for planned improvements
2. Fork the repository
3. Create a feature branch (`git checkout -b feature/amazing-feature`)
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## Tips for Success

- Education generally leads to higher income potential
- Pay off high-interest debt first
- Save for emergencies
- Invest early for retirement
- Don't buy more house than you can afford
- Maintain good credit by paying bills on time

## License
This project is for educational purposes. See LICENSE for details.

Enjoy your financial journey!
