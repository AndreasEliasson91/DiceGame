import random
import colorama
from assets.actors.actor import Actor
from assets.inventory import Inventory
from map.maze import DIRECTIONS


class Player(Actor):
    def __init__(self):
        super().__init__('player', (4, 4), 0, 0, 10, 1)
        self.inventory = Inventory()
        self.alive = True

    def go(self, direction: str):
        """Update player position, based on a constant value from DIRECTIONS"""
        for value in DIRECTIONS:
            if value[0] == direction:
                self.set_actor_position(value[1])

    def pick_up_item(self, label: str, current_location, chest=None):
        """
        Pick up an item from the current location, or from a chest, and append it to the players inventory
        :param label: The item to get
        :param current_location: The players current location
        :param chest: Chest to get item from, None as default
        """
        if chest:
            for item in chest.__dict__['contains']:
                if label == item.__dict__['label']:
                    self.inventory.process_item_pickup(item, current_location, chest)
                else:
                    print(f'There is no {colorama.Fore.RED}{label}{colorama.Style.RESET_ALL} in the chest')

        elif not current_location.item or label != current_location.item.__dict__['label']:
            print(f'There is no {label} here')

        elif label == current_location.item.__dict__['label']:
            self.inventory.process_item_pickup(current_location.item, current_location)

    def drop_item(self, label: str, current_location):
        """
        Drop an item from the players inventory
        :param label: The label of the item to drop
        :param current_location: The players current location
        """
        found_item = None
        if not current_location.got_item:
            for item in self.inventory.pouch:
                if label == item.__dict__['label']:
                    found_item = item
                    break
        else:
            print(f'This space isn\'t empty! You can\'t drop the {label}')

        if found_item and 'drop' in found_item.__dict__['actions']:
            print(f'You drop the {label}')
            self.inventory.pouch.remove(found_item)
            current_location.item = found_item
            current_location.got_item = True
        else:
            print(f'You can\'t drop the {label}, you should have thought of this earlier')

    def use_battle_item(self, label: str, enemy):
        if self.inventory.item_in_inventory(label):
            match label:
                case 'potion':
                    print(f'You drank the health potion and gained 10 health points!')
                    self.health_points += 10
                    self.inventory.remove_pouch_item(label)

                case 'pill':
                    effect = random.choice(['cursed', 'lucky'])
                    print(f'You consume the dark pill and you\'re {effect}!')

                    match effect:
                        case 'lucky':
                            print('You gain 15 health points!')
                            self.health_points += 15
                        case 'cursed':
                            print(f'You faint for a moment and the {enemy.get_actor_name()} takes advantage!\n'
                                  f'You lose {enemy.attack_points} health points!')
                            self.health_points -= enemy.attack_points

    def reset_player_stats(self):
        self.set_actor_position((0, 0))
        self.inventory = Inventory()
        self.level += 1
