import pygame
import os
from pygame.locals import *
from moneySmarts.constants import *
from moneySmarts.sound_manager import SoundManager
from moneySmarts.event_manager import EventBus

class Button:
    """
    A button UI element that can be clicked to trigger an action.
    """
    def __init__(self, x, y, width, height, text, color=BLUE, hover_color=LIGHT_BLUE, 
                 text_color=WHITE, font_size=FONT_MEDIUM, font_name=None, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        # Use custom font if available
        try:
            if font_name:
                self.font = pygame.font.Font(font_name, font_size)
            else:
                self.font = pygame.font.SysFont('Arial', font_size)
        except:
            self.font = pygame.font.SysFont('Arial', font_size)
        self.action = action
        self.hovered = False

    def draw(self, surface):
        """Draw the button on the given surface."""
        color = self.hover_color if self.hovered else self.color
        # Validate color is a tuple of 3 integers (RGB)
        if not (isinstance(color, tuple) and len(color) in (3, 4) and all(isinstance(c, int) and 0 <= c <= 255 for c in color)):
            color = (0, 120, 255)  # Default to BLUE
        pygame.draw.rect(surface, color, self.rect)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def update(self, mouse_pos, mouse_click):
        """
        Update the button state based on mouse position and click.
        Returns the action if the button is clicked, None otherwise.
        """
        self.hovered = self.rect.collidepoint(mouse_pos)
        if self.hovered:
            print(f"[DEBUG] Button '{self.text}' is hovered at {mouse_pos}.")
        if self.hovered and mouse_click:
            print(f"[DEBUG] Button '{self.text}' mouse_click detected at {mouse_pos}.")
            if self.action:
                print(f"[DEBUG] Button '{self.text}' returning action: {self.action}")
                return self.action
        return None

class TextInput:
    def __init__(self, x, y, width, height, font_size=FONT_MEDIUM, max_length=20, 
                 initial_text="", font_name=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = initial_text
        # Use custom font if available
        try:
            if font_name:
                self.font = pygame.font.Font(font_name, font_size)
            else:
                self.font = pygame.font.SysFont('Arial', font_size)
        except:
            self.font = pygame.font.SysFont('Arial', font_size)
        self.active = False
        self.max_length = max_length

    def draw(self, surface):
        """Draw the text input field on the given surface."""
        color = LIGHT_BLUE if self.active else WHITE
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)  # Border

        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(midleft=(self.rect.left + 10, self.rect.centery))
        surface.blit(text_surface, text_rect)

    def update(self, events):
        """
        Update the text input field based on user input.
        Returns the current text.
        """
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                self.active = self.rect.collidepoint(event.pos)

            if event.type == KEYDOWN and self.active:
                if event.key == K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == K_RETURN:
                    self.active = False
                elif len(self.text) < self.max_length:
                    self.text += event.unicode

        return self.text

class Screen:
    """
    Base class for all screens in the game.
    """
        
    play_startup_music = False  # Class attribute to control music

    def __init__(self, game):
        self.game = game
        self.buttons = []
        self.next_screen = None

        # Subscribe to random events for UI notification
        EventBus.subscribe("random_event", self.on_random_event)
        
    def on_random_event(self, event, effect, player):
        """Handle random events published by the event system (override in subclasses for custom UI)."""
        # Example: print/log or update UI elements
        pass

    def handle_events(self, events):
        """Handle pygame events for this screen."""
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False

        for event in events:
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                mouse_click = True

        for button in self.buttons:
            action = button.update(mouse_pos, mouse_click)
            if action:
                action()
                return

    def update(self):
        """Update the screen state."""
        pass

    def draw(self, surface):
        """Draw the screen on the given surface."""
        surface.fill(WHITE)
        for button in self.buttons:
            button.draw(surface)

class GUIManager:
    """
    Manages the GUI and screen transitions.
    """
    def __init__(self, game):
        self.game = game
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Money Smartz: Financial Life Simulator")
        self.clock = pygame.time.Clock()
        self.current_screen = None
        self.running = True
        
        # Initialize sound manager
        self.sound_manager = SoundManager()
        
        # Load sounds
        self.load_sounds()

    def load_sounds(self):
        """Load all sound assets"""
        # Get assets path relative to project root
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(current_dir)  # Go up to moneySmarts directory
        assets_dir = os.path.join(root_dir, 'assets')
        
        # Load startup song
        startup_song_path = os.path.join(assets_dir, 'startup_song.mp3')
        if os.path.exists(startup_song_path):
            self.sound_manager.load_music(startup_song_path, 'startup_song')
        else:
            print(f"Warning: Sound file not found at {startup_song_path}")

    def set_screen(self, screen):
        """Set the current screen to be displayed."""
        self.current_screen = screen
        print(f"[DEBUG] set_screen called: switched to {type(screen).__name__}")
        # Call on_enter if present
        if hasattr(screen, 'on_enter') and callable(screen.on_enter):
            screen.on_enter()
        # Handle music based on screen's play_startup_music attribute
        if getattr(screen, 'play_startup_music', False):
            self.sound_manager.play_music('startup_song')
        else:
            self.sound_manager.stop_music()
            
    def run(self):
        """Run the main game loop."""
        while self.running and not self.game.game_over:
            events = pygame.event.get()
            for event in events:
                if event.type == QUIT:
                    self.running = False
                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    # Store screen dimensions locally instead of modifying global constants
                    self.screen_width = event.w
                    self.screen_height = event.h
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                        # If the current screen has a back_btn, trigger its action
                        if hasattr(self.current_screen, 'back_btn') and self.current_screen.back_btn and hasattr(self.current_screen.back_btn, 'action'):
                            self.current_screen.back_btn.action()
            if self.current_screen:
                self.current_screen.handle_events(events)
                self.current_screen.update()
                self.current_screen.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()
