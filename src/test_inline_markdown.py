import unittest
from textnode import TextNode, TextType
from inline_markdown import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    extract_markdown_links,
    extract_markdown_images,
)

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

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()