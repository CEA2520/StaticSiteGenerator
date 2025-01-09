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