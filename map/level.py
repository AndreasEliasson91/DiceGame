import random

from assets.actors.enemy import Enemy
from assets.battle import Battle
from assets.item import Item
from data.enemy_data import enemies
from data.item_data import key_items, usable_items
from map.maze import Maze


def print_player_location_in_maze(game):
    """
    Debug function to see the players position
    The map is dynamic and changes for every run, which makes this very handy!
    """
    print('X Y')
    print(*game.player.get_actor_position())


class Level:
    def __init__(self, level: int, maze_size: tuple, player):
        self.battle = None
        self.level_complete = False
        self.enemies = {Enemy(level, **random.choice(enemies)) for _ in range(maze_size[0])}
        self.maze = Maze(*maze_size, self.item_generator(), self.enemies)
        self.player = player

    def run(self):
        while not self.level_complete and self.player.alive:
            self.print_maze_info()
            print_player_location_in_maze(self)
            self.process_user_input()

    @staticmethod
    def item_generator():
        items = [Item(**item) for item in usable_items]
        level_items = {random.choice(items) for _ in range(0)}
        level_items.update({Item(**item) for item in key_items})
        return level_items

    def process_user_input(self):
        """Process the user input, and through a matching pattern decide what method(s) to call"""
        command = input('>> ')
        current_location = self.maze.get_cell(*self.player.get_actor_position())

        match command.lower().split():
            case ['go', direction] if direction in current_location.walls and not current_location.walls[direction]:
                print('You go further in the maze!\n')
                self.player.go(direction)
                # self.engaged_in_battle(direction)
            case ['go', *bad_direction]:
                print(f'You can\'t go in that direction: {" ".join(bad_direction)}')

            case ['get', item]:
                self.player.pick_up_item(item, current_location)
            case ['drop', item]:
                self.player.drop_item(item, current_location)
            case ['check', item]:
                if current_location.item and 'check' in current_location.item.__dict__['actions']:
                    print(f'You pick up and look at the {item}\n'
                          f'It\'s a {current_location.item.__dict__["description"]}')
                else:
                    print(f'You can\'t check that out.')
            case ['investigate', item]:
                print(f'{self.investigate_item(item)}')

            case ['open', item]:
                if not current_location.item or current_location.item.__dict__['label'] != item:
                    print('There is nothing to open here!')
                elif item == current_location.item.__dict__['label']:
                    if self.player.inventory.item_in_inventory(current_location.item.__dict__['requirements']):
                        match item:
                            case 'chest':
                                self.open_chest(current_location.item)
                            case 'door':
                                print('You open the door and move to the next area!')
                                self.level_complete = True
                            case _:
                                print(f'I can\'t understand "open {item}"')
                    else:
                        print(f'The {item} is locked, you need something to unlock it with!')
                else:
                    print(f'I can\'t understand "open {item}"')

            case ['inventory']:
                self.player.inventory.print_inventory()

            case _:
                print(f'I don\'t understand {command}...')

    def open_chest(self, chest):
        if chest.__dict__['label'] == 'chest':
            chest.__dict__['open'] = True
            print(f'The {chest.__dict__["description"]} is open and contains the following: ')
            for i in chest.__dict__['contains']:
                print(f'* {i.__dict__["description"]}')

        while chest.__dict__['open']:
            command = input('>> ')
            match command.lower().split():
                case ['get', item]:
                    self.player.pick_up_item(item, self.maze.get_cell(*self.player.get_actor_position()), chest)
                case ['close'] | ['close', 'chest']:
                    print(f'You close the {chest.__dict__["description"]}')
                    chest.__dict__['open'] = False
                case _:
                    print(f'I don\'t understand {command}...')

    def investigate_item(self, label: str) -> str:
        if self.maze.get_cell(*self.player.get_actor_position()).got_item:
            item = self.maze.get_cell(*self.player.get_actor_position()).item
            if label == item.__dict__['label'] and 'investigate' in item.__dict__['actions']:
                return item.__dict__['bonus']
            elif 'investigate' not in item.__dict__['actions']:
                return f'Can\'t investigate {item.__dict__["description"]} further!'
            elif self.maze.get_cell(*self.player.get_actor_position()).got_item and label != item.__dict__['label']:
                return f'There is no {label} here, but something else!'
        else:
            return 'There is nothing to investigate here!'

    def engaged_in_battle(self, direction: str):
        """
        Check if the player is engaged in battle after it's movement. Aka is there an enemy in the new cell
        :param direction: The direction which the player came from
        """
        if self.maze.get_cell(*self.player.get_actor_position()).enemy:
            print(f'You bumped into a {self.maze.get_cell(*self.player.get_actor_position()).enemy.get_actor_name()}'
                  f'\nPREPARE TO FIGHT!')
            self.battle = Battle(self.maze.get_cell(*self.player.get_actor_position()), direction, self.player)

    def print_maze_info(self):
        if self.player.inventory.item_in_inventory('lantern'):
            print('You\'ve got the lantern. It lights up your surroundings.\nYou can go: ')
            for direction in self.maze.get_cell(*self.player.get_actor_position()).walls:
                if not self.maze.get_cell(*self.player.get_actor_position()).walls[direction]:
                    print(f'* {direction}')
            if self.maze.get_cell(*self.player.get_actor_position()).got_item:
                print(f'There is a {self.maze.get_cell(*self.player.get_actor_position()).item.__dict__["description"]} here')
        else:
            print('You\'re in a dark space.')
            if self.maze.get_cell(*self.player.get_actor_position()).got_item:
                print(f'There is something in this room, maybe check it out?')
