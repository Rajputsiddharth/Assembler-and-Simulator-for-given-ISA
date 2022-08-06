import sys
memory = ["0000000000000000"]*256  #memory list
register_file = [0,0,0,0,0,0,0,0]  

halt = False   #global halt
pc = 0         #global pc
temp = pc - 1
pointer = 1 
def bin_dec(string):
    l=[]
    for i in string:
        l.append(i)
    l1=[int(x)for x in l]
    l1.reverse()
    d=0
    for i in range(len(l1)):
        d += (2**i)*l1[i]
    return d

#cinversion function 
def convertBinary_8(dec):              
    bin = ""
    while dec > 0:
        bin = str(dec % 2) + bin
        dec = dec // 2

    while (len(bin) < 8):
        bin = "0" + bin 
    return bin

#conversion function
def convertBinary_16(dec):
    bin = ""
    while dec > 0:
        bin = str(dec % 2) + bin
        dec = dec // 2

    while (len(bin) < 16):
        bin = "0" + bin 
    return bin

def decimal_conv(ins,num):
    s1={'0','1','2','3','4','5','6','7','8','9'}
    s2=set(ins)
    if s2.issubset(s1):
        x=int(ins)
        l=[]
        while x>0:
            r=x%num
            x=x//num
            l.append(r)
        l.reverse()
        lst=[str(v) for v in l]
        l1=[]
        for i in range(10,36):
            l1.append(i)
        l2=[]
        for i in range(65,91):
            l2.append(chr(i))
        l3=[str(x) for x in l1]
        d=dict(zip(l3,l2))
        new_lst=[]
        for i in lst:
            if i in d:
                new_lst.append(d[i])
            else:
                new_lst.append(i)
        ans=''.join(new_lst)
        return ans
    else:
        pass


def conv_int(string):
    l=[]
    for i in string:
        l.append(i)
    l1=[int(x)for x in l]
    l1.reverse()
    d=0
    for i in range(len(l1)):
        d += (2**i)*l1[i]
    return d

def load(ins):
    r1 = conv_int(ins[5:8])
    memory_address = conv_int(ins[8:])
    register_file[r1] = conv_int(memory[memory_address])
    global temp
    temp += 1
    global pc
    pc = pc + 1
    register_file[7] = 0

#right inverted
def rightshift(ins):
    r1 = conv_int(ins[5:8])
    immediate = conv_int(ins[8:])
    register_file[r1]=register_file[r1]>>immediate
    global temp
    temp += 1
    global pc
    pc = pc + 1
    register_file[7] = 0

#immediate displacement 
def move_immediate(ins):
    dest_reg = conv_int(ins[5:8])
    immediate = conv_int(ins[8:])
    register_file[dest_reg] = immediate
    global temp
    temp += 1
    global pc
    pc = pc + 1
    register_file[7] = 0

def compare(ins):
    r1 = conv_int(ins[10:13])
    r2 = conv_int(ins[13:])
    value_r1 = register_file[r1]
    value_r2 = register_file[r2]
    if(value_r1 == value_r2):
        register_file[7] = 1

    elif(value_r1 > value_r2):
        register_file[7] = 2

    else:
        register_file[7] = 4
    global temp
    temp += 1
    global pc
    pc = pc + 1

def jump(ins):
    global pc
    memory_address = conv_int(ins[8:])
    pc = memory_address
    register_file[7] = 0

def store(ins):
    r1 = conv_int(ins[5:8])
    memory_address = conv_int(ins[8:])
    memory[memory_address] = convertBinary_16(register_file[r1])
    global temp
    temp += 1
    global pc
    pc = pc + 1
    register_file[7] = 0

def jump_GT(ins):
    global pc
    global temp
    if(register_file[7] == 2):
        memory_address = conv_int(ins[8:])
        pc = memory_address
    else:
        temp += 1
        pc = pc + 1
    register_file[7] = 0

def And(ins):
    r1 = conv_int(ins[7:10])
    r2 = conv_int(ins[10:13])
    dest_reg = conv_int(ins[13:16])
    and_register = (register_file[r1])&(register_file[r2])
    register_file[dest_reg] = and_register
    global temp
    temp += 1
    global pc
    pc = pc + 1
    register_file[7] = 0
    
def Not(ins):
    r1 = int(ins[10:13])
    dest_reg= int(ins[13:16])
    x = register_file[r1]
    negation_reg = 65535 - x
    register_file[dest_reg] = negation_reg
    global temp
    temp += 1
    global pc
    pc = pc + 1
    register_file[7] = 0
    
def jump_equal(ins):
    global pc
    global temp
    if(register_file[7] == 1):
        memory_address = conv_int(ins[8:])
        pc = memory_address
    else:
        temp += 1
        pc = pc + 1
    register_file[7] = 0

