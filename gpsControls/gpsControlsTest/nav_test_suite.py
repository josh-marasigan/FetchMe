import unittest
#import from parent directory
#import gps_module
import direction as Nav

class TestStringMethods(unittest.TestCase):

    # Test obstruction avoidance algorithm
    def test_avoidance(self):
        Nav.obsBL = False
        Nav.obsBR = False
        
        correct_movements = ['SW', 'N']
        Nav.obsR = False
        Nav.obsL = True
        Nav.obsC = True
        actual_movements = Nav.avoid_obstruction_T(True)
        
        # Verify correct movements
        count = 0
        for e in correct_movements:
            self.assertEqual(actual_movements[count], e)
            count = count + 1
        
        correct_movements = ['SE', 'N']
        Nav.obsR = True
        Nav.obsL = False
        Nav.obsC = True
        actual_movements = Nav.avoid_obstruction_T(True)
        
        # Verify correct movements
        count = 0
        for e in correct_movements:
            self.assertEqual(actual_movements[count], e)
            count = count + 1
        
        
        correct_movements = ['None']
        Nav.obsR = True
        Nav.obsL = True
        Nav.obsC = True
        actual_movements = Nav.avoid_obstruction_T(True)
        
        # Verify correct movements
        count = 0
        for e in correct_movements:
            self.assertEqual(actual_movements[count], e)
            count = count + 1

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()