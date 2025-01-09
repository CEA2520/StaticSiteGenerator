import unittest
from textnode import TextNode, TextType
from text_splitter import split_nodes_delimiter

class TestSplitter(unittest.TestCase):
    def test_split_nodes_delimiter_basic(self):
        node = TextNode("Hello `world` there", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        assert len(nodes) == 3
        assert nodes[0].text == "Hello "
        assert nodes[0].text_type == TextType.TEXT
        assert nodes[1].text == "world"
        assert nodes[1].text_type == TextType.CODE
        assert nodes[2].text == " there"
        assert nodes[2].text_type == TextType.TEXT

    def test_split_nodes_delimiter_multiple(self):
        node = TextNode("**bold** not bold **bold again**", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        assert len(nodes) == 3
        assert nodes[0].text == "bold"
        assert nodes[0].text_type == TextType.BOLD
        assert nodes[1].text == " not bold "
        assert nodes[1].text_type == TextType.TEXT
        assert nodes[2].text == "bold again"
        assert nodes[2].text_type == TextType.BOLD

    def test_split_nodes_delimiter_no_delimiters(self):
        node = TextNode("Hello world", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        assert len(nodes) == 1
        assert nodes[0].text == "Hello world"
        assert nodes[0].text_type == TextType.TEXT

    def test_split_nodes_delimiter_skip_non_text(self):
        node = TextNode("Hello world", TextType.CODE)
        nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        assert len(nodes)