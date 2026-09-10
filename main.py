import random
import time


# ==============================
# WAIT
# ==============================

def wait():

    for i in range(2):

        print(".")

        time.sleep(.5)


# ==============================
# ENEMY
# ==============================

enemy_count = 0


class Enemy:

    def __init__(self, name, hp, damage, gold, xp):

        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.damage = damage
        self.gold = gold
        self.xp = xp


ENEMIES = [

    Enemy("Zombie", 40, 10, 15, 20),

    Enemy("Vampire", 50, 12, 20, 25),

    Enemy("Werewolf", 50, 17, 30, 40),

    Enemy("Witch", 40, 15, 40, 40),

    Enemy("Ghost", 50, 15, 40, 40),

]


BOSSES = [

    Enemy("Minotaur", 300, 18, 500, 250),

]


def generate_enemy():

    global enemy_count

    enemy_count += 1

    # Boss a cada 25 inimigos

    if enemy_count % 25 == 0:

        base_enemy = random.choice(BOSSES)

    else:

        base_enemy = random.choice(ENEMIES)

    # +5% de HP e dano por inimigo

    multiplier = 1 + (enemy_count - 1) * 0.05

    hp = round(base_enemy.hp * multiplier)

    damage = round(base_enemy.damage * multiplier)

    return Enemy(

        base_enemy.name,
        hp,
        damage,
        base_enemy.gold,
        base_enemy.xp

    )


# ==============================
# WEAPONS
# ==============================

WEAPONS = {

    "Fists": {
        "damage": 10,
        "price": 0,
    },

    "Wooden Sword": {
        "damage": 20,
        "price": 45,
    },

    "Stone Sword": {
        "damage": 35,
        "price": 100,
    },

    "Iron Sword": {
        "damage": 45,
        "price": 300,
    },

    "Diamond Sword": {
        "damage": 70,
        "price": 800,
    },

}


# ==============================
# ITEMS
# ==============================

ITEMS = {

    "Health Potion": {
        "type": "heal",
        "value": 50,
        "price": 20,
    },

    "Big Health Potion": {
        "type": "heal",
        "value": 120,
        "price": 40,
    },

}


# ==============================
# NPCS
# ==============================

NPCS = [

    {
        "name": "Merchant",
        "message": "I have some spare Gold. Take it.",
        "reward": 50,
    },

    {
        "name": "Traveler",
        "message": "The road ahead is dangerous. Take this Gold.",
        "reward": 25,
    },

    {
        "name": "Old Man",
        "message": "You look like you could use some help.",
        "reward": 100,
    },

]


# ==============================
# HERO
# ==============================

class Hero:

    def __init__(self, name):

        self.name = name

        # Status

        self.level = 1
        self.xp = 0
        self.xp_need = 100

        self.max_hp = 100
        self.hp = self.max_hp

        self.gold = 0

        # Combat

        self.weapon = "Fists"
        self.buffs = 0

        # Inventory

        self.inventory = []

        # Pet

        self.pet = None

    @property
    def damage(self):

        weapon_damage = WEAPONS[self.weapon]["damage"]

        level_damage = (self.level - 1) * 5

        return weapon_damage + self.buffs + level_damage

    def gain_xp(self, amount):

        self.xp += amount

        print(f"You earned {amount} XP!")

        while self.xp >= self.xp_need:

            self.xp -= self.xp_need

            self.level += 1

            self.xp_need += 25

            self.max_hp += 40

            self.hp = self.max_hp

            print("LEVEL UP!")

            print(f"You are now level {self.level}!")

            print(f"Max HP: {self.max_hp}")

            print(f"Damage: {self.damage}")

    def take_damage(self, amount):

        self.hp -= amount

        if self.hp < 0:

            self.hp = 0


# ==============================
# CHARACTER
# ==============================

