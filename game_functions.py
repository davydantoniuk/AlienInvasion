import sys
import pygame
from bullet import Bullet
from Alien import Alien
from time import sleep


def chek_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fir_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def fir_bullet(ai_settings, screen, ship, bullets):
    """Create a new bullet and include it in the bullets group."""
    if len(bullets) < ai_settings.bullet_allow:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def chek_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def chek_events(ai_settings, screen, stats, sd, play_buttom, ship, aliens, bullets):
    """actions of users"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            chek_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            chek_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_buttom(ai_settings, screen, stats, sd,
                              play_buttom, ship, aliens, bullets, mouse_x, mouse_y)


def check_play_buttom(ai_settings, screen, stats, sd, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Starts a new game when the Play button is pressed."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True
        sd.prep_score()
        sd.prep_high_score()
        sd.prep_level()
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def _change_fleet_direction(self):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in self.aliens.sprites():
        alien.rect.y += self.settings.fleet_drop_speed
    self.settings.fleet_direction *= -1


def update_screen(ai_settings, screen, stats, sd, ship, aliens, bullets, play_buttom):
    """reload screen and return new picture"""
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    sd.show_score()
    if not stats.game_active:
        play_buttom.draw_button()
    pygame.display.flip()


def uptade_bullets(ai_settings, screen, stats, sd, ship, aliens, bullets):
    """Updates bullet positions and destroys old bullets."""
    bullets.update()
    """Removing bullets that have gone beyond the edge of the screen."""
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
        check_bullet_alien_collisions(
            ai_settings, screen, stats, sd, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sd, ship, aliens, bullets):
    """Handling bullet collisions with aliens."""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sd.prep_score()
            chek_high_score(stats, sd)
    if not aliens:
        # Destroy existing bullets and create new fleet.
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sd.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)


def get_number_aliens_x(ai_settings, alien_width):
    """Calculates the number of aliens in a row."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x // (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determines the number of rows that fit on the screen."""
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y // (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Creates an alien and places it in the row."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Creates an alien fleet."""
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(
        ai_settings, ship.rect.height, alien.rect.height)
    """The creation of the first row of aliens"""
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            """Creating an alien and placing it in a row."""
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """Reacts when an alien reaches the edge of the screen."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Drops the entire fleet and changes the direction of the fleet."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """Handles a ship-to-ship collision with an alien."""
    if stats.ships_left > 0:
        stats.ships_left -= 1
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """Checks to see if the aliens have made it to the bottom edge of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # What happens is the same thing that happens when you collide with a ship.
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    """
    Checks to see if the fleet has reached the edge of the screen,
    then updates the positions of all aliens in the fleet.
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)


def chek_high_score(stats, sd):
    """Checking to see if there's a new record."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sd.prep_high_score()
