import json
from critter import Critter
from food import Food
import config

def save_state(critters, food, generation):
    try:
        state = {
            "generation":generation,
            "critters":[c.to_dict() for c in critters],
            "food":[f.to_dict() for f in food],
        }
        with open(config.SAVE_FILE, "w") as f:
            json.dump(state, f, indent=2)
        print("Sim state saved.")
    except Exception as e:
        print(f"Error saving state: {e}")
def load_state():
    try:
        with open(config.SAVE_FILE, 'r') as f:
            state = json.load(f)
        critters = [Critter.from_dict(cd) for cd in state.get("critters", [])]
        food = [Food.from_dict(fd) for fd in state.get("food", [])]
        generation = state.get("generation", 0)

        print("Simulation state loaded")
        return critters, food, generation
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print("No save file found, starting new sim.")
        return None, None, None
    except Exception as e:
        print(f"Error loading state: {e}. starting new sim")
        return None, None, None