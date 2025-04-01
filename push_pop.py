def getPushD():
    return "@SP,A=M,M=D,@SP,M=M+1"

def getPopD():
    return "@SP,M=M-1,A=M,D=M"

def test_push_pop():
    # Hack machine state simulation
    memory = {
        0: 256,    # SP is stored at address 0, initialized to 256
        # Other memory locations will be used as stack
    }
    D = 1234      # Test value to push
    A = 0         # Address register
    
    def execute(instruction):
        nonlocal A, D, memory
        if instruction == "@SP":
            A = 0  # SP is at address 0
        elif instruction == "A=M":
            A = memory[A]
        elif instruction == "M=D":
            memory[A] = D
        elif instruction == "@SP,M=M+1":
            memory[0] += 1
        elif instruction == "@SP,M=M-1":
            memory[0] -= 1
        elif instruction == "D=M":
            D = memory[A]
    
    # Test push
    for op in getPushD().split(','):
        execute(op)
    
    assert memory[0] == 257, f"Push failed: SP={memory[0]} (expected 257)"
    assert memory[256] == 1234, f"Push failed: stack[256]={memory.get(256)} (expected 1234)"
    
    # Test pop
    for op in getPopD().split(','):
        execute(op)
    
    assert memory[0] == 256, f"Pop failed: SP={memory[0]} (expected 256)"
    assert D == 1234, f"Pop failed: D={D} (expected 1234)"
    
    print("All tests passed!")

test_push_pop()
