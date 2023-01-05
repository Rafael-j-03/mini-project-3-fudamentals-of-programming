import pygame
import random
from Player import *
from Enemies import *
from Bullet import *

# Setting the window
pygame.init()
screen = pygame.display.set_mode((1000, 380))

# Caption
pygame.display.set_caption("Heavy Ordnance")

# Load the lives image
heart_image = pygame.image.load('images/heart.png')

# Window stuff
screen_center_x = screen.get_width()/2
screen_center_y = screen.get_height()/2
screen_width = screen.get_width()
screen_height = screen.get_height()

# Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
ORANGE = (255,165,0)
SKY_BLUE = (0,181,226)
GREEN = (75,139,59)
ORANGE = (249,146,69)
OCEAN_BLUE = (0,94,184)
RED = (255,0,0)

# Setting clock
clock = pygame.time.Clock()

# Calling essential stuff
player = Player()
enemy_zone = Enemy_Zone()
danger_zone = Danger_Zone()
bullets = []
boats = []
boats_crashed = []
reference_enemy = Enemies(3)

# Start Screen
def startScreen():
    # Create font objects
    font = pygame.font.Font(None, 50)
    title_font = pygame.font.Font(None, 100)
    
    # Create text labels for the tile, the start button and the exit button
    title_text = title_font.render("HEAVY ORDNANCE", True, WHITE)
    title_rect = title_text.get_rect()
    title_rect.center = (screen_center_x, screen_center_y - 130)
    start_text = font.render("START", True, WHITE)
    start_rect = start_text.get_rect()
    start_rect.center = (screen_center_x, screen_center_y)
    exit_text = font.render("EXIT", True, WHITE)
    exit_rect = exit_text.get_rect()
    exit_rect.center = (screen_center_x, screen_center_y + 50)
    
    #Setting the loop to the start screen
    selected_button = "start"  # Start with the start button selected
    while True:
        # Draw the start and exit buttons on the screen
        screen.fill(SKY_BLUE)
        screen.blit(title_text, title_rect)
        if selected_button == "start":
            screen.blit(font.render("START", True, ORANGE), start_rect)
            screen.blit(exit_text, exit_rect)
        else:
            screen.blit(start_text, start_rect)
            screen.blit(font.render("EXIT", True, ORANGE), exit_rect)

        # Wait for a keyboard event
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            # Highligh the selected button
            if event.key == pygame.K_UP:
                # Highlight the start button
                selected_button = "start"
            elif event.key == pygame.K_DOWN:
                # Highlight the exit button
                selected_button = "exit"
            
            # Pressed a button
            if selected_button == "start":
                # If start is pressed
                if event.key == pygame.K_RETURN:
                    break
            elif selected_button == "exit":
                # If Exit is pressed
                if event.key == pygame.K_RETURN:
                    pygame.quit()
                    exit()
        
        pygame.display.flip()
        
