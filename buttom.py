import pygame.font


class Buttom():
    def __init__(self, ai_settings, screen, msg):
        """Initializes the attributes of the button."""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Assigning button sizes and properties
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        # Build the rect button object and align it to the center of the screen.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        # The button message is created only once.
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """Converts msg to a rectangle and centers the text."""
        self.msg_image = self.font.render(
            msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Display an empty button and output a message.
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
