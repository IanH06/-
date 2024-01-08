import unittest
import NEA

class Test(unittest.TestCase):

    def tGetIndex(self):
        self.assertEqual(NEA.getIndex("123:This is a test"),122)
        self.assertEqual(NEA.getIndex("1:This is a test"),17)

if __name__ == "__main__":
    unittest.main()