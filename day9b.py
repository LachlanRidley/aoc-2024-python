from dataclasses import dataclass
from typing import Literal, Union, Self


@dataclass
class Block:
    type: Union[Literal["free"], Literal["file"]]
    id: int | None
    size: int
    prev: Self | None
    next: Self | None


puzzle = "2333133121414131402"

file = True
memory_start: Block | None = None
memory: Block | None = None
memory_end: Block | None = None
id = 0
for size in puzzle:
    if file:
        block = Block("file", id, size, None, None)
        id += 1
    else:
        block = Block("free", None, size, None, None)

    if memory_start is None:
        memory_start = block
    else:
        memory.next = block
        block.prev = memory
        memory = block
    
    memory_end = memory

    file = not file

free_block = memory
file = 
while free_block.type != "free":
    free_block = free_block.next



