import pygame
import sys
import random
import textwrap
import math
import threading
from agent import QLearningAgent
from director import GameDirector

# ==============================================================================
# 1. CONFIGURATION & CONSTANTS
# ==============================================================================
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
MAZE_WIDTH = WINDOW_WIDTH
GRID_SIZE = 40          # The world is divided into 40x40 pixel blocks

# --- ENGINE & PACING TIMERS ---
FPS = 60                # Visual refresh rate (Smooth 60 frames per second)
TICK_RATE = 1.2         # AI Brain speed: Makes ~1.2 decisions per second for a human-like pace
TICK_DELAY = int(1000 // TICK_RATE) # Milliseconds between each AI logical step

# --- SCI-FI COLOR PALETTE ---
BLACK = (8, 10, 15)        # Deep space void (Dark navy/black)
WHITE = (240, 250, 255)    # Cyan-tinted white for glowing highlights
LIGHT_GRAY = (140, 150, 170)
BLUE = (0, 255, 255)       # Neon Cyan (Used for the Agent and safe UI)
RED = (255, 40, 80)        # Neon Magenta/Red (Used for Hazards and danger UI)
DARK_GREY = (20, 25, 35)   # Background elements

def format_time(frames):
    """Converts raw frame counts into a human-readable MM:SS format based on AI TICK_RATE."""
    total_seconds = int(frames // TICK_RATE)
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes:02d}:{seconds:02d}"

# ==============================================================================
# 2. SYSTEM INITIALIZATION
# ==============================================================================
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Hybrid AI Maze: Q-Learning vs LLM Director")

clock = pygame.time.Clock()

# Typography for the XAI HUD
font_main = pygame.font.SysFont('Consolas', 18, bold=True)
font_small = pygame.font.SysFont('Consolas', 15)

# ==============================================================================
# 3. GAME STATE & GLOBAL VARIABLES
# ==============================================================================

# --- A. AGENT LOGICAL STATE ---
# Start the player at a random grid-aligned coordinate
player_x = random.randrange(0, MAZE_WIDTH, GRID_SIZE)
player_y = random.randrange(0, WINDOW_HEIGHT, GRID_SIZE)
# Actions: 0=UP, 1=DOWN, 2=LEFT, 3=RIGHT, 4=UP-LEFT, 5=UP-RIGHT, 6=DOWN-LEFT, 7=DOWN-RIGHT
agent = QLearningAgent(actions=[0, 1, 2, 3, 4, 5, 6, 7])
last_tick_time = pygame.time.get_ticks() # Tracks real-time for the AI brain

# --- B. VISUAL & LERP STATE (Time-Based Smooth Movement) ---
# Separating Logical position (player_x) from Visual position (draw_x) allows 60 FPS rendering
draw_x = float(player_x)
draw_y = float(player_y)
prev_x = float(player_x) # Remembers the exact start position of the current movement
prev_y = float(player_y)

# --- C. ENVIRONMENT & LLM DIRECTOR STATE ---
director = GameDirector()
is_awaiting_director = False
current_spawn_chance = 0.02      # Starts extremely low (Onboarding Phase)
current_hazard_lifetime = 20     # Hazards disappear quickly during onboarding
current_eval_interval = 20       # How many AI ticks before Groq evaluates the game
frame_counter = 0                # Tracks ticks towards the next evaluation

# --- D. EXPLAINABLE AI (XAI) UI LOGS ---
current_llm_reasoning = "System Onboarding: Low hazards to allow safe initial exploration."
current_agent_log = "Action: [START] • System initialized. Waiting for data."
current_q_value = 0.0

# --- E. PERFORMANCE METRICS ---
deaths = 0
frames_survived = 0
max_survival_time = 0
global_high_score = 0


# ==============================================================================
# 4. CORE FUNCTIONS
# ==============================================================================

def get_state(x, y, hazards_lists):
    """
    The AI's Radar. Looks 1 block in the 4 cardinal directions.
    Implements Torus Topology (Pac-Man effect) so the radar wraps around the screen borders.
    Returns: Tuple of 4 integers (1 = Danger, 0 = Clear) mapping to (UP, DOWN, LEFT, RIGHT).
    """
    look_up_y = (y - GRID_SIZE) % WINDOW_HEIGHT
    look_down_y = (y + GRID_SIZE) % WINDOW_HEIGHT
    look_left_x = (x - GRID_SIZE) % MAZE_WIDTH
    look_right_x = (x + GRID_SIZE) % MAZE_WIDTH

    danger_up = 1 if (x, look_up_y) in hazards_lists else 0
    danger_down = 1 if (x, look_down_y) in hazards_lists else 0
    danger_left = 1 if (look_left_x, y) in hazards_lists else 0
    danger_right = 1 if (look_right_x, y) in hazards_lists else 0

    return (danger_up, danger_down, danger_left, danger_right)

def generate_maze(px, py):
    """
    Procedurally generates a new dictionary of hazards across the grid.
    Ensures a safe 5-block cross zone around the player's spawn point to prevent unfair instant deaths.
    """
    new_hazards = {}
    
    # Define the Anti-Spawn Kill Safe Zone
    safe_zone = [
         (px, py),              # Center (Player core)
         (px, py - GRID_SIZE),  # Up
         (px, py + GRID_SIZE),  # Down
         (px - GRID_SIZE, py),  # Left
         (px + GRID_SIZE, py)   # Right
    ]
        
    for x in range(0, MAZE_WIDTH, GRID_SIZE):
         for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
               if (x, y) in safe_zone:
                    continue # Skip spawning hazards in the safe zone
               
               if random.random() < current_spawn_chance:
                    # Assign a random lifetime to the hazard so they don't all blink out at once
                    min_life = max(1, int(current_hazard_lifetime * 0.5))
                    new_hazards[(x, y)] = random.randint(min_life, current_hazard_lifetime)
    
    return new_hazards

def director_worker(deaths_snapshot, time_snapshot, epsilon_snapshot):
    """
    Background Thread Function: Calls the Groq LLM API asynchronously.
    Prevents the main game loop (60 FPS rendering) from freezing while waiting for network responses.
    """
    global current_spawn_chance, current_hazard_lifetime, current_llm_reasoning
    global current_eval_interval, is_awaiting_director

    try:
        # Request new matrix rules from the LLM
        new_rules = director.evaluate_performance(deaths_snapshot, time_snapshot, epsilon_snapshot)

        new_spawn = new_rules.get("spawn_chance", current_spawn_chance)
        new_lifetime = new_rules.get("hazard_lifetime", current_hazard_lifetime)
        current_llm_reasoning = new_rules.get("reasoning", "Default difficulty adjustment.")

        # Adaptive Epsilon Shock: If the LLM makes the game much harder, spike the AI's randomness
        # This forces the agent to forget old safe routes and explore the new hostile environment
        spawn_increase = new_spawn - current_spawn_chance
        if (spawn_increase > 0 or new_lifetime < current_hazard_lifetime) and agent.epsilon < 0.50:
            extra_shock = max(0, spawn_increase) * 1.5
            dynamic_shock = min(0.05 + extra_shock, 0.30)
            agent.epsilon = min(agent.epsilon + dynamic_shock, 0.85)
            print(f"[ADAPTATION] Hostile environment! Epsilon increased to: {agent.epsilon:.2f}")
        
        # Apply the LLM's new rules to the world
        current_spawn_chance = new_spawn
        current_hazard_lifetime = new_lifetime

        # Dynamic Pacing: Evaluate more often if the agent is exploring (high epsilon)
        base_interval = 20
        if agent.epsilon > 0.5: current_eval_interval = int(base_interval * 1.5)
        elif agent.epsilon < 0.2: current_eval_interval = int(base_interval * 0.7)
        else: current_eval_interval = base_interval

    except Exception as e:
        # GRACEFUL DEGRADATION (API Fallback)
        # If internet drops or API times out, keep the game running using the Last Known Good State
        print(f"[THREAD ERROR] Failed to contact Groq: {e}")
        current_llm_reasoning = "⚠️ API Connection Lost. Using Last Known Good State to keep matrix stable."
        current_eval_interval = 50 # Backoff: Wait longer before hitting the broken API again
    
    is_awaiting_director = False

# Initialize the very first world map
hazards = generate_maze(player_x, player_y)


# ==============================================================================
# 5. MAIN GAME LOOP
# ==============================================================================
running = True
while running:

    # --------------------------------------------------------------------------
    # A. EVENT HANDLING (Window & OS Inputs)
    # --------------------------------------------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
             # Handle dynamic window resizing gracefully
             WINDOW_WIDTH = event.w
             WINDOW_HEIGHT = event.h
             MAZE_WIDTH = WINDOW_WIDTH
             screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)

             # Keep player inbound if window shrinks
             if player_x >= MAZE_WIDTH: player_x = MAZE_WIDTH - GRID_SIZE
             if player_y >= WINDOW_HEIGHT: player_y = WINDOW_HEIGHT - GRID_SIZE
    
    # --------------------------------------------------------------------------
    # B. GAME LOGIC UPDATE (The AI Brain)
    # --------------------------------------------------------------------------
    current_time = pygame.time.get_ticks()

    # Time Gate: The AI only processes logic based on TICK_DELAY (e.g., 1.2 times a second)
    if current_time - last_tick_time >= TICK_DELAY:
         
         # Save current position before calculating the next move (used for Visual Lerping)
         prev_x = float(player_x)
         prev_y = float(player_y)
         last_tick_time = current_time
    
         # --- 1. UPDATE DYNAMIC ENVIRONMENT ---
         # Age existing hazards and remove dead ones
         keys_to_remove = []
         for pos in hazards:
            hazards[pos] -= 1 
            if hazards[pos] <= 0:
                keys_to_remove.append(pos)
         for pos in keys_to_remove:
            del hazards[pos]

         # Randomly spawn new hazards organically based on LLM rules
         if random.random() < current_spawn_chance:
            hx = random.randrange(0, MAZE_WIDTH, GRID_SIZE)
            hy = random.randrange(0, WINDOW_HEIGHT, GRID_SIZE)
            if (hx, hy) != (player_x, player_y) and (hx, hy) not in hazards:
                hazards[(hx, hy)] = current_hazard_lifetime


         # --- 2. AGENT KNOWLEDGE CYCLE (Decision Making) ---
         # Observe the current state (Radar bounds)
         current_state = get_state(player_x, player_y, hazards)

         # Q-Learning: Ask the brain what action to take based on the observed state
         action = agent.choose_action(current_state)

         # Extract mathematical values for Explainable AI (XAI) UI
         q_vals = agent.q_table.get(current_state, [0.0] * 8)
         chosen_q = q_vals[action]
         dirs = ["UP", "DOWN", "LEFT", "RIGHT", "UP-LEFT", "UP-RIGHT", "DOWN-LEFT", "DOWN-RIGHT"]
         action_str = dirs[action]

         # Translate Q-Value into Natural Language for the HUD
         if chosen_q == 0.0:
             phrases = [
                 f"No prior data. Exploring {action_str} blindly.",
                 f"Mapping uncharted territory. Moving {action_str}.",
                 f"Lacking intel. Taking a random step {action_str}."
             ]
             nl_text = random.choice(phrases)
         elif chosen_q > 0:
             phrases = [
                 f"Safe route recognized. Proceeding {action_str}.",
                 f"Positive reinforcement detected. Heading {action_str}.",
                 f"Following optimized path. Moving {action_str}."
             ]
             nl_text = random.choice(phrases)
         else:
             phrases = [
                 f"Lethal threat ahead! Rerouting {action_str}.",
                 f"Evading danger zone. Executing evasive maneuver {action_str}.",
                 f"Hazard predicted. Changing course to {action_str}."
             ]
             nl_text = random.choice(phrases)
        
         # Commit strings to UI variables
         current_q_value = chosen_q
         current_agent_log = f"Action: [{action_str}] • {nl_text}"


         # --- 3. PHYSICS & COLLISION PREDICTION ---
         # Calculate where the chosen action will land the agent
         next_x, next_y = player_x, player_y
         if action == 0: next_y -= GRID_SIZE     # UP
         elif action == 1: next_y += GRID_SIZE   # DOWN
         elif action == 2: next_x -= GRID_SIZE   # LEFT
         elif action == 3: next_x += GRID_SIZE   # RIGHT
         elif action == 4: # UP-LEFT
              next_x -= GRID_SIZE
              next_y -= GRID_SIZE
         elif action == 5: # UP-RIGHT
              next_x += GRID_SIZE
              next_y -= GRID_SIZE
         elif action == 6: # DOWN-LEFT
              next_x -= GRID_SIZE
              next_y += GRID_SIZE
         elif action == 7: # DOWN-RIGHT
              next_x += GRID_SIZE
              next_y += GRID_SIZE

         # Apply Torus Topology (Pac-Man Screen Wrap-around)
         next_x = next_x % MAZE_WIDTH
         next_y = next_y % WINDOW_HEIGHT

         # Check if the planned move lands on a Plasma Hazard
         is_deadly = False
         if (next_x, next_y) in hazards:
             is_deadly = True 

         # Advanced Collision Physics: Prevent Diagonal Corner-Cutting (Ghosting)
         # If moving diagonally (actions 4-7), verify if the two adjacent blocks are hazards
         elif action >= 4:
             cross_1 = (player_x, next_y)
             cross_2 = (next_x, player_y)

             cross_1 = (cross_1[0] % MAZE_WIDTH, cross_1[1] % WINDOW_HEIGHT)
             cross_2 = (cross_2[0] % MAZE_WIDTH, cross_2[1] % WINDOW_HEIGHT)

             if cross_1 in hazards or cross_2 in hazards:
                 is_deadly = True
                 # Snap explosion coordinates to the exact corner hazard hit
                 next_x = cross_1[0] if cross_1 in hazards else cross_2[0]
                 next_y = cross_1[1] if cross_1 in hazards else cross_2[1]


         # --- 4. REWARD ASSIGNMENT & WORLD REBUILD ---
         if is_deadly:
            # Game Over logic
            if frames_survived > global_high_score:
                global_high_score = frames_survived

            reward = -100 # Heavy penalty for the Q-Table
            deaths += 1
            frames_survived = 0
            print(f"Crash! AI Randomness (Epsilon): {agent.epsilon:.2f} | Resetting map...")

            # --- VISUAL IMPACT: Freeze Frame Explosion ---
            # We break the rendering loop momentarily to show the impact explicitly
            draw_x = float(next_x)
            draw_y = float(next_y)
            body_rect = (draw_x + 8, draw_y + 10, 24, 24)
            pygame.draw.rect(screen, (50, 120, 220), body_rect, border_radius=5)
            
            crash_x = next_x + (GRID_SIZE // 2)
            crash_y = next_y + (GRID_SIZE // 2)

            pygame.draw.circle(screen, (255, 100, 0), (crash_x, crash_y), 30) # Fire
            pygame.draw.circle(screen, WHITE, (crash_x, crash_y), 15)         # Core
            pygame.display.flip()
            pygame.time.delay(400) # Freeze for 400ms to let player process the death
            # ---------------------------------------------

            # Respawn agent and rebuild a brand new randomized maze
            player_x = random.randrange(0, MAZE_WIDTH, GRID_SIZE)
            player_y = random.randrange(0, WINDOW_HEIGHT, GRID_SIZE)
            draw_x = float(player_x)
            draw_y = float(player_y)
            prev_x = float(player_x)
            prev_y = float(player_y)
            hazards = generate_maze(player_x, player_y) 

         else:
            # Survival logic
            reward = 1 # Positive reinforcement for surviving a step
            frames_survived += 1
            if frames_survived > max_survival_time:
                max_survival_time = frames_survived         

            player_x, player_y = next_x, next_y # Officially move the logical character

         # --- 5. CAMERA CORRECTION (Wrap-around Lerp) ---
         # If distance jumped > 2 blocks, it means the agent teleported across the screen borders.
         # We adjust prev_x/y out of bounds so the Lerp animation pulls them into the screen cleanly.
         if player_x - prev_x > GRID_SIZE * 2: 
             prev_x += MAZE_WIDTH
         elif prev_x - player_x > GRID_SIZE * 2: 
             prev_x -= MAZE_WIDTH
         if player_y - prev_y > GRID_SIZE * 2: 
             prev_y += WINDOW_HEIGHT
         elif prev_y - player_y > GRID_SIZE * 2: 
             prev_y -= WINDOW_HEIGHT         

         # --- 6. BELLMAN EQUATION TRIGGER ---
         # Observe the new state post-movement and update the mathematical Q-Table
         next_state = get_state(player_x, player_y, hazards)
         agent.learn(current_state, action, reward, next_state)

         # --- 7. THE DIRECTOR INTERVENES ---
         frame_counter += 1
         if frame_counter >= current_eval_interval and not is_awaiting_director:
            print("\n --- LLM EVALUATION TRIGGERED ---")

            # Clash Mechanic: RPG style dice roll (D20)
            agent_roll = random.randint(1, 20)
            director_roll = random.randint(1, 20)
            print(f"[CLASH] Agent rolled: {agent_roll} | Director rolled: {director_roll}")

            if agent_roll > director_roll:
                # Agent resists the matrix alteration, gaining more time to learn current layout
                print("[CLASH] Agent Wins! Intervention blocked. Gaining time to learn...")              
                print("--------------------------------\n")
            else:              
                # Director wins. Threading prevents 60 FPS stuttering while calling the API.
                print("[CLASH] Director Wins! Invoking Groq to alter the matrix...")
                is_awaiting_director = True
                thread = threading.Thread(target=director_worker, args=(deaths, max_survival_time, agent.epsilon))
                thread.daemon = True
                thread.start()
            
            # Reset metrics for the next epoch regardless of clash outcome
            deaths = 0
            max_survival_time = 0
            frame_counter = 0


    # --------------------------------------------------------------------------
    # C. RENDERING ENGINE (Runs independently at 60 FPS)
    # --------------------------------------------------------------------------
    
    # 1. Background (Holographic Tactical Grid)
    screen.fill(BLACK)
    for x in range(0, MAZE_WIDTH, GRID_SIZE):
         pygame.draw.line(screen, (20, 28, 45), (x, 0), (x, WINDOW_HEIGHT), 1)
    for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
         pygame.draw.line(screen, (20, 28, 45), (0, y), (MAZE_WIDTH, y), 1)       

    # Global continuous sine wave used for pulsating animations
    time_now = pygame.time.get_ticks()
    pulse = (math.sin(time_now / 200.0) + 1) / 2.0

    # 2. Draw Plasma Hazards
    for h_x, h_y in hazards:
         center_x = h_x + (GRID_SIZE // 2)
         center_y = h_y + (GRID_SIZE // 2)

         # Phase Shift: Uses grid coordinates to offset the sine wave, making them pulsate asynchronously
         time_offset = h_x + h_y
         mine_pulse = (math.sin((time_now + time_offset * 5) / 150.0) + 1) / 2.0
         glow_radius = int(10 + (mine_pulse * 6)) 
         
         # Fake Glow effect via overlaid transparent circles
         pygame.draw.circle(screen, (80, 20, 20), (center_x, center_y), glow_radius + 4) # Outer Aura
         pygame.draw.circle(screen, (100, 25, 50), (center_x, center_y), glow_radius)    # Mid Glow
         pygame.draw.circle(screen, RED, (center_x, center_y), glow_radius - 3)          # Inner Ring
         pygame.draw.circle(screen, WHITE, (center_x, center_y), 4)                      # Hot Core
         
         # Tactical Crosshair overlay
         pygame.draw.line(screen, WHITE, (center_x - 12, center_y), (center_x + 12, center_y), 2)
         pygame.draw.line(screen, WHITE, (center_x, center_y - 12), (center_x, center_y + 12), 2) 
         
    # 3. Time-Based Lerp (Linear Interpolation)
    # Calculates exact visual position based on how much time has passed since the last AI tick
    progress = (time_now - last_tick_time) / TICK_DELAY
    progress = min(progress, 1.0) # Caps at 100% to prevent overshooting destination
    draw_x = prev_x + (player_x - prev_x) * progress
    draw_y = prev_y + (player_y - prev_y) * progress

    # 4. Draw Agent (Tactical Drone Design)
    center_draw_x = draw_x + 20
    center_draw_y = draw_y + 20

    # Magnetic Shield Outline
    shield_pulse = int(2 + (pulse * 2))
    pygame.draw.circle(screen, BLUE, (center_draw_x, center_draw_y), 16 + shield_pulse, 1)

    # Drone Chassis
    pygame.draw.circle(screen, DARK_GREY, (center_draw_x, center_draw_y), 14)
    pygame.draw.circle(screen, BLUE, (center_draw_x, center_draw_y), 12, 2)

    # Dynamic Eye Color (Visual XAI indicator of Agent Confidence)
    if agent.epsilon > 0.6:
         eye_color = (255, 180, 0)  # Orange: High exploration / Clueless
    elif agent.epsilon < 0.3:
         eye_color = (50, 255, 100) # Neon Green: Low epsilon / Confident & Smart
    else:
         eye_color = BLUE           # Cyan: Standard learning state

    # Blinking Eye Animation
    eye_width = 14 if pulse > 0.1 else 4 
    pygame.draw.rect(screen, (10, 10, 15), (center_draw_x - 8, center_draw_y - 4, 16, 8))
    pygame.draw.rect(screen, eye_color, (center_draw_x - (eye_width//2), center_draw_y - 2, eye_width, 4))

    # Telemetry Antenna
    pygame.draw.line(screen, LIGHT_GRAY, (center_draw_x, center_draw_y - 14), (center_draw_x, center_draw_y - 22), 2)
    antenna_color = RED if pulse > 0.5 else BLUE
    pygame.draw.circle(screen, antenna_color, (center_draw_x, center_draw_y - 22), 3)

    # --------------------------------------------------------------------------
    # D. HUD (Heads-Up Display & XAI Logs)
    # --------------------------------------------------------------------------
    current_w, current_h = screen.get_size()
    hud_height = 150 

    hud_surface = pygame.Surface((current_w, hud_height))
    hud_surface.set_alpha(220) 
    hud_surface.fill(BLACK)
    screen.blit(hud_surface, (0, current_h - hud_height))
    pygame.draw.line(screen, LIGHT_GRAY, (0, current_h - hud_height), (current_w, current_h - hud_height), 1)

    pad_y = current_h - hud_height + 15
    hud_center_y = current_h - (hud_height // 2)

    # --- Column 1: Agent Stats ---
    col1_center = 120
    t1 = font_main.render("Q-Learning AI", True, WHITE)
    screen.blit(t1, t1.get_rect(center=(col1_center, hud_center_y - 25)))
    t2 = font_main.render(f"Time: {format_time(frames_survived)}", True, LIGHT_GRAY)
    screen.blit(t2, t2.get_rect(center=(col1_center, hud_center_y)))
    t3 = font_main.render(f"High Score: {format_time(global_high_score)}", True, (255, 215, 0))
    screen.blit(t3, t3.get_rect(center=(col1_center, hud_center_y + 25)))

    pygame.draw.line(screen, (70, 70, 70), (240, current_h - hud_height + 15), (240, current_h - 15), 1)
    
    # --- Column 2: LLM Director Stats ---
    col2_center = 410
    t4 = font_main.render("LLM Decision Rules (Groq)", True, WHITE)
    screen.blit(t4, t4.get_rect(center=(col2_center, hud_center_y - 25)))
    t5 = font_main.render(f"Exploration (Epsilon): {agent.epsilon:.2f}", True, LIGHT_GRAY)
    screen.blit(t5, t5.get_rect(center=(col2_center, hud_center_y)))
    t6 = font_small.render(f"Spawn Rate: {int(current_spawn_chance * 100)}%", True, (255, 100, 100))
    screen.blit(t6, t6.get_rect(center=(col2_center, hud_center_y + 25)))

    pygame.draw.line(screen, (70, 70, 70), (580, pad_y), (580, current_h - 15), 1)

    # --- Column 3: Explainable AI (XAI) Terminal ---
    col3_x = 600
    
    # 3.1 LLM Natural Language Log
    log_title = font_main.render("Groq Decision Log", True, WHITE)
    screen.blit(log_title, (col3_x, pad_y))

    tag_x = col3_x + log_title.get_width() + 10
    xai_tag = font_small.render("• Natural Language Translation", True, BLUE)
    screen.blit(xai_tag, (tag_x, pad_y + 2))

    # Wraps LLM text to fit the UI boundaries
    wrapped_reasoning = textwrap.wrap(current_llm_reasoning, width=70)
    for i, line in enumerate(wrapped_reasoning):
        texto_renderizado = font_small.render(line, True, (180, 255, 180))
        screen.blit(texto_renderizado, (col3_x, pad_y + 26 + (i * 20)))

    # 3.2 Agent Q-Table Translation Log
    agent_y = pad_y + 88
    agent_title = font_main.render("Agent Thought Process (Q-Table)", True, WHITE)
    screen.blit(agent_title, (col3_x, agent_y))

    tag_q_x = col3_x + agent_title.get_width() + 10
    tag_q_text = font_small.render(f"• Q: {current_q_value:.2f} (Higher = Safer)", True, BLUE)
    screen.blit(tag_q_text, (tag_q_x, agent_y + 2))

    text_agent = font_small.render(current_agent_log, True, (180, 255, 180))
    screen.blit(text_agent, (col3_x, agent_y + 24))

    # --------------------------------------------------------------------------

    # Push all drawings to the physical display
    pygame.display.flip()

    # Cap engine at 60 Frames Per Second to avoid CPU burning
    clock.tick(FPS)

# ==============================================================================
# 5. GRACEFUL EXIT
# ==============================================================================
pygame.quit()
sys.exit()