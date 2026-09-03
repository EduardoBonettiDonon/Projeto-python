import random
import time

class Enemy:
    def __init__(self, name, hp, damage, gold):
        self.name = name
        self.hp = hp
        self.damage = damage
        self.gold = gold
        


class Hero:
    def __init__(self, name):
        self.name = name
        self.hp = 100
        self.max_hp = 100
        self.gold = 200
        self.damage = 10
        self.has_sword = 0

    def take_damage(self, amount):
        self.hp -= amount

enemies = [
    Enemy("Goblin", 35, 5, 10),
    Enemy("Orc", 70, 15, 30)
]


def show_character(hero):
    print(f"""
Hero: {hero.name}
HP: {hero.hp}/{hero.max_hp}
Gold: {hero.gold}
Damage: {hero.damage}
""")
    

def store(hero):
    while True:
        print("""
========== STORE ==========

1 - Health Potion - 20 Gold
2 - Wooden Sword  - 45 Gold
3 - Exit
""")

        choice = input("Type here: ")

        if choice == "1":
            if hero.hp == hero.max_hp:
                print("Your HP is already full.")

            elif hero.gold >= 20:
                hero.gold -= 20
                hero.hp = min(hero.hp + 30, hero.max_hp)

                print("You bought a Health Potion!")
                print(f"HP: {hero.hp}/{hero.max_hp}")
                print(f"Gold: {hero.gold}")

            else:
                print("You don't have enough gold.")

        elif choice == "2":
            if hero.has_sword == 1:
                print("You already have a Wooden Sword.")

            elif hero.gold >= 45:
                hero.gold -= 45
                hero.damage += 10
                hero.has_sword = 1

                print("You bought a Wooden Sword")
                print(f"Damage: {hero.damage}")
                print(f"Gold: {hero.gold}")

            else:
                print("You don't have enough gold.")

        elif choice == "3":
            print("You left the Store.")
            break

        else:
            print("Invalid choice.")

def journey(hero):
      print("""
========== JOURNEY ==========

You leave the town and begin your journey...
""")
      event = random.randint(1, 1000)

      if event <= 2:
        print("Especial!")

      elif event <= 750:
        print("Encontrou inimigo!")

      elif event <= 950:
        print("Encontrou item!")

      else:
        print("Caiu numa armadilha!")
      



def show_menu():
    print("""
What do you want to do?

1 - Go to Store
2 - Continue your Journey
3 - Character
4 - Exit
""")

    choice = input("Type here: ")

    return choice


def main():
    print("""
================================
           ⚔️ ARENA ⚔️
================================
""")

    name = input("Give your Hero a name: ")

    hero = Hero(name)

    show_character(hero)

    while True:
        choice = show_menu()

        match choice:
            case "1":
                print("You entered the Store.")
                store(hero)

            case "2":
                journey(hero)

            case "3":
                show_character(hero)

            case "4":
                print("Goodbye!")
                break

            case _:
                print("Invalid choice.")


if __name__ == "__main__":
    main()
