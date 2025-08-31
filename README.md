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

## Development Environment Setup
Use the helper scripts in `scripts/` to create and maintain a local virtual environment:

Windows (Batch / CMD):
```
scripts\auto_start_env.bat [/force] [/noupgrade] [/quiet] [/pause] [/help]
```
PowerShell:
```
powershell -NoLogo -NoExit -ExecutionPolicy Bypass -File scripts/auto_start_env.ps1 [-Force] [-NoUpgrade] [-Quiet] [-Critical pkg1,pkg2] [-Help]
```
Flags:
- force / -Force: Force dependency upgrade even if already upgraded today.
- noupgrade / -NoUpgrade: Skip dependency upgrade (still shows outdated report).
- quiet / -Quiet: Suppress informational output.
- pause: (batch only) Pause before closing the window (useful when double-clicking).
- help / -Help: Show usage and exit.
- -Critical: (PowerShell) Specify additional critical packages to verify (default includes pygame).

Exit codes (both scripts): 0=Success, 1=Script failure, 2=Critical package(s) missing.

Daily Upgrades: The scripts store the last upgrade date in `.venv/last_upgrade.txt` and will skip subsequent upgrades the same day unless forced.

Outdated Report: After (or even if skipping) upgrades, an informational list of outdated packages is printed.

Critical Package Check: Verifies that required gameplay libraries (e.g. pygame) can be imported; exits with code 2 if missing.

Manual setup (alternative):
```bash
python -m venv .venv
. .venv/bin/activate  # Linux/macOS
# or on Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -e .[dev]
```

## Running Tests
After environment setup:
```bash
pytest
```
Add `-q` for quiet mode or `--cov` for coverage if `pytest-cov` is installed:
```bash
pytest --cov=moneySmarts --cov-report=term-missing
```

## Linting & Quality
Run Ruff lint:
```bash
python -m ruff check .
```
Or use the Makefile targets (on systems with make):
```bash
make lint
make test
make quality   # runs lint + tests
```

## Continuous Integration
A GitHub Actions workflow (`.github/workflows/ci.yml`) runs on pushes and pull requests for Python 3.11 and 3.12:
- Installs project with dev extras
- Runs Ruff lint
- Executes pytest (headless SDL via dummy driver)

Badges or status indicators can be added later if desired.

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
