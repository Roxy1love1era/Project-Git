import unittest
from FG_model import *


class LandTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(LandTest, self).__init__(*args, **kwargs)
        self.my_land = Land(0, 0)

    def test_cycle(self):
        self.assertFalse(self.my_land.isClaimed)
        self.assertFalse(self.my_land.isMowed)
        self.assertFalse(self.my_land.isWet)
        self.assertEqual(self.my_land.seed, ['', 0])
        self.my_land.claim()
        self.assertTrue(self.my_land.isClaimed)
        self.my_land.mow()
        self.assertTrue(self.my_land.isMowed)
        self.my_land.water()
        self.assertTrue(self.my_land.isWet)
        self.my_land.plant('Carrot')
        self.assertEqual(self.my_land.seed, ['Carrot', 0])
        self.my_land.grow(3)
        self.assertEqual(self.my_land.seed, ['Carrot', 3 * 1.5])  # wet is grow * 1.5
        self.my_land.plant('')
        self.assertEqual(self.my_land.seed, ['', 0])

    def test_un_claim(self):
        self.my_land.__init__()
        self.my_land.mow()
        self.my_land.water()
        self.my_land.plant('Wheat')
        self.my_land.grow()
        self.assertFalse(self.my_land.isMowed)
        self.assertFalse(self.my_land.isWet)
        self.assertEqual(self.my_land.seed, ['', 0])

    def test_un_mowed(self):
        self.my_land.__init__()
        self.my_land.claim()
        self.my_land.plant('Potato')
        self.my_land.grow()
        self.assertEqual(self.my_land.seed, ['', 0, 0])

    def test_no_seed(self):
        self.my_land.__init__()
        self.my_land.claim()
        self.my_land.grow()
        self.assertEqual(self.my_land.seed, ['', 0])


if __name__ == '__main__':
    unittest.main()


class GameTest(unittest.TestCase):
    def test_land_access(self):
        my_game = Game(3, 3)
        self.assertFalse(my_game.land(2, 2).isMowed())