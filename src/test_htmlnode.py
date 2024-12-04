import unittest

from htmlnode import *

class TestHTMLNode(unittest.TestCase):

    #test html node
    def test_props_to_html_no_props(self):
        # What should happen when props is None?
        node = HTMLNode(props=None)
        assert node.props_to_html() == ""

    def test_props_to_html_one_prop(self):
        # What should happen with one property?
        node = HTMLNode(props={"href": "https://test.com"})
        assert node.props_to_html() == ' href="https://test.com"'

    def test_props_to_html_multiple_props(self):
        # What should happen with multiple properties?
        node = HTMLNode(props={"href": "https://test.com", "target": "test"})
        assert node.props_to_html() == ' href="https://test.com" target="test"'

    def test_props_to_html_empty_dict(self):
        # What happens when the dictionary is empty?
        node = HTMLNode(props={})
        assert node.props_to_html() == ""

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    #test leaf node
    #A tag with no properties
    def test_to_html_no_properties(self):
        node = LeafNode(tag="a", value = "test value", props=None)
        assert node.to_html() == "<a>test value</a>"

    #A tag with one property
    def test_to_html_one_property(self):
        node = LeafNode(tag="a", value = "test value", props={"href": "https://test.com"})
        assert node.to_html() == '<a href="https://test.com">test value</a>'


    #A tag with multiple properties
    def test_to_html_multiple_properties(self):
        node = LeafNode(tag="a", value = "test value", props={"href": "https://test.com", "target": "test"})
        assert node.to_html() == '<a href="https://test.com" target="test">test value</a>'

    #A tag with no tag (just text)
    def test_to_html_no_tag(self):
        node = LeafNode(value="test value", props={"href": "https://test.com"})
        assert node.to_html() == "test value"

    #A tag with no value (should raise ValueError)
    def test_to_html_no_value(self):
        with self.assertRaises(ValueError):
            node = LeafNode(tag="a", props={"href": "https://test.com"})
            node.to_html()

    #test parent node
    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )


if __name__ == "__main__":
    unittest.main()
