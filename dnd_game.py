import pygame
import sys
import random
# --- FIX 1: ADD MISSING IMPORTS ---
# NOTE: Ensure you have 'character_classes.py' and 'battle_mechanics.py' files 
# in the same directory, or this will fail.
import character_classes 
import battle_mechanics 
# -----------------------------------

# Define Colors
WHITE = (255, 255, 255)
DARK_BLUE = (25, 25, 112)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# 1. Initialization
pygame.init()

# 2. Setup the Screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My Pygame D&D Game")

# Define the desired size for both characters
PLAYER_SIZE = (50, 50) 
MONSTER_SIZE = (50, 50) 

# **IMAGE LOADING AND RECT CREATION**
try:
    # NOTE: Ensure 'player.png', 'goblin.png', and 'platform.webp' exist
    original_player_image = pygame.image.load('player.png').convert_alpha()
    original_monster_image = pygame.image.load('goblin.png').convert_alpha()
    
    player_image = pygame.transform.scale(original_player_image, PLAYER_SIZE)
    monster_image = pygame.transform.scale(original_monster_image, MONSTER_SIZE)

    # Load the background and scale it to fit the screen
    background_image_orig = pygame.image.load('platform.webp').convert() 
    background_image = pygame.transform.scale(background_image_orig, (SCREEN_WIDTH, SCREEN_HEIGHT))

except pygame.error as e:
    print(f"Error loading images: {e}")
    # Display a message and exit if critical assets are missing
    font = pygame.font.Font(None, 40)
    screen.fill(DARK_BLUE)
    error_text = font.render(f"Error loading images: {e}", True, WHITE)
    screen.blit(error_text, (50, 250))
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

# **CREATE RECT OBJECTS**
player_rect = player_image.get_rect()
monster_rect = monster_image.get_rect()

# Set the initial position of the Rects (World Coordinates)
# FIX: Start player 1 pixel above the ground (500) to ensure collision on startup
player_rect.bottomleft = (50, 499) 

# Monster positioning far to the right for initial scrolling test
monster_rect.bottomright = (1200, 450) 

# Setup Font
font = pygame.font.Font(None, 40) 

# Define Menu Colors and Actions
BUTTON_COLOR = (100, 100, 150)
HOVER_COLOR = (150, 150, 200)
ACTION_BUTTONS = ["Attack", "Item", "Confuse", "Flee"]
BUTTON_WIDTH = 120
BUTTON_HEIGHT = 40

# --- State Variables ---
current_action = None 
message_timer = 0 

# Camera Variable
camera_offset_x = 0
SCROLL_BOUNDARY = 200 # New constant for camera boundary

# --- 3. Game Loop Variables ---
running = True
clock = pygame.time.Clock() 

# Platformer Physics Variables
player_x_vel = 0
player_y_vel = 0
GRAVITY = .3 
JUMP_STRENGTH = -10
MAX_SPEED = 5
is_jumping = False 

# Initial Game State
game_state = "PLATFORMING" 
game_message = "Run and Jump! (A/D/Space)"
is_in_battle = False 

# Define Platform Rects: (x, y, width, height) - World Coordinates
ground_rect = pygame.Rect(0, 500, SCREEN_WIDTH * 2, 100) # Made ground twice as long
platform1_rect = pygame.Rect(300, 350, 200, 20) 
platform2_rect = pygame.Rect(600, 250, 250, 20) 
platform3_rect = pygame.Rect(900, 150, 200, 20) 

platforms = [ground_rect, platform1_rect, platform2_rect, platform3_rect]

PLATFORM_TEXTURE_RECT = pygame.Rect(307, 560, 329, 25) # Example crop from your background image

# Define platform ranges
MIN_PLATFORM_GAP = 150 # Minimum horizontal gap between platforms
MAX_PLATFORM_GAP = 350 # Maximum horizontal gap
MAX_PLATFORM_Y_CHANGE = 75 # Max difference in height between platforms
PLATFORM_WIDTH_RANGE = (100, 250) # Min and Max width for new platforms
PLATFORM_HEIGHT = 20 # Standard height for simplicity


def generate_platform(last_rect, screen_height):
    """Generates a new platform rectangle based on the last one."""
    
    # 1. Calculate New X Position
    # Start the new platform after the last one, plus a random gap
    new_x = last_rect.right + random.randint(MIN_PLATFORM_GAP, MAX_PLATFORM_GAP)
    
    # 2. Calculate New Y Position
    # Calculate a random vertical offset from the last platform's Y position
    min_y = max(100, last_rect.y - MAX_PLATFORM_Y_CHANGE)
    max_y = min(screen_height - 100, last_rect.y + MAX_PLATFORM_Y_CHANGE)
    new_y = random.randint(min_y, max_y)
    
    # 3. Calculate New Width
    new_width = random.randint(*PLATFORM_WIDTH_RANGE)
    
    # 4. Create the new Rect
    new_platform = pygame.Rect(new_x, new_y, new_width, PLATFORM_HEIGHT)
    
    return new_platform


