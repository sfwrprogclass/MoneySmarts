import pygame
import random
from pygame.locals import *
from moneySmartz.constants import *
from moneySmartz.ui import Screen, Button, TextInput
from moneySmartz.models import Loan, Asset, Card

BROWN = (139, 69, 19)

class HighSchoolGraduationScreen(Screen):
    """
    Screen for high school graduation event.
    """
    def __init__(self, game):
        super().__init__(game)

        # Title
        self.title_font = pygame.font.SysFont('Arial', FONT_LARGE)
        self.text_font = pygame.font.SysFont('Arial', FONT_MEDIUM)

        # Buttons
        college_button = Button(
            SCREEN_WIDTH // 2 - 150,
            SCREEN_HEIGHT - 210,
            300, 50,
            "Go to College ($20,000/year)",
            action=self.go_to_college
        )

        trade_button = Button(
            SCREEN_WIDTH // 2 - 150,
            SCREEN_HEIGHT - 150,
            300, 50,
            "Go to Trade School ($10,000)",
            action=self.go_to_trade_school
        )

        work_button = Button(
            SCREEN_WIDTH // 2 - 150,
            SCREEN_HEIGHT - 90,
            300, 50,
            "Start Working Full-time",
            action=self.start_working
        )

        self.buttons = [college_button, trade_button, work_button]

    def go_to_college(self):
        """Choose to go to college."""
        # Check if player can afford college
        annual_cost = 20000
        if self.game.player.cash >= annual_cost:
            self.game.player.cash -= annual_cost
        elif self.game.player.bank_account and self.game.player.bank_account.balance >= annual_cost:
            self.game.player.bank_account.withdraw(annual_cost)
        else:
            # Need a student loan
            loan_amount = 80000  # 4 years of college
            loan = Loan("Student", loan_amount, 0.05, 20)  # 5% interest, 20-year term
            self.game.player.loans.append(loan)

        self.game.player.education = "College (In Progress)"

        # Return to game screen
        from moneySmartz.screens.game_screen import GameScreen
        self.game.gui_manager.set_screen(GameScreen(self.game))

    def go_to_trade_school(self):
        """Choose to go to trade school."""
        # Check if player can afford trade school
        cost = 10000
        if self.game.player.cash >= cost:
            self.game.player.cash -= cost
        elif self.game.player.bank_account and self.game.player.bank_account.balance >= cost:
            self.game.player.bank_account.withdraw(cost)
        else:
            # Need a student loan
            loan = Loan("Student", cost, 0.05, 10)  # 5% interest, 10-year term
            self.game.player.loans.append(loan)

        self.game.player.education = "Trade School"

        # Return to game screen
        from moneySmartz.screens.game_screen import GameScreen
        self.game.gui_manager.set_screen(GameScreen(self.game))

    def start_working(self):
        """Choose to start working full-time."""
        self.game.player.education = "High School Graduate"

        # Go to job search screen
        from moneySmartz.screens.financial_screens import JobSearchScreen
        self.game.gui_manager.set_screen(JobSearchScreen(self.game))

    def draw(self, surface):
        """Draw the high school graduation screen."""
        # Background
        surface.fill(WHITE)

        # Title
        title_surface = self.title_font.render("HIGH SCHOOL GRADUATION", True, BLUE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 80))
        surface.blit(title_surface, title_rect)

        # Graduation cap image (simple triangle and rectangle)
        cap_center_x = SCREEN_WIDTH // 2
        cap_center_y = 180

        # Draw cap
        pygame.draw.rect(surface, BLACK, (cap_center_x - 50, cap_center_y - 10, 100, 20))

        # Draw tassel
        pygame.draw.line(surface, YELLOW, (cap_center_x + 40, cap_center_y), (cap_center_x + 60, cap_center_y + 30), 5)
        pygame.draw.circle(surface, YELLOW, (cap_center_x + 60, cap_center_y + 40), 10)

        # Draw top
        pygame.draw.polygon(surface, BLACK, [
            (cap_center_x - 50, cap_center_y - 10),
            (cap_center_x + 50, cap_center_y - 10),
            (cap_center_x, cap_center_y - 60)
        ])

        # Explanation text
        text_lines = [
            "Congratulations! You've graduated from high school.",
            "It's time to make some important decisions about your future.",
            "",
            "You can go to college, which costs $20,000 per year for 4 years,",
            "but may lead to higher-paying jobs in the future.",
            "",
            "You can go to trade school, which costs $10,000 for 2 years,",
            "and can lead to specialized technical careers.",
            "",
            "Or you can start working full-time right away with your high school diploma.",
            "",
            "What would you like to do?"
        ]

        for i, line in enumerate(text_lines):
            text_surface = self.text_font.render(line, True, BLACK)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 250 + i * 30))
            surface.blit(text_surface, text_rect)

        # Draw buttons
        for button in self.buttons:
            button.draw(surface)

