import pygame


class Ship():
    def __init__(self, ai_settings, screen):
        """Load image"""
        self.screen = screen
        self.ai_settings = ai_settings
        self.image = pygame.image.load('images/ship.jpg')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        """Every ship appear in down of the screen"""
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.speed = 0.5
        self.center = float(self.rect.centerx)
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def uptade(self):
        """Updates the ship's position to reflect the flag."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed
        elif self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed
        self.rect.centerx = self.center

    def center_ship(self):
        """Places the ship in the center of the underside."""
        self.center = self.screen_rect.centerx

    def blitme(self):
        """Drowing ship"""
        self.screen.blit(self.image, self.rect)