def addition(ins):
    r1= conv_int(ins[7:10])
    r2 = conv_int(ins[10:13])
    dest_reg = conv_int(ins[13:16])
    sum_registers = register_file[r1] + register_file[r2]
    if sum_registers < 65535:
        register_file[dest_reg] = sum_registers
        register_file[7] = 0
    else:
        register_file[dest_reg] = sum_registers % 65536
        register_file[7] = 8
    global temp
    temp += 1
    global pc
    pc = pc + 1

def leftshift(ins):
    r1 = conv_int(ins[5:8])
    immediate = conv_int(ins[8:])
    register_file[r1]=register_file[r1]<<immediate
    global temp
    temp += 1
    global pc
    pc = pc + 1
    register_file[7] = 0

def subtraction(ins):
    r1 = conv_int(ins[7:10])
    r2 = conv_int(ins[10:13])
    dest_reg = conv_int(ins[13:16])
    diff_registers = register_file[r1] - register_file[r2]
    if diff_registers >= 0 :
        register_file[dest_reg] = diff_registers
        register_file[7] = 0
    else:
        register_file[dest_reg] = 0
        register_file[7] = 8
    global temp
    temp += 1
    global pc
    pc = pc + 1

def move_register(ins):
    source_reg = conv_int(ins[10:13])
    dest_reg = conv_int(ins[13:16])
    register_file[dest_reg] = register_file[source_reg]
    global temp
    temp += 1
    global pc
    pc = pc + 1
    register_file[7] = 0

def multiply(ins):
    r1 = conv_int(ins[7:10])
    r2 = conv_int(ins[10:13])
    dest_reg = conv_int(ins[13:16])
    product_register = register_file[r1] * register_file[r2]
    if product_register < 65535:
        register_file[dest_reg] = product_register
        register_file[7] = 0
    else:
        register_file[dest_reg] = product_register % 65536
        register_file[7] = 8
    global temp
    temp += 1
    global pc
    pc = pc + 1

def divide(ins):
    r1 = conv_int(ins[10:13])
    r2 = conv_int(ins[13:16])
    register_file[0] = (register_file[r1])//(register_file[r2])
    register_file[1] = (register_file[r1])%(register_file[r2])
    global temp
    temp += 1
    global pc
    pc = pc + 1
    register_file[7] = 0

def Or(ins):
    r1 = conv_int(ins[7:10])
    r2 = conv_int(ins[10:13])
    dest_reg = conv_int(ins[13:16])
    or_register = (register_file[r1])|(register_file[r2])
    register_file[dest_reg] = or_register
    global temp
    temp += 1
    global pc
    pc = pc + 1
    register_file[7] = 0

def jump_LT(ins):
    global pc
    global temp
    if(register_file[7] == 4):
        memory_address = conv_int(ins[8:])
        pc = memory_address
    else:
        temp += 1
        pc = pc + 1
    register_file[7] = 0


def xor(ins):
    r1 = conv_int(ins[7:10])
    r2 = conv_int(ins[10:13])
    value_r1 = register_file[r1]
    negation_r1 = 65535 - value_r1
    dest_reg = conv_int(ins[13:16])
    value_r2 = register_file[r2]
    negation_r2 = 65535 - value_r2
    xor_register = ((value_r1)&(negation_r2))|((negation_r1)&(value_r2))
    register_file[dest_reg] = xor_register
    global temp
    temp += 1
    global pc
    pc = pc + 1
    register_file[7] = 0

def hlt(ins):
    register_file[7] = 0
    global halt
    halt = True 


oper_array= [0,0,0,0,0,0,0,0,0,0,hlt,0,jump_LT,jump_GT,0,jump_equal,addition,subtraction,move_immediate,move_register,load,store,multiply,divide,rightshift,leftshift,xor,Or,And,Not,compare,jump]


input = sys.stdin.read()
fininp = input.split('\n')

instruct_lst=[]
for i in range (len(fininp)):
    if (len(fininp[i])>0):
        instruct_lst.append(fininp[i])

count = 0
for i in instruct_lst:
    memory[count] = i
    count += 1

#while loop printing alll instructsions

while (halt == False):
    current = memory[pc]
    s = convertBinary_8(pc)
    print(s,end = " ")
    ins_index = conv_int(current[0:5])
    oper_array[ins_index](current)

    for i in range(len(register_file)-1):
        s = convertBinary_16(register_file[i])
        print(s,end = " ")
            
    s = convertBinary_16(register_file[7])
    print(s)
    pointer += 1

    if(pointer == 0):
        decimal_conv(register_file[0])  
    
    
  
#printing the dumped mememory
for i in range (len(memory)):
    print(memory[i])
    
