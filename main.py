import random
import time


def wait():
    for i in range(3):
        print(".")
        time.sleep(1)


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
        self.weapon = "Fists"
        self.inventory = []

    def take_damage(self, amount):
        self.hp -= amount


enemies = [
    Enemy("Zombie", 50, 5, 5),
    Enemy("Vampire", 75, 7, 10),
    Enemy("Werewolf", 110, 4, 15),
    Enemy("Witch", 60, 15, 20),
    Enemy("Ghost", 1, 1, 1),
]


def generate_enemy():
    enemy = random.choice(enemies)

    return Enemy(
        enemy.name,
        enemy.hp,
        enemy.damage,
        enemy.gold
    )


def battle(hero, enemy):
    print(f"""
========== BATTLE ==========

A wild {enemy.name} appeared!
""")

    while hero.hp > 0 and enemy.hp > 0:

        print(f"""
{hero.name}: {hero.hp}/{hero.max_hp} HP
{enemy.name}: {enemy.hp} HP
""")

        print("1 - Attack")
        print("2 - Run")
        print("3 - Use Item")

        choice = input("Type here: ")

        if choice == "1":
            enemy.hp -= hero.damage
            print(f"You dealt {hero.damage} damage!")

            if enemy.hp <= 0:
                print(f"You defeated the {enemy.name}!")

                hero.gold += enemy.gold
                print(f"You earned {enemy.gold} gold!")

                wait()
                return "victory"

            hero.take_damage(enemy.damage)
            print(f"The {enemy.name} dealt {enemy.damage} damage!")

        elif choice == "2":
            print("You ran away!")
            wait()
            return "run"

        elif choice == "3":
            use_item(hero)

        else:
            print("Invalid choice.")


    if hero.hp <= 0:
        print("""
========== DEFEAT ==========

You are dead!
""")

        lost_gold = hero.gold // 2
        hero.gold -= lost_gold

        print(f"You lost {lost_gold} gold.")
        print(f"Gold remaining: {hero.gold}")

        hero.hp = hero.max_hp

        wait()
        return "defeat"


def show_character(hero):
    print(f"""
========== CHARACTER ==========

Hero: {hero.name}
HP: {hero.hp}/{hero.max_hp}
Gold: {hero.gold}
Damage: {hero.damage}
Weapon: {hero.weapon}
""")


def show_inventory(hero):
    print("""
========== INVENTORY ==========
""")

    if not hero.inventory:
        print("Your inventory is empty.")
    else:
        for i, item in enumerate(hero.inventory, 1):
            print(f"{i} - {item}")


def use_item(hero):
    if not hero.inventory:
        print("Your inventory is empty.")
        wait()
        return

    print("""
========== ITEMS ==========
""")

    for i, item in enumerate(hero.inventory, 1):
        print(f"{i} - {item}")

    print("0 - Cancel")

    choice = input("Type here: ")

    if choice == "0":
        return

    if not choice.isdigit():
        print("Invalid choice.")
        return

    choice = int(choice)

    if choice < 1 or choice > len(hero.inventory):
        print("Invalid choice.")
        return

    item = hero.inventory[choice - 1]

    if item == "Health Potion":

        if hero.hp == hero.max_hp:
            print("Your HP is already full.")
            return

        old_hp = hero.hp

        hero.hp = min(hero.hp + 30, hero.max_hp)

        hero.inventory.remove(item)

        print("You used a Health Potion!")
        print(f"HP: {old_hp} -> {hero.hp}/{hero.max_hp}")

        wait()


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

            if hero.gold >= 20:
                hero.gold -= 20
                hero.inventory.append("Health Potion")

                print("You bought a Health Potion!")
                print(f"Gold: {hero.gold}")

                wait()

            else:
                print("You don't have enough gold.")

        elif choice == "2":

            if hero.weapon == "Wooden Sword":
                print("You already have a Wooden Sword.")

            elif hero.gold >= 45:
                hero.gold -= 45

                hero.weapon = "Wooden Sword"
                hero.damage += 10

                print("You equipped a Wooden Sword!")
                print(f"Damage: {hero.damage}")
                print(f"Gold: {hero.gold}")

                wait()

            else:
                print("You don't have enough gold.")

        elif choice == "3":
            print("You left the Store.")
            wait()
            break

        else:
            print("Invalid choice.")


def journey(hero):
    print("""
========== JOURNEY ==========

You leave the town and begin your journey...
""")

    wait()

    event = random.randint(1, 1000)

    if event <= 2:
        print("Special!")
        wait()

    elif event <= 750:
        enemy = generate_enemy()
        battle(hero, enemy)

    elif event <= 950:
        print("You found an item!")
        wait()

    else:
        print("You fell into a trap!")
        wait()


def show_menu():
    print("""
What do you want to do?

1 - Go to Store
2 - Continue your Journey
3 - Character
4 - Inventory
5 - Exit
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
    wait()

    while True:
        choice = show_menu()

        match choice:

            case "1":
                print("You entered the Store.")
                wait()
                store(hero)

            case "2":
                journey(hero)

            case "3":
                show_character(hero)
                wait()

            case "4":
                show_inventory(hero)
                wait()

            case "5":
                print("Goodbye!")
                break

            case _:
                print("Invalid choice.")
                wait()


if __name__ == "__main__":
    main()
