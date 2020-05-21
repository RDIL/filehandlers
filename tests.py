import unittest
import filehandlers
import textwrap
import os


class Tests(unittest.TestCase):
    """The tests."""

    def setUp(self):
        """Sets up for the tests."""
        self.af = filehandlers.AbstractFile("test.txt")
        self.m = filehandlers.FileManipulator(self.af)
        self.af.touch()

    def tearDown(self):
        """Clears away old stuff after the tests."""
        self.m.delete()

    def test_file_naming(self):
        """Test that the file is named the correct thing."""
        self.assertEqual(str(self.af), "test.txt")

    def test_file_exists(self):
        """Test that the file exists."""
        self.assertTrue(self.af.exists())

    def test_writing_to_files(self):
        """Test that we can write to files."""
        self.assertTrue(self.af.exists())
        b = open(str(self.af), mode=filehandlers.OpenModes.READ.value)
        self.assertEqual(b.read(), "")
        b.close()  # to fix resourcewarning
        self.assertEqual(self.m.get_cache(), [])
        self.m.write_to_file("cool\nthings")
        self.m.refresh()
        self.assertEqual(self.m.get_cache(), ["cool", "things"])
        self.assertEqual(
            self.m.get_file_contents_singlestring(),
            textwrap.dedent(
                """\
                    cool
                    things"""  # noqa
            ),  # noqa
        )

    @unittest.skipUnless(os.getenv("CIRRUS_CI") is not None, reason="not CI")
    def test_abspath(self):
        """Test that the absolute path of the file is correct if in CI."""
        self.assertEqual(abs(self.af), "/tmp/cirrus-ci-build/test.txt")

    def test_semistrict_types(self):
        """Test that FileManipulators can only be created with AbstractFiles."""
        with self.assertRaises(TypeError):
            filehandlers.FileManipulator(0)  # wrong type on purpose

    @unittest.skipUnless(os.getenv("CIRRUS_CI") is not None, reason="not CI")
    def test_parent_directory(self):
        """Test the AbstractFile.parent_directory function."""
        self.assertEqual(self.af.parent_directory(), "/tmp/cirrus-ci-build")


if __name__ == "__main__":
    unittest.main()
