import unittest
import filehandlers
import os


class Tests(unittest.TestCase):
    def setUp(self):
        os.remove("test.txt")
        self.af = filehandlers.AbstractFile("test.txt")
        self.m = filehandlers.FileManipulator(self.af)
        self.af.touch()

    def test_file_naming(self):
        self.assertEqual(str(self.af), "test.txt")

    def test_file_exists(self):
        self.assertTrue(self.af.exists())

    def test_writing_to_files(self):
        self.assertTrue(self.af.exists())
        b = self.af.wrap()
        self.assertEqual(b.read(), "")
        b.close()  # to fix resourcewarning
        self.assertEqual(self.m.get_cache(), [])
        self.m.write_to_file("cool\nthings")
        self.m.refresh()
        self.assertEqual(self.m.get_cache(), ["cool", "things"])


if __name__ == "__main__":
    unittest.main()
