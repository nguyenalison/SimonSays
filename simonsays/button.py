import pygame
pygame.init()


# Classes are like blueprints for objects, it defines its properties and behaviors
class Button(pygame.sprite.Sprite):
    # Constructor
    def __init__(self, color_on, color_off, sound, x, y):  # Add given properties as parameters
        pygame.sprite.Sprite.__init__(self)
        # Initialize properties here
        self.color_on = color_on
        self.color_off = color_off
        self.sound = sound
        self.image = pygame.Surface((230, 230))
        self.image.fill(self.color_off)
        self.rect = self.image.get_rect()
        # Assign x, y coordinates to the top left of the sprite
        self.rect.topleft = (x, y)
        self.clicked = False

    # 1. Display on the game window
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    # 2. Check if the button has been interacted with
    def selected(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True
        return False


    # 3. Handles what happen when it is interacted with
    def update(self, screen):
        # Fill the button with its on-color
        self.image.fill(self.color_on)
        # Blit the button image to the screen
        screen.blit(self.image, (self.rect.x, self.rect.y))
        # Play the button's associated sound
        self.sound.play()
        # Update the display to show the illuminated button
        pygame.display.update()
        # Wait for 500 milliseconds
        pygame.time.wait(500)
        # Fill the button with its off-color
        self.image.fill(self.color_off)
        # Blit the button image to the screen again
        screen.blit(self.image, (self.rect.x, self.rect.y))
        # Update the display to show the button in its off state
        pygame.display.update()
