from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "<P>"
    HEADING = "<H1>"
    CODE = "code"
    QUOTE = "quote"
    ULS = "unordered_list"
    OLS = "ordered_list"
        
    

def markdown_to_blocks(markdown):
    tmp = markdown.split("\n\n")
    res = []
    for block in tmp:
        stripped = block.strip()
        if stripped:
            res.append(stripped)
    return res

def block_to_block_type(block):

    if len(block) == 0:
        return None
    i = 0
    while i < len(block) and block[i] == "#":
        i += 1

        
    if i < len(block) and i <= 6 and i > 0 and block[i] == " ":
        return BlockType.HEADING
    elif block[:3] == "```":
        return BlockType.CODE
    elif block[0] == ">":
        return BlockType.QUOTE
    elif block[:2] == "- ":
        return BlockType.ULS
    elif block[0].isdigit() and block[1:3] == ". ":
        return BlockType.OLS
    else:
        return BlockType.PARAGRAPH
    
