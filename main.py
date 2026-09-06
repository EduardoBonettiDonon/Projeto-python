import random
import time


def wait():
    for i in range(2):
        print(".")
        time.sleep(.5)


# ==============================
# ENEMY
# ==============================

turno = 0


class Enemy:
    def __init__(self, name, hp, damage, gold, xp):
        self.name = name
        self.hp = hp
        self.damage = damage
        self.gold = gold
        self.xp = xp


enemies = [
    Enemy("Zombie", 30, 5, 15, 20),
    Enemy("Vampire", 40, 7, 20, 25),
    Enemy("Werewolf", 40, 15, 30, 40),
    Enemy("Witch", 20, 15, 40, 40),
    Enemy("Ghost", 40, 10, 40, 40)
]

minotaur = Enemy("Minotaur", 400, 20, 500, 250)


def generate_enemy():
    if turno % 25 == 0:
        enemy = minotaur
    else:
        enemy = random.choice(enemies)

    damage = enemy.damage * (1 + turno * 0.10)
    hp = enemy.hp * (1 + turno * 0.10)

    return Enemy(
        enemy.name,
        hp,
        damage,
        enemy.gold,
        enemy.xp
    )

# ==============================
# ITEM
# ==============================

class Item:
    def __init__(self, name):
        self.name = name


items = [
    Item("15 Gold"),
    Item("30 Gold"),
    Item("Health Potion"),
]


def random_item():
    return random.choice(items)


def find_item(hero):
    item_found = random_item()

    print(f"You found {item_found.name}!")

    if item_found.name == "15 Gold":
        hero.gold += 15

        print(f"Gold: {hero.gold}")

    elif item_found.name == "30 Gold":
        hero.gold += 30

        print("You received 30 Gold!")
        print(f"Gold: {hero.gold}")

    elif item_found.name == "Health Potion":
        hero.inventory.append(item_found.name)

        print("You received a Health Potion!")

    wait()


# ==============================
# HERO
# ==============================

WEAPONS = {
    "Fists": 10,
    "Wooden Sword": 20,
    "Stone Sword": 35,
    "Iron Sword": 45,
    "Diamond Sword": 70,
}

class Hero:
    def __init__(self, name):
        self.name = name
        self.hp = 100
        self.max_hp = 100
        self.gold = 0

        self.weapon = "Fists"
        self.buffs = 0
        self.level_damage = 0
        self.damage = WEAPONS[self.weapon] + self.buffs + self.level_damage
        

        self.inventory = []
        self.xp = 0
        self.xp_need = 100
        self.level = 1

        self.pet_dmg = 0
        self.pet_name = "none"

    def update_damage(self):
        self.damage = WEAPONS[self.weapon] + self.buffs + self.level_damage

    def add_buff(self, amount):
        self.buffs += amount
        self.update_damage()

    def take_damage(self, amount):
        self.hp -= amount

    def leveling(self):
        while self.xp >= self.xp_need:
            self.xp -= self.xp_need
            self.level += 1
            self.xp_need += 25
            self.max_hp += 50
            self.level_damage += 5
            self.update_damage()
            self.hp = self.max_hp

            print("LEVEL UP!")
            print(f"You are now level {self.level}!")


      

# ==============================
# BATTLE
# ==============================

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

            if hero.pet_dmg == 0:
                pass

            else:

                enemy.hp -= hero.pet_dmg

                print(f"Your pet dealt {hero.pet_dmg} damage")



            if enemy.hp <= 0:

                print(f"You defeated the {enemy.name}!")

                hero.gold += enemy.gold

                print(f"You earned {enemy.gold} gold!")

                hero.xp += enemy.xp

                print(f"You earned {enemy.xp} XP!")
                hero.leveling()


                wait()

                return "victory"

            hero.take_damage(enemy.damage)

            print(
                f"The {enemy.name} dealt "
                f"{enemy.damage} damage!"
            )

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


# ==============================
# CHARACTER
# ==============================

def show_character(hero):
    print(f"""
========== CHARACTER ==========

Hero: {hero.name}
HP: {hero.hp}/{hero.max_hp}
Gold: {hero.gold}
Damage: {hero.damage}
Weapon: {hero.weapon}
""")


