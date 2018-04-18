import unittest
import test.test_basic

def run():
    suite = unittest.TestLoader().loadTestsFromModule(test.test_basic)
    unittest.TextTestRunner(verbosity=3).run(suite)

if __name__ == '__main__':
    run()