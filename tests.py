import unittest
import importerTest


importerTests = unittest.TestLoader().loadTestsFromTestCase(importerTest.ImporterTest)
unittest.TextTestRunner(verbosity=2).run(importerTests)
