
class HTMLNode:
    def __init__(self, tag: str | None = None, value: str | None = None, children: list["HTMLNode"] | None = None, props: dict[str, str] | None = None):
        self.tag: str | None = tag
        self.value: str | None = value
        self.children: list["HTMLNode"] | None = children
        self.props: dict[str, str] | None = props
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HTMLNode):
            return False
        return (
            self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props
        )    
    
    def to_html(self) -> str:
        raise NotImplementedError("This is not active for now")
    
    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        props_html: str = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html
    
    def __repr__(self) -> str:
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
        # if props:
        #     return f"<{self.tag}{props}>" + f"{self.value}" + f"</{self.tag}>"
        # return f"<{self.tag}>{self.value}</{self.tag}>"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str, str] | None = None):
        if children is None:
            raise ValueError("ParentNode must have a no-None children")
        if tag is None:
            raise ValueError("ParentNode must have a no-None tag")
        super().__init__(tag, None, children, props)
        
    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("ParentNode must have a tag")
        if not self.children:
            raise ValueError("ParentNode must have children")
        children_html: str = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>" 
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ParentNode):
            return False
        return (
            self.tag == other.tag and
            self.children == other.children and
            self.props == other.props
        )
    
    def __repr__(self) -> str:
        return f"ParentNode({self.tag}, {self.value}, {self.children}, {self.props})"