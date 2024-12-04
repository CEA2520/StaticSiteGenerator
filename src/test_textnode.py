import unittest

from textnode import *
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq_1(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_2(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node, node2)

    def test_eq_3(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(node, node2)
    
    def test_eq_4(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node, node2)

    def test_not_eq_1(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)
    
    def test_not_eq_2(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)
    
    def test_not_eq_3(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
 
    def test_not_eq_4(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD, "this is a test URL")
        self.assertNotEqual(node, node2)

class TestTextNodeConversion(unittest.TestCase):
    #Test that a TextNode of type TEXT returns a LeafNode with no tag and the same text.
    def test_normal_text_conversion(self):
        # Assuming TextNode and LeafNode are already defined
        text_node = TextNode(text_type=TextType.TEXT, text="Hello, World!")

        # Convert the text node to a leaf node
        result = text_node_to_html_node(text_node)

        # Check that the result is a LeafNode with no tag and the correct text
        self.assertIsInstance(result, LeafNode)
        self.assertIsNone(result.tag)
        self.assertEqual(result.value, "Hello, World!")

    #Test that a TextNode of type BOLD returns a LeafNode with a "b" tag and the same text.
    def test_bold_text_coversion(self):
        # Assuming TextNode and LeafNode are already defined
        text_node = TextNode(text_type=TextType.BOLD, text="Hello, World!")

        # Convert the text node to a leaf node
        result = text_node_to_html_node(text_node)

        # Check that the result is a LeafNode with proper tag and the correct text
        self.assertIsInstance(result, LeafNode)
        self.assertEqual(result.tag, "b")
        self.assertEqual(result.value, "Hello, World!")


    #Test that a TextNode of type ITALIC returns a LeafNode with a "i" tag and the same text.
    def test_italic_text_coversion(self):
         # Assuming TextNode and LeafNode are already defined
        text_node = TextNode(text_type=TextType.ITALIC, text="Hello, World!")

        # Convert the text node to a leaf node
        result = text_node_to_html_node(text_node)

        # Check that the result is a LeafNode with proper tag and the correct text
        self.assertIsInstance(result, LeafNode)
        self.assertEqual(result.tag, "i")
        self.assertEqual(result.value, "Hello, World!")

    #Test that a TextNode of type CODE returns a LeafNode with a "code" tag and the same text.
    def test_code_text_coversion(self):
         # Assuming TextNode and LeafNode are already defined
        text_node = TextNode(text_type=TextType.CODE, text="Hello, World!")

        # Convert the text node to a leaf node
        result = text_node_to_html_node(text_node)

        # Check that the result is a LeafNode with proper tag and the correct text
        self.assertIsInstance(result, LeafNode)
        self.assertEqual(result.tag, "code")
        self.assertEqual(result.value, "Hello, World!")

    #Test a TextNode of type LINK and ensure that the LeafNode has an "a" tag, appropriate text, and the href attribute correctly set.
    def test_link_text_coversion(self):
         # Assuming TextNode and LeafNode are already defined
        text_node = TextNode(text_type=TextType.LINK, text="Hello, World!")

        # Convert the text node to a leaf node
        result = text_node_to_html_node(text_node)

        # Check that the result is a LeafNode with proper tag and the correct text
        self.assertIsInstance(result, LeafNode)
        self.assertEqual(result.tag, "a")
        self.assertEqual(result.value, "Hello, World!")
        self.assertIn("href", result.props)
        self.assertEqual(result.props["href"], text_node.url)

    #Test an IMAGE type TextNode to see if a LeafNode is created with img tag, an empty string as value, and src and alt properties populated correctly.
    def test_img_text_coversion(self):
         # Assuming TextNode and LeafNode are already defined
        text_node = TextNode(text_type=TextType.IMAGE, text="Hello, World!")

        # Convert the text node to a leaf node
        result = text_node_to_html_node(text_node)

        # Check that the result is a LeafNode with proper tag and the correct text
        self.assertIsInstance(result, LeafNode)
        self.assertEqual(result.tag, "img")
        self.assertEqual(result.value, "")
        self.assertIn("src", result.props)
        self.assertEqual(result.props["src"], text_node.url)
        self.assertIn("alt", result.props)
        self.assertEqual(result.props["alt"], text_node.text)

    # Pass a TextNode with an unhandled text_type and assert that the function raises an exception
    def test_unknown_type_text_conversion(self):
        #Assuming TextNode is already defined
        text_node = TextNode(text_type="UNKNOWN", text="Hello, World!")

        #Assert that calling the function with this text_node raises an exception
        with self.assertRaises(Exception) as context:
            text_node_to_html_node(text_node)

        #Check the exception message
        self.assertEqual(str(context.exception), "unknown text type")

if __name__ == "__main__":
    unittest.main()