from enum import Enum
from htmlnode import LeafNode
import re


def text_to_textnodes(text):
    ls = [TextNode(text, TextType.TEXT)]
    ls = split_nodes_delimiter(ls, '`', TextType.CODE)
    ls = split_nodes_link(ls)
    ls = split_nodes_image(ls)
    ls = split_nodes_delimiter(ls, '**', TextType.BOLD)
    ls = split_nodes_delimiter(ls, '_', TextType.ITALIC)

    return ls

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    res = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            tmp = node.text.split(delimiter)
            if len(tmp) % 2 == 0:
                raise Exception("Invalid Block")

            for i in range(0, len(tmp)):
                if i % 2 == 0:
                    if tmp[i] != "":
                        res.append(TextNode(tmp[i], TextType.TEXT))
                elif i % 2 != 0:
                    res.append(TextNode(tmp[i], text_type))
        else:
            res.append(node)
    return res

def split_nodes_image(old_nodes):
    res = []
    for node in old_nodes:
        tmp = extract_markdown_images(node.text)
        if tmp:
            sections = node.text.split(f"![{tmp[0][0]}]({tmp[0][1]})", 1)
            if sections[0]:
                res.append(TextNode(sections[0], TextType.TEXT))
            res.append(TextNode(tmp[0][0], TextType.IMAGE, tmp[0][1]))
            if sections[1] and len(tmp) == 1:
                res.append(TextNode(sections[1], TextType.TEXT))
            elif sections[1] and len(tmp) > 1:
                res.extend(split_nodes_image([TextNode(sections[1], TextType.TEXT)]))
        else:
            res.append(node)
    return res

def split_nodes_link(old_nodes):
    res = []
    for node in old_nodes:
        tmp = extract_markdown_links(node.text)
        if tmp:
            sections = node.text.split(f"[{tmp[0][0]}]({tmp[0][1]})", 1)
            if sections[0]:
                res.append(TextNode(sections[0], TextType.TEXT))
            res.append(TextNode(tmp[0][0], TextType.LINK, tmp[0][1]))
            if sections[1] and len(tmp) == 1:
                res.append(TextNode(sections[1], TextType.TEXT))
            elif sections[1] and len(tmp) > 1:
                res.extend(split_nodes_link([TextNode(sections[1], TextType.TEXT)]))
        else:
            res.append(node)
    return res


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

class TextType(Enum):
    TEXT = "normal text"
    BOLD = "BOLD"
    ITALIC = "italic text"
    CODE = "code text"
    LINK = "link"
    IMAGE = "image"

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})



class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url


    def __eq__(self, target):
        if self.text == target.text and self.text_type == target.text_type and self.url == target.url:
            return True
        else:
            return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
