
import unittest

from s_tool.parser import LxmlParser


class LxmlParserTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = LxmlParser()

    def test_dropdown(self):
        html_string = """
            <html>
                <body>
                    <select>
                        <option value="1">Option 1</option>
                        <option value="2">Option 2</option>
                        <option value="3">Option 3</option>
                    </select>
                </body>
            </html>"""
        
        expected_result = [('Option 1', '1'), ('Option 2', '2'), ('Option 3', '3')]
        dropdown_options = self.parser.dropdown(html_string)

        self.assertEqual(expected_result,dropdown_options)
        self.assertTrue(len(dropdown_options)==3)
        
