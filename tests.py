import unittest
from functions import get_files_info as g

class TestGetFiles(unittest.TestCase):

    def test_get_files_info(self):
        # Test cases for the get_files_info function
        self.assertEqual(
            g.get_files_info("calculator", "."), 
            "- pkg: file_size=4096 bytes, is_dir=True\n- main.py: file_size=564 bytes, is_dir=False\n- tests.py: file_size=1330 bytes, is_dir=False\n"
        )
        print(g.get_files_info("calculator", "."))
        self.assertEqual(
            g.get_files_info("calculator", "pkg"), 
            "- calculator.py: file_size=1720 bytes, is_dir=False\n- render.py: file_size=753 bytes, is_dir=False\n- __pycache__: file_size=4096 bytes, is_dir=True\n"
        )
        print(g.get_files_info("calculator", "pkg"))
        self.assertEqual(
            g.get_files_info("calculator", "/bin"), 
            'Error: Cannot list "/bin" as it is outside the permitted working directory'
        )
        print(g.get_files_info("calculator", "/bin"))
        self.assertEqual(
            g.get_files_info("calculator", "../"), 
            'Error: Cannot list "../" as it is outside the permitted working directory'
        )
        print(g.get_files_info("calculator", "../"))

if __name__ == "__main__":
    unittest.main()    