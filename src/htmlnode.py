
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (
            self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props
        )    
    
    def to_html(self):
        raise NotImplementedError("This is not active for now")
    
    def props_to_html(self):
        return " ".join([f'{key}="{value}"' for key, value in self.props.items()]) if self.props else ""
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    

class LeafNode(HTMLNode):
    # attributes of child class (LeafNode)
    def __init__(self, tag=None, value=None, props=None):
        if value is None:
            raise ValueError("LeafNode must have a no-None value")
        # attribute of parent class (HTMLNode)
        super().__init__(tag, value, None, props)
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if children is None:
            raise ValueError("ParentNode must have a no-None children")
        if tag is None:
            raise ValueError("ParentNode must have a no-None tag")
        super().__init__(tag, None, children, props)
        
    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode must have a tag")
        if not self.children:
            raise ValueError("ParentNode must have children")
        children_html = "".join([child.to_html() for child in self.children])
        props_html = self.props_to_html()
        opening_tag = self.tag
        if props_html:
            opening_tag += f" {props_html}"
        return f"<{opening_tag}>{children_html}</{self.tag}>"
    
    def __eq__(self, other):
        if not isinstance(other, ParentNode):
            return False
        return (
            self.tag == other.tag and
            self.children == other.children and
            self.props == other.props
        )
    
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.value}, {self.children}, {self.props})"