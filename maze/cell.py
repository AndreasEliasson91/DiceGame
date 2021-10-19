from data.item_data import key_items, environment_items


class Cell:

    WALL_SEPARATES = {
        'north': 'south',
        'south': 'north',
        'east': 'west',
        'west': 'east'
    }

    def __init__(self, x, y):
        """:param x: Cell X-coordinate  :param y: Cell Y-coordinate"""
        self.x, self.y = x, y
        self.walls = {
            'north': True,
            'south': True,
            'east': True,
            'west': True
        }
        self.got_item = False
        self.item = {}

    def surrounded_by_walls(self) -> bool:
        return all(self.walls.values())

    def remove_wall(self, other_cell, wall):
        """
        Remove the wall between two cells
        :param other_cell: The wall between this cell and self will be removed
        :param wall: The wall direction to remove
        """
        self.walls[wall] = False
        other_cell.walls[Cell.WALL_SEPARATES[wall]] = False

    def set_item(self):
        """Set item to the cell with the same position, based on usable_items dict"""
        for item in key_items:
            if item['position'] == (self.x, self.y):
                self.item = item
                self.got_item = True

        for item in environment_items:
            if item['position'] == (self.x, self.y):
                self.item = item
                self.got_item = True
