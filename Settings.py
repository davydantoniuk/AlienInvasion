class Settings():
    def __init__(self):
        self.screen_width = 1500
        self.screen_height = 780
        self.bg_color = (255, 255, 255)
        # ship settings
        self.ship_limit = 3
        # bullet settings
        self.bullet_width = 10
        self.bullet_height = 10
        self.bullet_color = 60, 60, 60
        self.bullet_allow = 3
        # alien settings
        self.fleet_drop_speed = 10
        # Pace of play acceleration
        self.speedup_scale = 1.4
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initializes settings that change over the course of the game."""
        self.ship_speed = 1.0
        self.bullet_speed = 3
        self.alien_speed_factor = 0.5
        # fleet_direction = 1 indicates movement to the right; and -1 indicates movement to the left.
        self.fleet_direction = 1
        self.alien_points = 50

    def increase_speed(self):
        """Increases the speed settings."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
