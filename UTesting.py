import unittest
import UI

class Test(unittest.TestCase):

    def tGetIndex(self):
        self.assertEqual(UI.getIndex("123:This is a test"),122)
        self.assertEqual(UI.getIndex("1:This is a test"),17)

if __name__ == "__main__":
    unittest.main()