from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK =  "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
        self.text == other.text and 
        self.text_type == other.text_type and 
        self.url == other.url
    )
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

#convert text node to html node
def text_node_to_html_node(text_node):
    
    #This should become a LeafNode with no tag, just a raw text value.
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)

    #This should become a LeafNode with a "b" tag and the text
    if text_node.text_type == TextType.BOLD: 
        return LeafNode("b", text_node.text)

    # "i" tag, text
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)

    # "code" tag, text
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text) 

    #"a" tag, anchor text, and "href" prop
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})

    #"img" tag, empty string value, "src" and "alt" props ("src" is the image URL, "alt" is the alt text)
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text}) 
 
    raise Exception("unknown text type")