def character(hero):

    print(f"""
========== CHARACTER ==========

Name: {hero.name}

Level: {hero.level}
XP: {hero.xp}/{hero.xp_need}

HP: {hero.hp}/{hero.max_hp}
Gold: {hero.gold}

Weapon: {hero.weapon}
Damage: {hero.damage}
Buffs: {hero.buffs}

Pet: {hero.pet if hero.pet else "None"}

===============================
""")

    wait()


# ==============================
# INVENTORY
# ==============================

def inventory(hero):

    print("""
========== INVENTORY ==========
""")

    if not hero.inventory:

        print("Your inventory is empty.")

    else:

        for i, item_name in enumerate(hero.inventory, 1):

            print(f"{i} - {item_name}")

    print("""
===============================
""")

    wait()


# ==============================
# USE ITEM
# ==============================

def use_item(hero, item_name):

    if item_name not in hero.inventory:

        print("You don't have this item.")

        return False

    item = ITEMS[item_name]

    if item["type"] == "heal":

        if hero.hp == hero.max_hp:

            print("Your HP is already full!")

            return False

        old_hp = hero.hp

        hero.hp += item["value"]

        if hero.hp > hero.max_hp:

            hero.hp = hero.max_hp

        healed = hero.hp - old_hp

        print(f"You used a {item_name}!")

        print(f"You recovered {healed} HP!")

    hero.inventory.remove(item_name)

    return True


# ==============================
# BATTLE
# ==============================

def battle(hero, enemy):

    # Verifica se o inimigo é um boss

    is_boss = any(
        enemy.name == boss.name
        for boss in BOSSES
    )

    if is_boss:

        print(f"""
========== BOSS BATTLE ==========

A BOSS has appeared!

{enemy.name}!

There is NO ESCAPE.

You must defeat the boss.
""")

    else:

        print(f"""
========== BATTLE ==========

A wild {enemy.name} appeared!
""")

    wait()

    while hero.hp > 0 and enemy.hp > 0:

        if is_boss:

            print(f"""
{hero.name}: {hero.hp}/{hero.max_hp} HP
{enemy.name}: {enemy.hp}/{enemy.max_hp} HP

1 - Attack
2 - Use Item
""")

        else:

            print(f"""
{hero.name}: {hero.hp}/{hero.max_hp} HP
{enemy.name}: {enemy.hp}/{enemy.max_hp} HP

1 - Attack
2 - Run
3 - Use Item
""")

        choice = input("Type here: ")

        # ==============================
        # ATTACK
        # ==============================

        if choice == "1":

            enemy.hp -= hero.damage

            print(f"You dealt {hero.damage} damage!")

            if enemy.hp <= 0:

                enemy.hp = 0

                print(f"You defeated the {enemy.name}!")

                hero.gold += enemy.gold

                print(f"You earned {enemy.gold} Gold!")

                hero.gain_xp(enemy.xp)

                return "victory"

            hero.take_damage(enemy.damage)

            print(
                f"The {enemy.name} dealt "
                f"{enemy.damage} damage!"
            )

        # ==============================
        # RUN - ONLY NORMAL ENEMIES
        # ==============================

        elif choice == "2" and not is_boss:

            print("You ran away!")

            return "run"

        # ==============================
        # USE ITEM - BOSS
        # ==============================

        elif choice == "2" and is_boss:

            if not hero.inventory:

                print("Your inventory is empty!")

                continue

            print("""
========== INVENTORY ==========
""")

            for i, item in enumerate(hero.inventory, 1):

                print(f"{i} - {item}")

            print("0 - Cancel")

            item_choice = input("Choose an item: ")

            if item_choice == "0":

                continue

            if not item_choice.isdigit():

                print("Invalid choice.")

                continue

            item_index = int(item_choice) - 1

            if (
                item_index < 0
                or item_index >= len(hero.inventory)
            ):

                print("Invalid choice.")

                continue

            item_name = hero.inventory[item_index]

            used = use_item(hero, item_name)

            if not used:

                continue

            # Usar item consome o turno

            hero.take_damage(enemy.damage)

            print(
                f"The {enemy.name} dealt "
                f"{enemy.damage} damage!"
            )

        # ==============================
        # USE ITEM - NORMAL ENEMY
        # ==============================

        elif choice == "3":

            if not hero.inventory:

                print("Your inventory is empty!")

                continue

            print("""
========== INVENTORY ==========
""")

            for i, item in enumerate(hero.inventory, 1):

                print(f"{i} - {item}")

            print("0 - Cancel")

            item_choice = input("Choose an item: ")

            if item_choice == "0":

                continue

            if not item_choice.isdigit():

                print("Invalid choice.")

                continue

            item_index = int(item_choice) - 1

            if (
                item_index < 0
                or item_index >= len(hero.inventory)
            ):

                print("Invalid choice.")

                continue

            item_name = hero.inventory[item_index]

            used = use_item(hero, item_name)

            if not used:

                continue

            # Usar item consome o turno

            hero.take_damage(enemy.damage)

            print(
                f"The {enemy.name} dealt "
                f"{enemy.damage} damage!"
            )

        # ==============================
        # INVALID
        # ==============================

        else:

            if is_boss and choice == "2":

                print("You cannot run from a boss!")

            else:

                print("Invalid choice.")

    # ==============================
    # DEATH / PERMADEATH
    # ==============================

    if hero.hp <= 0:

        print("""
========== GAME OVER ==========

You were defeated.

Your run has ended.

PERMADEATH
""")

        return "death"


