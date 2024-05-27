from pygame.sprite import Sprite
import pygame


class Bullet(Sprite):
    def __init__(self, ai_settings, screen, ship):
        """creating bullet in that position"""
        super(Bullet, self).__init__()
        self.screen = screen
        """Creating a bullet at position (0,0) and assigning the correct position."""
        self.rect = pygame.Rect(
            0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        """The position of the bullet is stored in real format."""
        self.y = float(self.rect.y)
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed

    def update(self):
        """Moves the bullet up the screen."""
        self.y -= self.speed_factor
        """Updates the position of the rectangle."""
        self.rect.y = self.y

    def draw_bullet(self):
        """Displaying the bullet on the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