class CollegeGraduationScreen(Screen):
    """
    Screen for college graduation event.
    """
    def __init__(self, game):
        super().__init__(game)

        # Title
        self.title_font = pygame.font.SysFont('Arial', FONT_LARGE)
        self.text_font = pygame.font.SysFont('Arial', FONT_MEDIUM)

        # Buttons
        continue_button = Button(
            SCREEN_WIDTH // 2 - 100,
            SCREEN_HEIGHT - 90,
            200, 50,
            "Continue",
            action=self.continue_to_job_search
        )

        self.buttons = [continue_button]

    def continue_to_job_search(self):
        """Continue to job search after graduation."""
        # Update education status
        self.game.player.education = "College Graduate"

        # Boost credit score
        self.game.player.credit_score += 20  # Education boosts credit score

        # Go to job search screen
        from moneySmartz.screens.financial_screens import JobSearchScreen
        self.game.gui_manager.set_screen(JobSearchScreen(self.game))

    def draw(self, surface):
        """Draw the college graduation screen."""
        # Background
        surface.fill(WHITE)

        # Title
        title_surface = self.title_font.render("COLLEGE GRADUATION", True, BLUE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 80))
        surface.blit(title_surface, title_rect)

        # Graduation cap image (simple triangle and rectangle)
        cap_center_x = SCREEN_WIDTH // 2
        cap_center_y = 180

        # Draw cap
        pygame.draw.rect(surface, BLACK, (cap_center_x - 50, cap_center_y - 10, 100, 20))

        # Draw tassel
        pygame.draw.line(surface, YELLOW, (cap_center_x + 40, cap_center_y), (cap_center_x + 60, cap_center_y + 30), 5)
        pygame.draw.circle(surface, YELLOW, (cap_center_x + 60, cap_center_y + 40), 10)

        # Draw top
        pygame.draw.polygon(surface, BLACK, [
            (cap_center_x - 50, cap_center_y - 10),
            (cap_center_x + 50, cap_center_y - 10),
            (cap_center_x, cap_center_y - 60)
        ])

        # Explanation text
        text_lines = [
            "Congratulations! You've graduated from college with a bachelor's degree.",
            "Your education will open up better job opportunities.",
            "",
            "Your credit score has increased due to your educational achievement.",
            f"Your credit score is now {self.game.player.credit_score}.",
            "",
            "With your new degree, you have access to better job opportunities.",
            "Let's look for a job that matches your qualifications!"
        ]

        for i, line in enumerate(text_lines):
            text_surface = self.text_font.render(line, True, BLACK)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 250 + i * 30))
            surface.blit(text_surface, text_rect)

        # Draw buttons
        for button in self.buttons:
            button.draw(surface)