# ==============================
# NPC EVENT
# ==============================

def npc_event(hero):

    npc = random.choice(NPCS)

    print(f"""
========== NPC ==========

You encountered a {npc["name"]}!

{npc["message"]}
""")

    print(f"You received {npc['reward']} Gold!")

    hero.gold += npc["reward"]

    wait()


# ==============================
# JOURNEY
# ==============================

def journey(hero):

    print("""
========== JOURNEY ==========

You leave the town and begin your journey...
""")

    wait()

    event = random.randint(1, 1000)

    # ==============================
    # SPECIAL EVENT
    # 0.1%
    # ==============================

    if event == 1:

        print("""
========== SPECIAL EVENT ==========

Something extremely rare happened!
""")

        wait()

    # ==============================
    # ENEMY
    # 84.9%
    # ==============================

    elif event <= 850:

        enemy = generate_enemy()

        result = battle(hero, enemy)

        return result

    # ==============================
    # ITEM
    # 5%
    # ==============================

    elif event <= 900:

        item_name = random.choice(list(ITEMS.keys()))

        hero.inventory.append(item_name)

        print("""
========== ITEM ==========

You found an item!
""")

        print(f"You found a {item_name}!")

        wait()

    # ==============================
    # TRAP
    # 5%
    # ==============================

    elif event <= 950:

        print("""
========== TRAP ==========

You fell into a trap!
""")

        damage = hero.hp // 10

        hero.take_damage(damage)

        print(f"You lost {damage} HP!")

        # Verifica morte por armadilha

        if hero.hp <= 0:

            print("""
========== GAME OVER ==========

The trap killed you.

Your run has ended.

PERMADEATH
""")

            return "death"

        wait()

    # ==============================
    # NPC
    # 5%
    # ==============================

    else:

        npc_event(hero)


# ==============================
# STORE
# ==============================

