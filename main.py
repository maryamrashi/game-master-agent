import random
import time

# === TOOLS ===
def roll_dice(sides=6):
    return random.randint(1, sides)

def generate_event():
    return random.choice([
        "A mysterious cave appears ahead.",
        "You hear howling in the distance.",
        "A monster blocks your path!",
        "You discover a glowing chest.",
        "An old man offers you wisdom."
    ])

# === AGENTS ===

class NarratorAgent:
    def narrate(self, player_choice):
        print(f"\n📜 Narrator: You chose to '{player_choice}'. Let me spin the tale...")
        time.sleep(1)
        event = generate_event()
        print(f"📖 Event: {event}")
        return event

class MonsterAgent:
    def combat(self, player):
        print("\n👹 MonsterAgent: A Wild Shadow Beast appears!")
        beast_hp = roll_dice(10) + 5
        print(f"⚔️ Combat Begins! Your HP: {player['hp']} | Beast HP: {beast_hp}")

        while beast_hp > 0 and player["hp"] > 0:
            input("🎲 Press Enter to roll your attack dice...")
            player_roll = roll_dice(8)
            monster_roll = roll_dice(6)

            print(f"🧝 You rolled: {player_roll} | 🐉 Beast rolled: {monster_roll}")

            if player_roll >= monster_roll:
                damage = roll_dice(4)
                beast_hp -= damage
                print(f"✅ You hit the beast for {damage} damage! Beast HP: {max(beast_hp, 0)}")
            else:
                damage = roll_dice(3)
                player["hp"] -= damage
                print(f"❌ The beast hits you! You lose {damage} HP. Your HP: {player['hp']}")

            time.sleep(1)

        if player["hp"] > 0:
            print("🏆 You defeated the Shadow Beast!")
            player["xp"] += 10
            return True
        else:
            print("💀 You were defeated...")
            return False

class ItemAgent:
    def reward(self, inventory):
        item = random.choice([
            "🗡️ Sword of Emberfire",
            "🛡️ Aegis of the Ancients",
            "💍 Ring of Eternal Light",
            "🧪 Potion of Vitality"
        ])
        inventory.append(item)
        print(f"🎁 ItemAgent: You received **{item}**!")
        return item

# === GAME MASTER ===

def level_up(player):
    if player["xp"] >= 20 and player["level"] == 1:
        player["level"] += 1
        player["hp"] += 10
        print("🔺 You leveled up to Level 2! Max HP increased!")
    elif player["xp"] >= 40 and player["level"] == 2:
        player["level"] += 1
        player["hp"] += 10
        print("🔺 You reached Level 3! You're a true hero!")

def main():
    narrator = NarratorAgent()
    monster_agent = MonsterAgent()
    item_agent = ItemAgent()
    inventory = []

    # 🎮 Game Start
    print("═════════════════════════════════════════════")
    print("   🧙‍♂️ Welcome to the Legendary Adventure!")
    print("═════════════════════════════════════════════")
    player_name = input("Enter your hero name: ")
    player = {
        "name": player_name,
        "hp": 20,
        "xp": 0,
        "level": 1
    }

    print(f"\n✨ Welcome, {player_name} the Brave. Let the journey begin!")

    while player["hp"] > 0:
        print("\n➡️ Choose your action: explore / rest / inventory / quit")
        choice = input("👉 Your choice: ").strip().lower()

        if choice == "quit":
            print("👋 Farewell, adventurer!")
            break
        elif choice == "rest":
            healed = roll_dice(4)
            player["hp"] += healed
            print(f"🛌 You rested and healed {healed} HP. Current HP: {player['hp']}")
        elif choice == "inventory":
            print(f"🎒 Inventory: {inventory if inventory else 'Empty'}")
        elif choice == "explore":
            event = narrator.narrate(choice)

            if "monster" in event or "beast" in event:
                won = monster_agent.combat(player)
                if won:
                    item_agent.reward(inventory)
            elif "chest" in event or "wisdom" in event:
                item_agent.reward(inventory)
                player["xp"] += 5
                print("🧠 You gained 5 XP from the discovery!")
            else:
                print("🌄 You travel peacefully... for now.")

            level_up(player)
        else:
            print("❓ Invalid choice!")

        print(f"\n❤️ HP: {player['hp']} | 🧪 XP: {player['xp']} | ⭐ Level: {player['level']}")

    print("\n💀 Game Over. Thanks for playing!")

if __name__ == "__main__":
    main()