class CarPurchaseScreen(Screen):
    """
    Screen for car purchase opportunity.
    """
    def __init__(self, game):
        super().__init__(game)

        # Title
        self.title_font = pygame.font.SysFont('Arial', FONT_LARGE)
        self.text_font = pygame.font.SysFont('Arial', FONT_MEDIUM)

        # Car options
        self.car_options = [
            {"name": "Used Economy Car", "value": 5000},
            {"name": "New Economy Car", "value": 18000},
            {"name": "Used Luxury Car", "value": 15000},
            {"name": "New Luxury Car", "value": 35000},
        ]

        # Selected car
        self.selected_car = None

        # Payment method
        self.payment_method = None

        # State (0 = car selection, 1 = payment selection, 2 = confirmation)
        self.state = 0

        # Create car selection buttons
        self.create_car_buttons()

    def create_car_buttons(self):
        """Create buttons for car selection."""
        self.buttons = []

        if self.state == 0:
            # Car selection buttons
            for i, car in enumerate(self.car_options):
                car_button = Button(
                    SCREEN_WIDTH // 2 - 150,
                    250 + i * 60,
                    300, 50,
                    f"{car['name']} - ${car['value']}",
                    action=lambda c=car: self.select_car(c)
                )
                self.buttons.append(car_button)

            # Skip button
            skip_button = Button(
                SCREEN_WIDTH // 2 - 100,
                SCREEN_HEIGHT - 90,
                200, 50,
                "Skip for Now",
                action=self.skip_purchase
            )
            self.buttons.append(skip_button)

        elif self.state == 1:
            # Payment method buttons
            payment_options = ["Cash"]

            if self.game.player.bank_account and self.game.player.bank_account.balance >= self.selected_car['value']:
                payment_options.append("Bank Account")

            payment_options.append("Auto Loan")

            for i, method in enumerate(payment_options):
                method_button = Button(
                    SCREEN_WIDTH // 2 - 100,
                    300 + i * 60,
                    200, 50,
                    method,
                    action=lambda m=method: self.select_payment_method(m)
                )
                self.buttons.append(method_button)

            # Back button
            back_button = Button(
                SCREEN_WIDTH // 2 - 100,
                SCREEN_HEIGHT - 90,
                200, 50,
                "Back",
                action=self.go_back_to_car_selection
            )
            self.buttons.append(back_button)

        elif self.state == 2:
            # Confirmation button
            confirm_button = Button(
                SCREEN_WIDTH // 2 - 100,
                SCREEN_HEIGHT - 90,
                200, 50,
                "Continue",
                action=self.confirm_purchase
            )
            self.buttons.append(confirm_button)

    def select_car(self, car):
        """Select a car to purchase."""
        self.selected_car = car
        self.state = 1
        self.create_car_buttons()

    def go_back_to_car_selection(self):
        """Go back to car selection."""
        self.state = 0
        self.create_car_buttons()

    def select_payment_method(self, method):
        """Select a payment method."""
        self.payment_method = method

        # Process payment
        if method == "Cash" and self.game.player.cash >= self.selected_car['value']:
            self.game.player.cash -= self.selected_car['value']
        elif method == "Bank Account":
            self.game.player.bank_account.withdraw(self.selected_car['value'])
        else:  # Auto Loan
            # Determine loan terms based on credit score
            if self.game.player.credit_score >= 700:
                interest_rate = 0.03  # 3%
            elif self.game.player.credit_score >= 650:
                interest_rate = 0.05  # 5%
            else:
                interest_rate = 0.08  # 8%

            loan = Loan("Auto", self.selected_car['value'], interest_rate, 5)  # 5-year auto loan
            self.game.player.loans.append(loan)

        # Add car to assets
        self.game.player.assets.append(Asset("Car", self.selected_car['name'], self.selected_car['value']))

        # Move to confirmation
        self.state = 2
        self.create_car_buttons()

    def skip_purchase(self):
        """Skip car purchase."""
        from moneySmartz.screens.game_screen import GameScreen
        self.game.gui_manager.set_screen(GameScreen(self.game))

    def confirm_purchase(self):
        """Confirm purchase and return to game."""
        from moneySmartz.screens.game_screen import GameScreen
        self.game.gui_manager.set_screen(GameScreen(self.game))

    def draw(self, surface):
        """Draw the car purchase screen."""
        # Background
        surface.fill(WHITE)

        # Title
        title_surface = self.title_font.render("CAR PURCHASE OPPORTUNITY", True, BLUE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 80))
        surface.blit(title_surface, title_rect)

        if self.state == 0:
            # Car selection state
            text_lines = [
                "You're now at an age where having your own car could be beneficial.",
                "Would you like to look at some car options?",
                "",
                "Select a car to purchase:"
            ]

            for i, line in enumerate(text_lines):
                text_surface = self.text_font.render(line, True, BLACK)
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 150 + i * 30))
                surface.blit(text_surface, text_rect)

        elif self.state == 1:
            # Payment method selection state
            text_lines = [
                f"You've selected the {self.selected_car['name']} for ${self.selected_car['value']}.",
                "",
                "How would you like to pay?"
            ]

            for i, line in enumerate(text_lines):
                text_surface = self.text_font.render(line, True, BLACK)
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 150 + i * 30))
                surface.blit(text_surface, text_rect)

        elif self.state == 2:
            # Confirmation state
            text_lines = [
                f"Congratulations on your new {self.selected_car['name']}!",
                "",
                f"You paid using {self.payment_method}."
            ]

            if self.payment_method == "Auto Loan":
                loan = self.game.player.loans[-1]  # The loan we just added
                text_lines.extend([
                    "",
                    f"Your auto loan details:",
                    f"Amount: ${loan.original_amount:.2f}",
                    f"Interest Rate: {loan.interest_rate*100:.1f}%",
                    f"Monthly Payment: ${loan.monthly_payment:.2f}",
                    f"Term: {loan.term_years} years"
                ])

            for i, line in enumerate(text_lines):
                text_surface = self.text_font.render(line, True, BLACK)
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 150 + i * 30))
                surface.blit(text_surface, text_rect)

            # Draw car image (simple rectangle)
            car_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 350, 200, 100)
            pygame.draw.rect(surface, BLUE, car_rect)
            pygame.draw.rect(surface, BLACK, car_rect, 2)  # Border

            # Draw wheels
            pygame.draw.circle(surface, BLACK, (SCREEN_WIDTH // 2 - 60, 450), 20)
            pygame.draw.circle(surface, BLACK, (SCREEN_WIDTH // 2 + 60, 450), 20)

        # Draw buttons
        for button in self.buttons:
            button.draw(surface)

class HousingScreen(Screen):
    """
    Screen for house purchase opportunity.
    """
    def __init__(self, game):
        super().__init__(game)

        # Title
        self.title_font = pygame.font.SysFont('Arial', FONT_LARGE)
        self.text_font = pygame.font.SysFont('Arial', FONT_MEDIUM)

        # House options
        self.house_options = [
            {"name": "Small Starter Home", "value": 150000},
            {"name": "Mid-size Family Home", "value": 250000},
            {"name": "Large Luxury Home", "value": 500000},
            {"name": "Urban Condo", "value": 200000},
        ]

        # Selected house
        self.selected_house = None

        # Payment method for down payment
        self.payment_method = None

        # State (0 = house selection, 1 = payment selection, 2 = confirmation)
        self.state = 0

        # Create house selection buttons
        self.create_house_buttons()

    def create_house_buttons(self):
        """Create buttons for house selection."""
        self.buttons = []

        if self.state == 0:
            # House selection buttons
            for i, house in enumerate(self.house_options):
                house_button = Button(
                    SCREEN_WIDTH // 2 - 150,
                    250 + i * 60,
                    300, 50,
                    f"{house['name']} - ${house['value']}",
                    action=lambda h=house: self.select_house(h)
                )
                self.buttons.append(house_button)

            # Skip button
            skip_button = Button(
                SCREEN_WIDTH // 2 - 100,
                SCREEN_HEIGHT - 90,
                200, 50,
                "Skip for Now",
                action=self.skip_purchase
            )
            self.buttons.append(skip_button)

        elif self.state == 1:
            # Payment method buttons for down payment
            payment_options = []

            down_payment = self.selected_house['value'] * 0.2

            if self.game.player.cash >= down_payment:
                payment_options.append("Cash")

            if self.game.player.bank_account and self.game.player.bank_account.balance >= down_payment:
                payment_options.append("Bank Account")

            if not payment_options:
                # Not enough money for down payment
                self.state = 3  # Special state for not enough money
                self.create_house_buttons()
                return

            for i, method in enumerate(payment_options):
                method_button = Button(
                    SCREEN_WIDTH // 2 - 100,
                    300 + i * 60,
                    200, 50,
                    method,
                    action=lambda m=method: self.select_payment_method(m)
                )
                self.buttons.append(method_button)

            # Back button
            back_button = Button(
                SCREEN_WIDTH // 2 - 100,
                SCREEN_HEIGHT - 90,
                200, 50,
                "Back",
                action=self.go_back_to_house_selection
            )
            self.buttons.append(back_button)

        elif self.state == 2:
            # Confirmation button
            confirm_button = Button(
                SCREEN_WIDTH // 2 - 100,
                SCREEN_HEIGHT - 90,
                200, 50,
                "Continue",
                action=self.confirm_purchase
            )
            self.buttons.append(confirm_button)

        elif self.state == 3:
            # Not enough money state
            back_button = Button(
                SCREEN_WIDTH // 2 - 100,
                SCREEN_HEIGHT - 90,
                200, 50,
                "Back",
                action=self.go_back_to_house_selection
            )
            self.buttons.append(back_button)

            skip_button = Button(
                SCREEN_WIDTH // 2 - 100,
                SCREEN_HEIGHT - 150,
                200, 50,
                "Skip for Now",
                action=self.skip_purchase
            )
            self.buttons.append(skip_button)

    def select_house(self, house):
        """Select a house to purchase."""
        self.selected_house = house
        self.state = 1
        self.create_house_buttons()

    def go_back_to_house_selection(self):
        """Go back to house selection."""
        self.state = 0
        self.create_house_buttons()

    def select_payment_method(self, method):
        """Select a payment method for down payment."""
        self.payment_method = method

        # Calculate down payment (20% is standard)
        down_payment = self.selected_house['value'] * 0.2
        loan_amount = self.selected_house['value'] - down_payment

        # Process down payment
        if method == "Cash":
            self.game.player.cash -= down_payment
        else:  # Bank Account
            self.game.player.bank_account.withdraw(down_payment)

        # Create mortgage
        if self.game.player.credit_score >= 750:
            interest_rate = 0.035  # 3.5%
        elif self.game.player.credit_score >= 700:
            interest_rate = 0.04   # 4.0%
        elif self.game.player.credit_score >= 650:
            interest_rate = 0.045  # 4.5%
        else:
            interest_rate = 0.055  # 5.5%

        loan = Loan("Mortgage", loan_amount, interest_rate, 30)  # 30-year mortgage
        self.game.player.loans.append(loan)

        # Add house to assets
        self.game.player.assets.append(Asset("House", self.selected_house['name'], self.selected_house['value']))

        # Move to confirmation
        self.state = 2
        self.create_house_buttons()

    def skip_purchase(self):
        """Skip house purchase."""
        from moneySmartz.screens.game_screen import GameScreen
        self.game.gui_manager.set_screen(GameScreen(self.game))

    def confirm_purchase(self):
        """Confirm purchase and return to game."""
        from moneySmartz.screens.game_screen import GameScreen
        self.game.gui_manager.set_screen(GameScreen(self.game))

    def draw(self, surface):
        """Draw the housing screen."""
        # Background
        surface.fill(WHITE)

        # Title
        title_surface = self.title_font.render("HOUSE PURCHASE OPPORTUNITY", True, BLUE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 80))
        surface.blit(title_surface, title_rect)

        if self.state == 0:
            # House selection state
            text_lines = [
                "You're now at a stage in life where buying a house could be a good investment.",
                "Would you like to look at some housing options?",
                "",
                "Select a house to purchase:"
            ]

            for i, line in enumerate(text_lines):
                text_surface = self.text_font.render(line, True, BLACK)
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 150 + i * 30))
                surface.blit(text_surface, text_rect)

        elif self.state == 1:
            # Payment method selection state
            down_payment = self.selected_house['value'] * 0.2

            text_lines = [
                f"You've selected the {self.selected_house['name']} for ${self.selected_house['value']}.",
                f"A standard mortgage requires a 20% down payment of ${down_payment:.2f}.",
                "",
                "How would you like to pay the down payment?"
            ]

            for i, line in enumerate(text_lines):
                text_surface = self.text_font.render(line, True, BLACK)
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 150 + i * 30))
                surface.blit(text_surface, text_rect)

        elif self.state == 2:
            # Confirmation state
            loan = self.game.player.loans[-1]  # The loan we just added
            down_payment = self.selected_house['value'] * 0.2

            text_lines = [
                f"Congratulations on your new {self.selected_house['name']}!",
                "",
                f"You paid the down payment of ${down_payment:.2f} using {self.payment_method}.",
                "",
                f"Your mortgage details:",
                f"Loan Amount: ${loan.original_amount:.2f}",
                f"Interest Rate: {loan.interest_rate*100:.1f}%",
                f"Monthly Payment: ${loan.monthly_payment:.2f}",
                f"Term: {loan.term_years} years"
            ]

            for i, line in enumerate(text_lines):
                text_surface = self.text_font.render(line, True, BLACK)
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 150 + i * 30))
                surface.blit(text_surface, text_rect)

            # Draw house image (simple house shape)
            house_rect = pygame.Rect(SCREEN_WIDTH // 2 - 75, 400, 150, 100)
            pygame.draw.rect(surface, LIGHT_BLUE, house_rect)

            # Draw roof
            pygame.draw.polygon(surface, RED, [
                (SCREEN_WIDTH // 2 - 85, 400),
                (SCREEN_WIDTH // 2 + 85, 400),
                (SCREEN_WIDTH // 2, 350)
            ])

            # Draw door
            door_rect = pygame.Rect(SCREEN_WIDTH // 2 - 15, 450, 30, 50)
            pygame.draw.rect(surface, BROWN, door_rect)

            # Draw window
            window_rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, 420, 25, 25)
            pygame.draw.rect(surface, WHITE, window_rect)
            pygame.draw.rect(surface, BLACK, window_rect, 2)  # Border

            window_rect2 = pygame.Rect(SCREEN_WIDTH // 2 + 25, 420, 25, 25)
            pygame.draw.rect(surface, WHITE, window_rect2)
            pygame.draw.rect(surface, BLACK, window_rect2, 2)  # Border

        elif self.state == 3:
            # Not enough money state
            down_payment = self.selected_house['value'] * 0.2

            text_lines = [
                f"You've selected the {self.selected_house['name']} for ${self.selected_house['value']}.",
                f"A standard mortgage requires a 20% down payment of ${down_payment:.2f}.",
                "",
                "You don't have enough money for the down payment.",
                "You'll need to save up more money before buying a house.",
                "",
                "Would you like to select a different house or skip for now?"
            ]

            for i, line in enumerate(text_lines):
                text_surface = self.text_font.render(line, True, BLACK)
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 150 + i * 30))
                surface.blit(text_surface, text_rect)

        # Draw buttons
        for button in self.buttons:
            button.draw(surface)

class FamilyPlanningScreen(Screen):
    """
    Screen for family planning opportunity.
    """
    def __init__(self, game):
        super().__init__(game)

        # Title
        self.title_font = pygame.font.SysFont('Arial', FONT_LARGE)
        self.text_font = pygame.font.SysFont('Arial', FONT_MEDIUM)

        # State (0 = initial, 1 = spouse added, 2 = children question, 3 = confirmation)
        self.state = 0

        # Spouse info
        self.spouse_age = self.game.player.age - random.randint(-3, 3)  # Spouse age is close to player age
        self.spouse_has_job = random.random() < 0.7  # 70% chance of spouse having a job

        if self.spouse_has_job:
            self.spouse_income = int(self.game.player.salary * random.uniform(0.5, 1.5))  # Spouse income relative to player
        else:
            self.spouse_income = 0

        # Children info
        self.num_children = random.randint(1, 3)  # Random number of children

        # Create buttons
        self.create_buttons()

    def create_buttons(self):
        """Create buttons based on current state."""
        self.buttons = []

        if self.state == 0:
            # Initial state - start family or skip
            start_button = Button(
                SCREEN_WIDTH // 2 - 100,
                SCREEN_HEIGHT - 150,
                200, 50,
                "Start a Family",
                action=self.start_family
            )

            skip_button = Button(
                SCREEN_WIDTH // 2 - 100,
                SCREEN_HEIGHT - 90,
                200, 50,
                "Not Now",
                action=self.skip_family
            )

            self.buttons = [start_button, skip_button]

        elif self.state == 1:
            # Spouse added - have children or not
            children_button = Button(
                SCREEN_WIDTH // 2 - 100,
                SCREEN_HEIGHT - 150,
                200, 50,
                "Have Children",
                action=self.have_children
            )

            no_children_button = Button(
                SCREEN_WIDTH // 2 - 100,
                SCREEN_HEIGHT - 90,
                200, 50,
                "No Children",
                action=self.no_children
            )

            self.buttons = [children_button, no_children_button]

        elif self.state == 2 or self.state == 3:
            # Confirmation
            continue_button = Button(
                SCREEN_WIDTH // 2 - 100,
                SCREEN_HEIGHT - 90,
                200, 50,
                "Continue",
                action=self.continue_to_game
            )

            self.buttons = [continue_button]

    def start_family(self):
        """Start a family by adding a spouse."""
        # Add spouse to family
        self.game.player.family.append({"relation": "Spouse", "age": self.spouse_age})

        # Add spouse income if applicable
        if self.spouse_has_job:
            self.game.player.salary += self.spouse_income

        # Move to next state
        self.state = 1
        self.create_buttons()

    def have_children(self):
        """Have children."""
        # Add children to family
        for i in range(self.num_children):
            child_name = f"Child {i+1}"  # Placeholder name
            child_age = 0  # Newborn
            self.game.player.family.append({"relation": "Child", "name": child_name, "age": child_age})

        # Move to confirmation state
        self.state = 2
        self.create_buttons()

    def no_children(self):
        """Choose not to have children."""
        # Move to confirmation state
        self.state = 3
        self.create_buttons()

    def skip_family(self):
        """Skip family planning for now."""
        from moneySmartz.screens.game_screen import GameScreen
        self.game.gui_manager.set_screen(GameScreen(self.game))

    def continue_to_game(self):
        """Continue to game after family planning."""
        from moneySmartz.screens.game_screen import GameScreen
        self.game.gui_manager.set_screen(GameScreen(self.game))

    def draw(self, surface):
        """Draw the family planning screen."""
        # Background
        surface.fill(WHITE)

        # Title
        title_surface = self.title_font.render("FAMILY PLANNING", True, BLUE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 80))
        surface.blit(title_surface, title_rect)

        if self.state == 0:
            # Initial state
            text_lines = [
                "You've reached a stage in life where starting a family might be a consideration.",
                "Starting a family will increase your monthly expenses but can bring joy to your life.",
                "",
                "Would you like to start a family?"
            ]

            for i, line in enumerate(text_lines):
                text_surface = self.text_font.render(line, True, BLACK)
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 150 + i * 30))
                surface.blit(text_surface, text_rect)

            # Draw family image (simple stick figures)
            self.draw_stick_figure(surface, SCREEN_WIDTH // 2 - 50, 300, 40, is_male=True)
            self.draw_stick_figure(surface, SCREEN_WIDTH // 2 + 50, 300, 40, is_male=False)

        elif self.state == 1:
            # Spouse added state
            text_lines = [
                "Congratulations! You've gotten married.",
                f"Your spouse is {self.spouse_age} years old."
            ]

            if self.spouse_has_job:
                text_lines.extend([
                    f"Your spouse has a job that adds ${self.spouse_income}/year to your family income.",
                    f"Your combined family income is now ${self.game.player.salary}/year."
                ])
            else:
                text_lines.append("Your spouse doesn't currently have a job.")

            text_lines.extend([
                "",
                "Would you like to have children?"
            ])

            for i, line in enumerate(text_lines):
                text_surface = self.text_font.render(line, True, BLACK)
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 150 + i * 30))
                surface.blit(text_surface, text_rect)

            # Draw family image (simple stick figures)
            self.draw_stick_figure(surface, SCREEN_WIDTH // 2 - 50, 300, 40, is_male=True)
            self.draw_stick_figure(surface, SCREEN_WIDTH // 2 + 50, 300, 40, is_male=False)

        elif self.state == 2:
            # Children added state
            text_lines = [
                f"Congratulations! You now have {self.num_children} {'child' if self.num_children == 1 else 'children'}.",
                "Having children will increase your monthly expenses.",
                "",
                "Your monthly expenses have increased to account for your growing family."
            ]

            for i, line in enumerate(text_lines):
                text_surface = self.text_font.render(line, True, BLACK)
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 150 + i * 30))
                surface.blit(text_surface, text_rect)

            # Draw family image (simple stick figures)
            self.draw_stick_figure(surface, SCREEN_WIDTH // 2 - 100, 300, 40, is_male=True)
            self.draw_stick_figure(surface, SCREEN_WIDTH // 2 + 100, 300, 40, is_male=False)

            # Draw children
            child_positions = self.distribute_children(self.num_children, SCREEN_WIDTH // 2, 350, 150)
            for pos in child_positions:
                self.draw_stick_figure(surface, pos[0], pos[1], 25, is_child=True)

        elif self.state == 3:
            # No children state
            text_lines = [
                "You've decided not to have children at this time.",
                "You can always reconsider this decision in the future."
            ]

            for i, line in enumerate(text_lines):
                text_surface = self.text_font.render(line, True, BLACK)
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 150 + i * 30))
                surface.blit(text_surface, text_rect)

            # Draw family image (simple stick figures)
            self.draw_stick_figure(surface, SCREEN_WIDTH // 2 - 50, 300, 40, is_male=True)
            self.draw_stick_figure(surface, SCREEN_WIDTH // 2 + 50, 300, 40, is_male=False)

        # Draw buttons
        for button in self.buttons:
            button.draw(surface)

    def draw_stick_figure(self, surface, x, y, size, is_male=True, is_child=False):
        """Draw a simple stick figure."""
        # Head
        head_radius = size // 4
        pygame.draw.circle(surface, BLACK, (x, y - size // 2 + head_radius), head_radius, 2)

        # Body
        body_length = size // 2
        pygame.draw.line(surface, BLACK, (x, y - size // 2 + head_radius * 2), (x, y - size // 2 + head_radius * 2 + body_length), 2)

        # Arms
        arm_length = size // 3
        pygame.draw.line(surface, BLACK, (x, y - size // 2 + head_radius * 2 + body_length // 3), 
                         (x - arm_length, y - size // 2 + head_radius * 2 + body_length // 3), 2)
        pygame.draw.line(surface, BLACK, (x, y - size // 2 + head_radius * 2 + body_length // 3), 
                         (x + arm_length, y - size // 2 + head_radius * 2 + body_length // 3), 2)

        # Legs
        leg_length = size // 2
        pygame.draw.line(surface, BLACK, (x, y - size // 2 + head_radius * 2 + body_length), 
                         (x - arm_length // 2, y - size // 2 + head_radius * 2 + body_length + leg_length), 2)
        pygame.draw.line(surface, BLACK, (x, y - size // 2 + head_radius * 2 + body_length), 
                         (x + arm_length // 2, y - size // 2 + head_radius * 2 + body_length + leg_length), 2)

        # Gender/age specific details
        if is_child:
            # Smaller figure already handled by size parameter
            pass
        elif is_male:
            # Bow tie for male
            pygame.draw.circle(surface, RED, (x, y - size // 2 + head_radius * 2 + body_length // 6), 3)
        else:
            # Skirt for female
            pygame.draw.polygon(surface, PURPLE, [
                (x, y - size // 2 + head_radius * 2 + body_length),
                (x - arm_length, y - size // 2 + head_radius * 2 + body_length + leg_length // 2),
                (x + arm_length, y - size // 2 + head_radius * 2 + body_length + leg_length // 2)
            ], 2)

    def distribute_children(self, num_children, center_x, y, width):
        """Calculate positions for children stick figures."""
        positions = []

        if num_children == 1:
            positions.append((center_x, y))
        else:
            spacing = width / (num_children - 1) if num_children > 1 else 0
            for i in range(num_children):
                x = center_x - width // 2 + i * spacing
                positions.append((x, y))

        return positions

