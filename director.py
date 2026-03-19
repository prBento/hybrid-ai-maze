import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables (API Keys) from the hidden .env file
load_dotenv()

# ==============================================================================
# LLM GAME DIRECTOR (Generative AI)
# ==============================================================================
class GameDirector:
    """
    A Cloud-based LLM Game Director.
    It receives telemetry data from the local Q-Learning Agent, analyzes its performance, 
    and adjusts the procedural generation rules of the matrix in real-time.
    """

    def __init__(self):
        # We use the standard OpenAI Python SDK, but we point the base URL to Groq's servers.
        # This allows us to use Groq's blazing-fast LPUs (Language Processing Units) for real-time gaming.
        self.client = OpenAI(
            api_key=os.getenv("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1"
        )
        
        # We use Llama 3.1 (8B) as it is incredibly fast, smart, and highly capable of strict JSON formatting
        self.model_id = 'llama-3.1-8b-instant'  

    def evaluate_performance(self, deaths, max_survival_time, current_epsilon):
        """
        Sends the Agent's statistics to the LLM and asks for new game rules.
        Returns a dictionary with the new 'spawn_chance', 'hazard_lifetime', and 'reasoning'.
        """
        print("\n[DIRECTOR] Analyzing AI performance with Groq...")
        
        # --- PROMPT ENGINEERING ---
        # 1. Context: Give the LLM its persona and explain the player.
        # 2. Data: Inject the real-time variables.
        # 3. Rules: Establish strict mathematical bounds for the output.
        # 4. Format: Enforce a rigid JSON structure with a One-Shot example.
        prompt = f"""
        You are the Game Director of a dynamic maze.
        The player is a Q-Learning Artificial Intelligence learning to survive.
        
        Here are the player's current stats:
        - Deaths: {deaths}
        - Max survival time (in frames): {max_survival_time}
        - Epsilon Rate (Randomness. 1.0 is exploring/dumb, near 0.0 is smart): {current_epsilon:.2f}

        Based on this data, adjust the game difficulty to keep the AI engaged:
        - If it dies too much or Epsilon is high, make it easier (lower spawn_chance, higher hazard_lifetime).
        - If it survives for a long time and Epsilon is low, make the game much harder!
        
        Strict limits you must follow:
        - spawn_chance: float number between 0.05 and 0.50
        - hazard_lifetime: integer between 10 and 100
        - IMPORTANT: Your 'reasoning' string MUST explicitly state the new numerical values you applied.

        Respond EXCLUSIVELY with a valid JSON object.
        Use exactly this structure:
        {{
            "spawn_chance": <float_value>,
            "hazard_lifetime": <int_value>,
            "reasoning": "<e.g., 'Agent survived long! Raising spawn to 25% and dropping lifetime to 30.' Max 80 chars!>"
        }}
        """

        try:
            # Call the LLM API
            response = self.client.chat.completions.create(
                model=self.model_id,
                response_format={ "type": "json_object" }, # Forces the model to output valid JSON
                messages=[
                    {"role": "system", "content": "You are a game server that outputs strictly JSON."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Extract the string content from the response
            response_text = response.choices[0].message.content
            
            # Parse the JSON string into a native Python Dictionary
            new_rules = json.loads(response_text)
            print(f"[DIRECTOR] New rules defined: {new_rules}")
            return new_rules
            
        except Exception as e:
            # --- GRACEFUL DEGRADATION (API Fallback) ---
            # If the internet drops, the API hits a rate limit, or the JSON parsing fails,
            # we catch the exception so the game doesn't crash. We return safe default rules.
            print(f"[DIRECTOR ERROR] Failed to contact the API: {e}")
            print("[DIRECTOR] Triggering Graceful Degradation: Keeping default difficulty for safety.")
            
            return {
                "spawn_chance": 0.10, 
                "hazard_lifetime": 50,
                "reasoning": "⚠️ API Connection Lost. Using fallback default state."
            }