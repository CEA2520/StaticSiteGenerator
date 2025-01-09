import re

from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    # Initialize empty result list
    new_nodes = []
    
    # For each node in old_nodes:
        # If node is not TEXT type:
            # Add it to result list unchanged
            # Continue to next node
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        
        # If node is TEXT type:
            # Get the text content
            # Look for pairs of delimiters
            # If no matching delimiter found:
                # Raise exception    
        text = node.text
        # Keep processing the text as long as we find delimiters
        while True:
            first_delimiter = text.find(delimiter)
            if first_delimiter == -1:
                if text:  # Add remaining text if any
                    new_nodes.append(TextNode(text, TextType.TEXT))
                break  # Exit the while loop
                
            second_delimiter = text.find(delimiter, first_delimiter + 1)
            if second_delimiter == -1:
                raise ValueError(f"No matching delimiter {delimiter} found in text")
            
            # Get the three parts:
            #everything before first delimiter
            before = text[:first_delimiter]
            
            #everything between delimiters
            between = text[first_delimiter + len(delimiter):second_delimiter]
            
            #everything after second delimiter
            text = text[second_delimiter + len(delimiter):]
            
            # Create new nodes for each part (if they're not empty)
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            if between:
                new_nodes.append(TextNode(between, text_type))
            # Continue loop to process remaining text

    # Return result list
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches