import unittest
import hexagon as h 

class TestHexagonMethods(unittest.TestCase):
    def setUp(self):
        """ sets up initial environment for testing """ 
        self.a = h.hexagon("a")
        self.b = h.hexagon("b")
        self.c = h.hexagon("c")
        h.hexagons["a"] = self.a
        h.hexagons["b"] = self.b
        h.hexagons["c"] = self.c

    def test_single_add(self):
        """ tests if a singular addition will work """ 
        self.b.add_neighbour(5, self.a)
        self.assertEqual(self.b.query(), [(5, "a")])
        self.assertEqual(self.a.query(), [(2, "b")])

    def test_multiple_add(self):
        """ test if multiple addition will work - ie, if a hexagon will update itself when an adjacent neighbour is added indirectly """ 
        self.b.add_neighbour(4, self.c)
        self.b.add_neighbour(5, self.a)
        self.assertEqual(self.b.query(), [(4, "c"), (5, "a")])
        self.assertEqual(self.b.query(), [(4, "c"), (5, "a")])
        self.assertEqual(self.a.query(), [(2, "b"), (3, "c")])
        self.assertEqual(self.c.query(), [(0, "a"), (1, "b")])

    def test_valid_remove(self):
        """ tests if a hexagon can be removed. b is invalid as it borders a, c. a is valid as it is not a chokepoint """ 
        self.b.add_neighbour(5, self.a)
        self.b.add_neighbour(1, self.c)
        self.assertFalse(h.valid_remove(self.b))
        self.assertTrue(h.valid_remove(self.a))
    
    def test_rotate(self):
        """ tests rotation to see if path to traverse is correct """ 
        arr = [0,1,2,3,4,5]
        new = h.rotate(arr, 3)
        self.assertEqual(new, [5, 0, 1, 2, 3, 4])
    
    def test_remove(self):
        """ tests removal of a single, isolated hexagon """
        h.remove("a")
        self.assertEqual(list(h.hexagons.keys()), ["b", "c"])

    def test_connected_remove(self):
        """ tests removal functionality - b should not be removed as it is connecting a/c; a can be removed """ 
        self.b.add_neighbour(4, self.c)
        self.b.add_neighbour(1, self.a)
        h.remove("b")
        self.assertEqual(list(h.hexagons.keys()), ["a", "b", "c"])
        h.remove("a")
        self.assertEqual(list(h.hexagons.keys()), ["b", "c"])
        self.assertEqual(self.b.query(), [(4, "c")])
        self.assertEqual(self.c.query(), [(1, "b")])

if __name__ == '__main__':
    unittest.main()