# **D&D Combat Variables**
ATTACK_RANGE = 75
player_attack_cooldown = 0
ATTACK_COOLDOWN_TIME = 30
ENEMY_DIFFICULTY = 15 

player = character_classes.Acrobat(name='Nathan', age=33, sex='male', height=180)
monster = character_classes.Orc(name='Bork')

def draw_combat_menu(screen, font, mouse_pos):
    """Draws the combat action buttons."""
    buttons = {}
    x_start = 50
    y_start = SCREEN_HEIGHT - 120 
    
    for i, action in enumerate(ACTION_BUTTONS):
        x = x_start + (BUTTON_WIDTH + 20) * i
        y = y_start
        rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
        buttons[action] = rect
        
        color = HOVER_COLOR if rect.collidepoint(mouse_pos) else BUTTON_COLOR
        
        pygame.draw.rect(screen, color, rect)
        
        text_surf = font.render(action, True, WHITE)
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)
        
    return buttons 

# 4. Main Game Loop
while running:
    # 1. Handle Cooldown 
    if player_attack_cooldown > 0:
        player_attack_cooldown -= 1

    # --- NEW: INPUT & STATE LOGIC SETUP ---
    mouse_pos = pygame.mouse.get_pos()
    clicked_button = None
    button_rects = {} 

    # --- 1. EVENT HANDLING (Processes one-time events) ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # MOUSE CLICK CHECK
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if game_state == "PLAYER_TURN_MENU":
                for action, rect in button_rects.items():
                    if rect.collidepoint(mouse_pos):
                        clicked_button = action
                        break
        
        # JUMP CHECK (Using K_SPACE)
        if game_state == "PLATFORMING":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not is_jumping:
                    player_y_vel = JUMP_STRENGTH
                    is_jumping = True

    # --- 2. TURN ACTION PROCESSING ---
    
    # Process the clicked button
    if clicked_button and is_in_battle and player_attack_cooldown == 0:
        game_state = "PROCESSING_ACTION" 
        
        # Attack logic
        if clicked_button == "Attack":
            in_range = player_rect.colliderect(monster_rect) 
            
            if in_range:
                d20_roll = battle_mechanics.dice_roll(20, 1)[0]
                
                # NOTE: These functions must exist in battle_mechanics.py
                hit, damage_dealt, outcome_message = battle_mechanics.resolve_attack_attempt(
                    player, monster, d20_roll, ENEMY_DIFFICULTY)
                
                game_message = outcome_message
                game_state = "MONSTER_TURN_INIT" 
                player_attack_cooldown = ATTACK_COOLDOWN_TIME
            else:
                game_message = "Error: You are too far to attack!"
                game_state = "PLAYER_TURN_MENU" 
        
        # Flee logic placeholder
        elif clicked_button == "Flee":
            game_message = "Fleeing..."
            game_state = "PLATFORMING"
            is_in_battle = False
            # You may want to push the player away from the monster here

    # Monster Turn Execution 
    if game_state == "MONSTER_TURN_INIT":
        message_timer = 30 
        game_state = "MONSTER_TURN_WAIT"
        
    if game_state == "MONSTER_TURN_WAIT":
        message_timer -= 1
        if message_timer <= 0:
            # NOTE: Monster turn logic placeholder
            # game_message = battle_mechanics.handle_enemy_turn(monster, player)
            game_message = f"{monster.name} stares menacingly."
            game_state = "PLAYER_TURN_MENU" 

    # --- Game Logic: Platformer Physics ---

    if game_state == "PLATFORMING":
        
        # 1. Horizontal Input (A and D keys)
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_d]: # 'D' key for Right
            player_x_vel = MAX_SPEED
        elif keys[pygame.K_a]: # 'A' key for Left
            player_x_vel = -MAX_SPEED
        else:
            player_x_vel = 0

        # 2. Apply Gravity (Velocity increases every frame)
        player_y_vel += GRAVITY
        
        if player_y_vel > 10: 
            player_y_vel = 10
        
        # 3. Apply Velocity to Position (World Coordinates)
        player_rect.x += player_x_vel
        player_rect.y += player_y_vel

        # --- Horizontal Camera Scrolling Logic ---

        # Scroll Right
        if player_rect.right - camera_offset_x > SCREEN_WIDTH - SCROLL_BOUNDARY:
            camera_offset_x += (player_rect.right - camera_offset_x) - (SCREEN_WIDTH - SCROLL_BOUNDARY)

        # Scroll Left
        if player_rect.left - camera_offset_x < SCROLL_BOUNDARY:
            camera_offset_x += (player_rect.left - camera_offset_x) - SCROLL_BOUNDARY
            
        # Optional: Limit camera scrolling to the left edge of the world (0)
        if camera_offset_x < 0:
            player_rect.x -= camera_offset_x # push player back to the edge
            camera_offset_x = 0

        # --- NEW: Platform Generation Logic ---
        # Get the last platform added to the world
        last_platform = platforms[-1] 

        # Condition for Generation: If the last platform's right edge, 
        # adjusted by the camera offset, is less than 1.5 screen widths away.
        # This ensures a new platform is ready well before the player sees the end of the world.
        if (last_platform.right - camera_offset_x) < (SCREEN_WIDTH * 1.5):
            
            # Generate the new platform
            new_platform = generate_platform(last_platform, SCREEN_HEIGHT)
            
            # Add it to the list
            platforms.append(new_platform)
            
            # Optional: Prune old platforms (remove platforms the player has passed)
            # This prevents the platforms list from growing infinitely large, saving memory.
            if len(platforms) > 10: # Keep a maximum of 10 platforms visible/ahead of player
                # Remove the oldest platform (which is the first one in the list)
                platforms.pop(0) 

        # --- END Platform Generation Logic ---
        
        # 4. Collision Detection and Resolution
        for platform in platforms:
            if player_rect.colliderect(platform):
                if player_y_vel > 0: # Falling (Hitting top of platform)
                    player_rect.bottom = platform.top
                    player_y_vel = 0
                    is_jumping = False
                
                elif player_y_vel < 0: # Rising (Hitting bottom of platform)
                    player_rect.top = platform.bottom
                    player_y_vel = 0

        # 5. Boundary Check (Keep player from scrolling infinitely left past X=0)
        # Note: Horizontal screen limits were removed for scrolling
        if player_rect.left < 0:
            player_rect.left = 0
        # NOTE: You may want to add a MAX_WORLD_WIDTH limit here later.

        # 6. Combat Initiation Check
        if player_rect.colliderect(monster_rect):
            game_state = "PLAYER_TURN_MENU"
            is_in_battle = True
            game_message = "Battle! Choose your action."
            
            # FREEZE MOVEMENT
            player_x_vel = 0
            player_y_vel = 0
            is_jumping = False

    
    # --- Drawing Section ---
    
    # 1. DRAW THE BACKGROUND IMAGE (Fixed screen position)
    screen.blit(background_image, (0, 0)) 

    # 2. Draw Platforms (World coordinates, apply offset)
    for platform in platforms:
        # 1. Calculate the screen position with camera offset
        screen_rect = platform.move(-camera_offset_x, 0)

        # 2. Create a scaled texture surface to fit the platform's width/height
        # We take the texture slice and scale it to match the current platform's dimensions
        texture_surface = pygame.transform.scale(
            background_image_orig.subsurface(PLATFORM_TEXTURE_RECT), 
            (platform.width, platform.height)
        )
        
        # 3. Draw the scaled texture onto the screen position
        screen.blit(texture_surface, screen_rect)

    # 3. DRAW MONSTER AND PLAYER (World coordinates, apply offset)
    screen.blit(monster_image, monster_rect.move(-camera_offset_x, 0))
    screen.blit(player_image, player_rect.move(-camera_offset_x, 0)) 
        
    # 4. Draw Combat Menu (Fixed screen position)
    if game_state == "PLAYER_TURN_MENU":
        button_rects = draw_combat_menu(screen, font, mouse_pos) 

    # 5. Draw Attack Rect (World coordinates, apply offset)
    # Recalculate attack_rect based on current player position (world coords)
    attack_rect = pygame.Rect(player_rect.right, player_rect.y, ATTACK_RANGE, player_rect.height)
        
    if attack_rect.colliderect(monster_rect): 
        # DRAW the attack rect with the camera offset
        pygame.draw.rect(screen, YELLOW, attack_rect.move(-camera_offset_x, 0), 1) 
        
    # 6. Draw HUD/Status (Fixed screen position)
    status_text = f"Player HP: {player.health} | {monster.name} HP: {monster.health} | State: {game_state}"
    status_surface = font.render(status_text, True, WHITE)
    screen.blit(status_surface, (10, 10))

    message_text = font.render(game_message, True, WHITE)
    text_x = SCREEN_WIDTH // 2 - message_text.get_width() // 2
    text_y = SCREEN_HEIGHT - 50 
    screen.blit(message_text, (text_x, text_y))

    # IMPORTANT: Ensure button_rects is available for the next frame's mouse check
    # We clear it here to ensure it's only populated when the menu is drawn
    if game_state != "PLAYER_TURN_MENU":
         button_rects = {} 

    # --- Update the Display ---
    pygame.display.flip()
    clock.tick(60)

# 5. Quit Pygame
pygame.quit()
sys.exit()