# Game Screen
def game_Screen():
    new_speed = 0 # Variable to update the speed
    key_press_time = 0 # Set up a variable to store the time when the key is first pressed
    MIN_TIME_BETWEEN_ACTIONS = 1 # Set the minimum time between actions in seconds
    last_action_time = 0 # Set the time of the last action to 0
    enemy_spawn_timer = 0 # Calling a timer to spawn enemies
    score_font = pygame.font.Font(None, 30) # Setting the score font
    alive = True # Check if player is alive
    
    while alive:
        player.increase_score() # Increase the player score + 1 after 1 second
        score_text = score_font.render("Score: " + str(player.score), 1, WHITE) # Updating the score
        clock.tick(60) # Set FPS
      
        # Check for events (inputs)
        for event in pygame.event.get():
            # If the player wants to close the game
            if event.type == pygame.QUIT:
                # Quit the game and close the window
                pygame.quit() 
                exit()
            # If the player presses the mouse button
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Get the current time
                key_press_time = pygame.time.get_ticks()
            # If the player releases the mouse button
            elif event.type == pygame.MOUSEBUTTONUP:
                current_time = pygame.time.get_ticks() # Get the current time
                elapsed_time = (current_time - key_press_time) / 1000 / 2.5 # Calculate the elapsed time between the press and release of the mouse button
                action_elapsed_time = (current_time - last_action_time) / 1000 # Calculate the elapsed time since the last action
                # If the elapsed time since the last action is greater than or equal to the minimum time between actions
                if action_elapsed_time >= MIN_TIME_BETWEEN_ACTIONS:
                    last_action_time = current_time # Store the current time as the time of the last action
                    # Check if theres less than 2 bullets on the field
                    if len(bullets) < 2:
                        if elapsed_time != 0:
                            if elapsed_time < 0.7:
                                bullets.append(Bullet(player, elapsed_time))
                            if elapsed_time >= 0.7:
                                elapsed_time = 0.7
                                bullets.append(Bullet(player, elapsed_time))
                    else:
                        pass
                    
        # Update the enemy boats
        for enemy in boats:
            enemy.update()
            # Check for collision between bullets and enemies boat's
            for b in bullets:
                if enemy.collider.colliderect(b.collider):
                    # Handle collision
                    boats_crashed.append(boats.index(enemy)) # Set a new crashed boat
                    boats.pop(boats.index(enemy))
                    bullets.pop(bullets.index(b))
                    player.score += enemy.score * enemy.speed #Increases the player score by the difficulty
                    # Each time the player crash 10 enemy boats the difficulty is increased
                    if len(boats_crashed) % 10 == 0:
                        enemy.speed += 1
                        new_speed = enemy.speed
                        reference_enemy.speed = new_speed  
            # Boat collision with the danger zone
            if enemy.collider.colliderect(danger_zone.collider):
                boats.pop(boats.index(enemy))
                player.lives -= 1
                    
        # Bullets Update
        for b in bullets:
            b.update()
            # Check if the bullet is out of bounds
            if b.active == False:
                bullets.pop(bullets.index(b))
            # Check if the bullet collides with the enemy zone
            if b.collider.colliderect(enemy_zone.collider):
                bullets.pop(bullets.index(b))
                
        # Player Update
        player.update()
        
        # Spawn new enemy if timer is up and there are less than 4 enemies on the screen
        current_time = pygame.time.get_ticks() # Sets a timer
        new_boat = Enemies(random.randint(1,5)) # Random ranked boat
        new_boat.speed = new_speed # Update speed
        if new_speed != 0: # Update spawn delay for a higher difficulty
            new_boat.spawn_delay /= new_speed
        if current_time - enemy_spawn_timer > new_boat.spawn_delay and len(boats) < 4:
            if new_speed == 0:
                new_boat.speed = 1
                boats.append(new_boat)
            else:
                boats.append(new_boat)
                print(new_boat.spawn_delay)
            enemy_spawn_timer = current_time
            
        # Check if player have more lifes
        if player.lives == 0:
            alive = False
            
        # Clear the screen
        screen.fill(SKY_BLUE)
        
        # Draw the enemy boats
        for enemy in boats:
            enemy.draw(screen, RED)
            
        # Player's area
        player.draw_area(screen, GREEN)
        
        # Danger zone
        danger_zone.draw_zone(screen, ORANGE)
        
        # Enemy Zone
        enemy_zone.draw_zone(screen, OCEAN_BLUE)
        
        # Player Draw
        player.draw(screen, BLACK)
        
        # Bullet Draw
        for b in bullets:
            b.draw(screen, BLACK)
            
        # Shows the score
        screen.blit(score_text, (screen_width - score_text.get_width() - 25, 10))
        
        # Draw lives
        player.draw_lifes(screen, heart_image)
                
        # Update the screen
        pygame.display.flip()
        
#Game Over Screen
def gameOverScreen():
    # Set the background color to black
    screen.fill(SKY_BLUE)
    # Display the game over message
    font = pygame.font.Font(None, 170)
    text = font.render("GAME OVER", True, WHITE)
    text_rect = text.get_rect()
    text_rect.centerx = screen_center_x
    text_rect.centery = screen_center_y
    screen.blit(text, text_rect)
    # Update the display
    pygame.display.update()
    # Wait for 2 seconds
    pygame.time.delay(2000)
        
# Main game loop
while True:
    # Start Screen
    startScreen()
    # Game Screen
    game_Screen()
    # Game Over Screen
    gameOverScreen()
    # Reset
    player.reset()
    reference_enemy.reset()
    boats = []
    bullets = []