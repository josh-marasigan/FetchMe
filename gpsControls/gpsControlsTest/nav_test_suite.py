import unittest
#import from parent directory
#import gps_module
import direction as Nav

class TestStringMethods(unittest.TestCase):

    # Test turn radius
    def test_turn(self):
        turnRad = Nav.get_angle(170,180)
        print (turnRad)
        
        bearng = Nav.bearings(turnRad)
        print (bearng)
    
    # Test obstruction avoidance algorithm
    def test_avoidance(self):
        Nav.obsBL = False
        Nav.obsBR = False
        '''
        correct_movements = ['SW', 'N']
        Nav.obsR = False
        Nav.obsL = True
        Nav.obsC = True
        actual_movements = Nav.avoid_obstruction()
        
        # Verify correct movements
        count = 0
        for e in correct_movements:
            self.assertEqual(actual_movements[count], e)
            count = count + 1
        
        correct_movements = ['SE', 'N']
        Nav.obsR = True
        Nav.obsL = False
        Nav.obsC = True
        actual_movements = Nav.avoid_obstruction()
        
        # Verify correct movements
        count = 0
        for e in correct_movements:
            self.assertEqual(actual_movements[count], e)
            count = count + 1
        
        
        correct_movements = ['None']
        Nav.obsR = True
        Nav.obsL = True
        Nav.obsC = True
        actual_movements = Nav.avoid_obstruction()
        
        # Verify correct movements
        count = 0
        for e in correct_movements:
            self.assertEqual(actual_movements[count], e)
            count = count + 1
        '''

    def test_in_radius(self):
        
        yes = Nav.inRadius((30.173359,-97.442115),(30.173266,-97.442186))
        print yes
        self.assertTrue(yes)
        
        route = [(30.284743, -97.736801),(30.284591, -97.737299),(30.284100, -97.737347),(30.283469, -97.737409),(30.282684, -97.737479)]
        route1 = [(30.284731, -97.736803),(30.284583, -97.737303),(30.284102, -97.737354),(30.283469, -97.737418),(30.282683, -97.737472)]
        #route1 is actual gps coordinates
        for index in range(0, 5):
            isInRadius = Nav.inRadius(route[index], route1[index])
            lon1 = route[index][0]
            lat1 = route[index][1]
            lon2 = route1[index][0]
            lat2 = route1[index][1]
            #print "TEST 1: ",Nav.haversine(lon1, lat1, lon2, lat2)
            #print isInRadius
            self.assertTrue(isInRadius)
        
        #Opposite directions. Must return false
        route2 = route[::-1]
        route2[2] = (30.284731, -97.736803)
        
        for i in range(0, 5):
            isInRadius = Nav.inRadius(route[i], route2[i])
            lon1 = route[i][0]
            lat1 = route[i][1]
            lon2 = route2[i][0]
            lat2 = route2[i][1]
            #print "Test 2: ",Nav.haversine(lon1, lat1, lon2, lat2)
            #print lon1, lat1, lon2, lat2
            #print isInRadius
            self.assertFalse(isInRadius)
        

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