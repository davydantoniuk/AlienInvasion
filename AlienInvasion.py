import pygame
from Settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from buttom import Buttom
from scorbored import Scoreboard


def run_game():
    """Running the grill"""
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Alien Invasion')
    play_button = Buttom(ai_settings, screen, "Play")
    ship = Ship(ai_settings, screen)
    aliens = Group()
    """Creating a group to store bullets."""
    bullets = Group()
    """Starting the main cycle"""
    gf.create_fleet(ai_settings, screen, ship, aliens)
    stats = GameStats(ai_settings)
    sd = Scoreboard(ai_settings, screen, stats)
    while True:
        gf.chek_events(ai_settings, screen, stats, sd,
                       play_button, ship, aliens, bullets)
        if stats.game_active:
            ship.uptade()
            gf.uptade_bullets(ai_settings, screen, stats,
                              sd,  ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)
        gf.update_screen(ai_settings, screen, stats, sd,
                         ship, aliens, bullets, play_button)


run_game()
