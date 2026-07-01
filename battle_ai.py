import os
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# Load Pokémon dataset
pokemon = pd.read_csv("data/pokemon.csv")


def predict_battle(pokemon1_name, pokemon2_name):

    # Find Pokémon
    pokemon1 = pokemon[pokemon["Name"].str.lower() == pokemon1_name.lower()]
    pokemon2 = pokemon[pokemon["Name"].str.lower() == pokemon2_name.lower()]

    if pokemon1.empty:
        return f"❌ Pokémon '{pokemon1_name}' not found!"

    if pokemon2.empty:
        return f"❌ Pokémon '{pokemon2_name}' not found!"

    # Convert to dictionaries
    pokemon1 = pokemon1.iloc[0].to_dict()
    pokemon2 = pokemon2.iloc[0].to_dict()

    battle_info = {
        "Pokemon1": {
            "Name": pokemon1["Name"],
            "Type1": pokemon1["Type1"],
            "Type2": pokemon1["Type2"],
            "HP": pokemon1["HP"],
            "Attack": pokemon1["Attack"],
            "Defense": pokemon1["Defense"],
            "SpAtk": pokemon1["SpAtk"],
            "SpDef": pokemon1["SpDef"],
            "Speed": pokemon1["Speed"],
            "Legendary": pokemon1["Legendary"],
        },
        "Pokemon2": {
            "Name": pokemon2["Name"],
            "Type1": pokemon2["Type1"],
            "Type2": pokemon2["Type2"],
            "HP": pokemon2["HP"],
            "Attack": pokemon2["Attack"],
            "Defense": pokemon2["Defense"],
            "SpAtk": pokemon2["SpAtk"],
            "SpDef": pokemon2["SpDef"],
            "Speed": pokemon2["Speed"],
            "Legendary": pokemon2["Legendary"],
        },
    }

    prompt = f"""
You are a Pokémon battle simulator. Use Gen Z slang and emojis to make your responses fun and engaging. Analyze the following battle data between two Pokémon and predict the winner based on their stats, types, and other relevant factors.

Use ONLY:
- The provided stats
- The official Pokémon type chart
- Standard Pokémon mechanics

Do NOT invent moves, abilities, held items, EVs, IVs, weather, or Mega Evolutions unless explicitly given.

Battle Data:

{battle_info}

Respond exactly like this:

🏆 Winner:
📊 Confidence:
⚔️ Type Advantage:
📈 Stat Advantage:
🧠 Reason:
"""

    response = client.chat.completions.create(
        model="openai/gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=300,
        temperature=0.3
    )

    return response.choices[0].message.content