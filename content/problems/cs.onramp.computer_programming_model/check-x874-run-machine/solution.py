def run_machine(program):
    mem = {}
    out = []
    for instr in program:
        op = instr[0]
        if op == "set":
            mem[instr[1]] = instr[2]
        elif op == "add":
            mem[instr[1]] = mem.get(instr[1], 0) + mem.get(instr[2], 0)
        elif op == "sub":
            mem[instr[1]] = mem.get(instr[1], 0) - mem.get(instr[2], 0)
        elif op == "out":
            out.append(mem.get(instr[1], 0))
    return out
