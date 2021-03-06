import unittest
from unittest.mock import patch

from src.assets import Enemy
from src.assets import Player
from src.assets import Battle
from src.db.data import enemies
from src.assets.game.level import Level


class TestBattle(unittest.TestCase):
    @patch('builtins.input', return_value='roll')
    def test_two_handed_sword(self, input):
        player = Player()

        level = Level(1, (5, 5), player)
        level.maze.get_cell(*player.get_actor_position())\
            .set_enemy([Enemy(1, **enemy) for enemy in enemies if enemy['name'] == 'skeleton'])

        level.battle = Battle(level.maze.get_cell(*player.get_actor_position()), 'east', player)
        while player.alive and level.maze.get_cell(*player.get_actor_position()).enemy:
            level.battle.battle(level.maze.get_cell(*player.get_actor_position()), 'east', player)

        self.assertFalse(level.battle.in_battle)


if __name__ == '__main__':
    unittest.main()
