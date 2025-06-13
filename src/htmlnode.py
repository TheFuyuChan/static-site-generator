class HTMLNode():
    def __init__(self, tag=None, value=None, children=[], props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        res = ""
        if self.props == None:
            return ""
        for key in self.props:
            res += " " + key + "=" + f'"{self.props[key]}"'
        return res

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)


    def to_html(self):
        if self.value == None:
            raise ValueError()
        if self.tag == None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("missing tag")
        if self.children == None:
            raise ValueError("missing children")
        res = ""
        for child in self.children:
            res += child.to_html()

        return f'<{self.tag}{self.props_to_html()}>{res}</{self.tag}>'
