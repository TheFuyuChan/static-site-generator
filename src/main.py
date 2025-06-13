from email.mime import base
from unittest import result
from textnode import *
from htmlnode import *
from blocks import *
from markdown import Markdown
from io import StringIO
import os, shutil, sys

print(f"sys.argv: {sys.argv}")
basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
print(f"Basepath value: '{basepath}'")

def markdown_to_html_node(md):
    blocks = markdown_to_blocks(md)
    papa = ParentNode("div", children=[])
    for block in blocks:
        b_type = block_to_block_type(block)
        if b_type == BlockType.PARAGRAPH:
            lines = [line.strip() for line in block.splitlines()]
            text = ' '.join(lines)
            node = ParentNode(tag="p", children=text_to_children(text))
        elif b_type == BlockType.HEADING:
            i = 0
            while i < len(block) and block[i] == "#":
                i += 1
            node = ParentNode(tag=f"h{i}", children=text_to_children(block[i+1:]))
        elif b_type == BlockType.CODE:
            lines = block.split('\n')
            code_lines = lines[1:-1]  # Remove first and last lines (the ```)
            stripped_lines = [line.lstrip() for line in code_lines]
            code_content = '\n'.join(stripped_lines) + '\n'  # Add trailing newline
            node = ParentNode(tag="pre", children=[LeafNode(tag="code", value=code_content)])
        elif b_type == BlockType.QUOTE:
            cleaned_lines = []
            lines = block.split('\n')
            for line in lines:
                cleaned_line = line.lstrip(">").lstrip()
                cleaned_lines.append(cleaned_line)

            cleaned_block_content = "\n".join(cleaned_lines)
            node = ParentNode(tag="blockquote", children=text_to_children(cleaned_block_content))
        elif b_type == BlockType.OLS:
            ls = block.split("\n")
            node = ParentNode(tag="ol", children=[])
            for l in ls:
                entry = l.split(". ", 1)
                node.children.append(ParentNode("li", children=text_to_children(entry[1])))
        elif b_type == BlockType.ULS:
            ls = block.split("\n")
            node = ParentNode(tag="ul", children=[])
            for l in ls:
                entry = l.split("- ", 1)
                node.children.append(ParentNode("li", children=text_to_children(entry[1])))
        papa.children.append(node)
    return papa
def text_to_children(text):
    l = text_to_textnodes(text)
    res = []
    for n in l:
        res.append(text_node_to_html_node(n))
    return res

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as f:
        file = f.read()
    with open(template_path, 'r') as f:
        template = f.read()
    html = markdown_to_html_node(file)
    title = extract_title(file)
    result = template.replace("{{ Title }}", title).replace("{{ Content }}", html.to_html())
    result = result.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    dir_name = os.path.dirname(dest_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(result)
    
def move_to_dir(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.makedirs(dest)
    for item in os.listdir(src):
        s_item = os.path.join(src, item)
        d_item = os.path.join(dest, item)
        if os.path.isfile(s_item):
            shutil.copy(s_item, d_item)
        else:
            move_to_dir(s_item, d_item)

def extract_title(markdown):
    res = markdown.split("# ")
    return res[1].split("\n")[0]

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        s_item = os.path.join(dir_path_content, item)
        d_item = os.path.join(dest_dir_path, item)
        if os.path.isfile(s_item):
            if s_item.split(".")[-1] == "md":
                suffix = d_item.split(".")[:-1]
                suffix.append("html")
                d_item = ".".join(suffix)
                generate_page(s_item, template_path, d_item)    
        else:
            os.makedirs(d_item)
            generate_pages_recursive(s_item, template_path, d_item)

def main():
    if os.path.exists("docs"):
        shutil.rmtree("docs")
    os.makedirs("docs")
    move_to_dir("static", "docs")
    generate_pages_recursive("content", "template.html", "docs")



main()
