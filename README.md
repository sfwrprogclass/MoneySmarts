# MoneySmarts: Financial Life Simulator

MoneySmarts is an educational financial life simulator game. Players make real-world financial decisions, manage budgets, purchase homes and vehicles, handle life events, and learn about personal finance in a fun, interactive way.

## Game Overview
- Start as a high school student and open your first bank account
- Make education choices (college, trade school, or start working)
- Apply for credit cards and build your credit score
- Buy vehicles and manage transportation costs
- Find jobs and advance your career
- Purchase a home and manage a mortgage
- Start a family and handle expenses
- Deal with random life events
- Save for retirement and build wealth

## Features
- Realistic banking, credit, and loan systems
- Asset management (homes, vehicles, investments)
- Family planning and life events
- Recurring bills and budgeting
- Pixel art graphics and engaging UI
- Save/load game progress
- Hot-swappable images and Unity export support

## How to Play
1. Install Python and Pygame (`pip install pygame`)
2. Run the game: `python main.py`
3. Use your mouse to navigate the interface and make decisions
4. Try to maximize your net worth and achieve financial security by retirement

## Controls
- Mouse: interact with buttons and menus
- Keyboard: ESC or Backspace to go back

## Assets
All game assets (images, sounds, fonts) are in the `assets/` folder. Images are hot-swappable and can be exported for Unity via the automated script in `moneySmarts/image_manager.py`.

## Project Structure
- Modular MVC architecture
- Models: game entities (Player, BankAccount, Card, Loan, Asset)
- Views: UI components and screens
- Controller: game logic and state management

## Development Status
- Basic game functionality implemented
- Modular architecture and MVC pattern in progress
- Migration from monolithic to modular structure ongoing
- Documentation and feature improvements ongoing

## Financial Education
Learn about:
- Budgeting and saving
- Credit management
- Loan amortization
- Asset depreciation/appreciation
- Investment growth
- Income progression
- Financial planning

## Unity Export
To export all images for Unity, run:
```bash
python moneySmarts/image_manager.py
```
This will copy all PNG/JPG images from `assets/images` to `assets/unity_export` for easy Unity import.

## How to Contribute
1. Check `docs/tasks.md` for planned improvements
2. Fork the repository
3. Create a feature branch
4. Commit and push your changes
5. Open a Pull Request

## Tips for Success
- Education leads to higher income potential
- Pay off high-interest debt first
- Save for emergencies
- Invest early for retirement
- Don’t buy more house than you can afford
- Maintain good credit by paying bills on time

## License
This project is for educational purposes. See LICENSE for details.

Enjoy your financial journey!
