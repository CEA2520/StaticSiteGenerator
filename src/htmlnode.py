class HTMLNode:

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        # Child classes will override
        raise NotImplementedError

    def props_to_html(self):
        # First, check if we have any props
        if self.props is None:
            return ""
    
        # Create an empty list to store our formatted strings
        prop_list = []
    
        for key, value in self.props.items():
            # Format each prop and add to list
            formatted_prop ='{}="{}"'.format(key, value)
            prop_list.append(formatted_prop)
    
        # Join all props with spaces and add leading space unless empty then return no space
        return " " + " ".join(prop_list) if prop_list else ""

    def __repr__(self):
        # Useful for debugging
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

class LeafNode(HTMLNode):

    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value == None:
            raise ValueError
        if self.tag == None:
            return f"{self.value}"
 
        # Get the props string using the parent class's method
        props_string = self.props_to_html()
    
        return f"<{self.tag}{props_string}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Invalid HTML: no tag")
        if self.children is None or self.children == []:
            raise ValueError("Invalid HTML: no children")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"

    