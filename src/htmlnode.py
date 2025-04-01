
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
        if self.props is None:
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    

class LeafNode(HTMLNode):
    # attributes of child class (LeafNode)
    def __init__(self, tag, value, props=None):
        # attribute of parent class (HTMLNode)
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("invalid HTML: no value")
        if self.tag is None:
            return self.value
        props = self.props_to_html()
        # if props:
        #     return f"<{self.tag}{props}>" + f"{self.value}" + f"</{self.tag}>"
        # return f"<{self.tag}>{self.value}</{self.tag}>"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
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
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>" 
    
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