# ==============================
# INVENTORY
# ==============================

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

        hero.hp = min(
            hero.hp + 30,
            hero.max_hp
        )

        hero.inventory.remove(item)

        print("You used a Health Potion!")

        print(
            f"HP: {old_hp} -> "
            f"{hero.hp}/{hero.max_hp}"
        )

        wait()



# ==============================
# STORE
# ==============================

def store(hero):

    while True:

        print(f"""
========== STORE ==========

You have {hero.gold} Gold.

------- CONSUMABLES -------

1 - Health Potion - 15 Gold

--------- SWORDS ----------

2 - Wooden Sword  - 45 Gold
3 - Stone Sword   - 100 Gold
4 - Iron Sword    - 300 Gold
5 - Diamond Sword - 800 Gold

6 - Exit
""")

        choice = input("Type here: ")

        # Health Potion
        if choice == "1":

            if hero.gold >= 15:

                hero.gold -= 15

                hero.inventory.append("Health Potion")

                print("You bought a Health Potion!")
                print(f"Gold: {hero.gold}")

                wait()

            else:

                print("You don't have enough gold.")

        # Wooden Sword
        elif choice == "2":

            if hero.weapon == "Wooden Sword":

                print("You already have a Wooden Sword.")

            elif hero.gold >= 45:

                hero.gold -= 45

                hero.weapon = "Wooden Sword"
                hero.update_damage()

                print("You equipped a Wooden Sword!")
                print(f"Damage: {hero.damage}")
                print(f"Gold: {hero.gold}")

                wait()

            else:

                print("You don't have enough gold.")

        # Stone Sword
        elif choice == "3":

            if hero.weapon == "Stone Sword":

                print("You already have a Stone Sword.")

            elif hero.gold >= 100:

                hero.gold -= 100

                hero.weapon = "Stone Sword"
                hero.update_damage()

                print("You equipped a Stone Sword!")
                print(f"Damage: {hero.damage}")
                print(f"Gold: {hero.gold}")

                wait()

            else:

                print("You don't have enough gold.")

        # Iron Sword
        elif choice == "4":

            if hero.weapon == "Iron Sword":

                print("You already have an Iron Sword.")

            elif hero.gold >= 300:

                hero.gold -= 300

                hero.weapon = "Iron Sword"
                hero.update_damage()

                print("You equipped an Iron Sword!")
                print(f"Damage: {hero.damage}")
                print(f"Gold: {hero.gold}")

                wait()

            else:

                print("You don't have enough gold.")

# Diamond Sword
        elif choice == "5":

            if hero.weapon == "Diamond Sword":

                print("You already have an Diamond Sword.")

            elif hero.gold >= 800:

                hero.gold -= 800

                hero.weapon = "Diamond Sword"
                hero.update_damage()

                print("You equipped an Diamond Sword!")
                print(f"Damage: {hero.damage}")
                print(f"Gold: {hero.gold}")

                wait()

            else:

                print("You don't have enough gold.")

        # Exit
        elif choice == "6":

            print("You left the Store.")

            wait()

            break

        else:

            print("Invalid choice.")


# ==============================
# JOURNEY
# ==============================

def journey(hero):
    global turno
    turno+= 1

    print("""
========== JOURNEY ==========

You leave the town and begin your journey...
""")

    wait()

    event = random.randint(1, 1000)

    # Special event
    if event <= 2:

        print("Special!")

        wait()

    # Enemy
    elif event <= 850:

        enemy = generate_enemy()
        battle(hero, enemy)
        

    # Item
    elif event <= 950:

        find_item(hero)

    # Trap
    else:

        print("You fell into a trap!")

        damage = hero.hp // 10
        hero.hp -= damage
        print(f"You lose {damage} HP!")
        
        wait()


# ==============================
# MENU
# ==============================

def show_menu():

    print(f"""
    turno {turno}
What do you want to do?

1 - Go to Store
2 - Continue your Journey
3 - Character
4 - Inventory
5 - Exit
""")

    choice = input("Type here: ")

    return choice


# ==============================
# MAIN
# ==============================

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
