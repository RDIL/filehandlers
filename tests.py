import unittest
import filehandlers
import os


class Tests(unittest.TestCase):
    def test_file_naming(self):
        self.assertEqual(str(filehandlers.AbstractFile("file.txt")), "file.txt")

    def test_file_creation_and_exists(self):
        af = filehandlers.AbstractFile("test.txt")
        self.assertFalse(af.exists())
        af.touch()
        self.assertTrue(af.exists())
        os.remove(str(af))

    def test_writing_to_files(self):
        af = filehandlers.AbstractFile("test.txt")
        m = filehandlers.FileManipulator(af)
        self.assertFalse(af.exists())
        af.touch()
        self.assertTrue(af.exists())
        self.assertEqual(af.wrap().read(), "")
        self.assertEqual(m.get_cache(), [])
        m.write_to_file("cool\nthings")
        m.refresh()
        self.assertEqual(af.wrap().read(), "cool\nthings")
        self.assertEqual(m.get_cache(), ["cool", "things"])
        os.remove(str(af))


if __name__ == "__main__":
    unittest.main()