def store(hero):

    while True:

        print(f"""
========== STORE ==========

Gold: {hero.gold}

1 - Weapons
2 - Items
3 - Exit
""")

        choice = input("Type here: ")

        # ==============================
        # WEAPONS
        # ==============================

        if choice == "1":

            print("""
========== WEAPONS ==========
""")

            weapon_names = list(WEAPONS.keys())

            for i, weapon_name in enumerate(weapon_names, 1):

                weapon = WEAPONS[weapon_name]

                print(
                    f"{i} - {weapon_name} | "
                    f"Damage: {weapon['damage']} | "
                    f"Price: {weapon['price']} Gold"
                )

            print("0 - Back")

            weapon_choice = input("Choose a weapon: ")

            if weapon_choice == "0":

                continue

            if not weapon_choice.isdigit():

                print("Invalid choice.")

                continue

            weapon_index = int(weapon_choice) - 1

            if (
                weapon_index < 0
                or weapon_index >= len(weapon_names)
            ):

                print("Invalid choice.")

                continue

            weapon_name = weapon_names[weapon_index]

            weapon = WEAPONS[weapon_name]

            if hero.weapon == weapon_name:

                print("You already have this weapon.")

                continue

            if hero.gold < weapon["price"]:

                print("You don't have enough Gold.")

                continue

            hero.gold -= weapon["price"]

            hero.weapon = weapon_name

            print(f"You bought a {weapon_name}!")

        # ==============================
        # ITEMS
        # ==============================

        elif choice == "2":

            print("""
========== ITEMS ==========
""")

            item_names = list(ITEMS.keys())

            for i, item_name in enumerate(item_names, 1):

                item = ITEMS[item_name]

                print(
                    f"{i} - {item_name} | "
                    f"Price: {item['price']} Gold"
                )

            print("0 - Back")

            item_choice = input("Choose an item: ")

            if item_choice == "0":

                continue

            if not item_choice.isdigit():

                print("Invalid choice.")

                continue

            item_index = int(item_choice) - 1

            if (
                item_index < 0
                or item_index >= len(item_names)
            ):

                print("Invalid choice.")

                continue

            item_name = item_names[item_index]

            item = ITEMS[item_name]

            if hero.gold < item["price"]:

                print("You don't have enough Gold.")

                continue

            hero.gold -= item["price"]

            hero.inventory.append(item_name)

            print(f"You bought a {item_name}!")

        # ==============================
        # EXIT
        # ==============================

        elif choice == "3":

            print("You left the store.")

            return

        # ==============================
        # INVALID
        # ==============================

        else:

            print("Invalid choice.")


# ==============================
# MENU
# ==============================

def menu(hero):

    while True:

        print(f"""
========== ARENA ==========

Gold: {hero.gold}
HP: {hero.hp}/{hero.max_hp}

1 - Journey
2 - Character
3 - Inventory
4 - Store
5 - Exit
""")

        choice = input("Type here: ")

        # ==============================
        # JOURNEY
        # ==============================

        if choice == "1":

            result = journey(hero)

            # ==============================
            # PERMADEATH
            # ==============================

            if result == "death":

                print("""
================================

Your character is gone.

Everything from this run
has been lost.

================================
""")

                return "death"

        # ==============================
        # CHARACTER
        # ==============================

        elif choice == "2":

            character(hero)

        # ==============================
        # INVENTORY
        # ==============================

        elif choice == "3":

            inventory(hero)

        # ==============================
        # STORE
        # ==============================

        elif choice == "4":

            store(hero)

        # ==============================
        # EXIT
        # ==============================

        elif choice == "5":

            print("""
========== EXIT ==========

Thanks for playing ARENA!
""")

            return "exit"

        # ==============================
        # INVALID
        # ==============================

        else:

            print("Invalid choice.")


# ==============================
# MAIN
# ==============================

def main():

    global enemy_count

    print("""
========== ARENA ==========

Welcome to ARENA!
""")

    while True:

        # Cada nova run começa do zero

        enemy_count = 0

        name = input("Enter your name: ")

        hero = Hero(name)

        print(f"""
Welcome, {hero.name}!

Your adventure begins...
""")

        wait()

        result = menu(hero)

        # ==============================
        # PERMADEATH
        # ==============================

        if result == "death":

            print("""
========== NEW RUN ==========

Your previous character is dead.

A new adventure begins...
""")

            wait()

            continue

        # ==============================
        # NORMAL EXIT
        # ==============================

        if result == "exit":

            break


# ==============================
# START GAME
# ==============================

main()
