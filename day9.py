with open("day9.txt") as f:
    puzzle = f.read()

file = True

original_memory = list()
id = 0
for c in puzzle:
    if file:
        for i in range(int(c)):
            original_memory.append(id)
        id += 1
    else:
        for i in range(int(c)):
            original_memory.append(".")

    file = not file

memory = original_memory[:]


def find_next_free_block(mem, start):
    while True:
        if mem[start] == ".":
            return start
        start += 1


def size_of_free_block(mem, start):
    size = 0
    while True:
        if mem[start] == ".":
            size += 1
        else:
            return size


def find_free_block_of_size(size, mem):
    start_of_free_block = None
    for i, block in enumerate(mem):
        if block == ".":
            if start_of_free_block is None:
                start_of_free_block = i
        else:
            if start_of_free_block is not None:
                block_size = i - start_of_free_block
                if block_size >= size:
                    return start_of_free_block
                else:
                    start_of_free_block = None
    return None


def size_of_file(mem, id):
    i = 0
    while i < len(mem) and str(mem[i]) != str(id):
        i += 1
    size = 0
    while i < len(mem) and str(mem[i]) == str(id):
        size += 1
        i += 1
    return size


def index_of_file(mem, id):
    i = 0
    while i < len(mem) and str(mem[i]) != str(id):
        i += 1
    return i


def checksum(mem):
    cs = 0
    i = 0
    for block in mem:
        if block != ".":
            cs += i * int(block)
        i += 1

    return cs


free_block = find_next_free_block(memory, 0)
for i in reversed(range(len(memory))):
    register = memory[i]
    memory[i] = "."
    memory[free_block] = register

    free_block = find_next_free_block(memory, free_block)
    if free_block >= i:
        break

print(f"Part 1: {checksum(memory)}")

memory = original_memory[:]
i = len(memory) - 1
id = None
while True:
    if id is None:
        while memory[i] == ".":
            i -= 1
        id = int(memory[i])

    file_start = index_of_file(memory, id)
    file_size = size_of_file(memory, id)
    free_block = find_free_block_of_size(file_size, memory)
    print(file_start, free_block, id, file_size)

    if free_block and free_block < file_start:
        for j in range(file_size):
            memory[free_block + j] = id
            memory[file_start + j] = "."
    id -= 1
    if id < 0:
        break

print(memory)
print(f"Part 2: {checksum(memory)}")
