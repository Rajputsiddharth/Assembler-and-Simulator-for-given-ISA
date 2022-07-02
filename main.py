typeA =["typeA","add","sub","mul","and","or","xor"]
typeB = ["typeB","mov","ls"]
typeC = ["typeC","not","cmp","div","mov"]
typeD = ["typeD","ld","st"]
typeE = ["typeE","je","jgt","jlt","jmp"]
typeF = ["typeF","hlt"]
Instruc = [typeA, typeB, typeC, typeD, typeE, typeF]

#Function to get encoding of register
def getRegister(reg):
    dict_reg = {
        "R0": "000",
        "R1": "001",
        "R2": "010",
        "R3": "011",
        "R4": "100",
        "R5": "101",
        "R6": "110",
        "FLAGS": "111"
    }

    return dict_reg[reg]


#Function to get encoding of instruction
def instruction(ins):
    dict_ins = {
        "add": "10000",
        "sub": "10001",
        "mul": "10110",
        "div": "10111",
        "ld": "10100",
        "st": "10101",
        "ls": "11001",
        "rs": "11000",
        "xor": "11010",
        "or": "11011",
        "and": "11100",
        "not": "11101",
        "cmp": "11110",
        "jmp": "11111",
        "jlt": "01100",
        "jgt": "01101",
        "je": "01111",
        "hlt": "01010",
        "mov1": "10010",
        "mov2": "10011"
    }

    return dict_ins[ins]


#function to convert decimal to binary


#Function decimal to binary
def decimal_to_binary(dec):
    dec = int(dec)
    bin = ""
    while dec > 0:
        bin = str(dec % 2) + bin
        dec = dec // 2

    while (len(bin) < 8):
        bin = "0" + bin
    return bin


#function to return type


#type of function to return 16 bit encodings
def Call_TypeA(list):
    newlist = []
    newlist.append(instruction(list[0]))
    newlist.append("00")
    newlist.append(getRegister(list[1]))
    newlist.append(getRegister(list[2]))
    newlist.append(getRegister(list[3]))
    answer = ''.join(newlist)
    return answer


def mov_B(list):
    newlist = []
    newlist.append("10010")
    newlist.append(getRegister(list[1]))
    newlist.append(decimal_to_binary(list[2][1:]))
    answer = ''.join(newlist)
    return answer



def mov_c(list):
    newlist = []
    newlist.append("10011")
    newlist.append("00000")
    newlist.append(getRegister(list[1]))
    newlist.append(getRegister(list[2]))
    answer = ''.join(newlist)
    return answer

  

def Call_TypeB(list):
    newlist = []
    newlist.append(instruction(list[0]))
    newlist.append(getRegister(list[1]))
    newlist.append(decimal_to_binary(list[2][1:]))
    answer = ''.join(newlist)
    return answer


def Call_TypeC(list):
    newlist = []
    newlist.append(instruction(list[0]))
    newlist.append("00000")
    newlist.append(getRegister(list[1]))
    newlist.append(getRegister(list[2]))
    answer = ''.join(newlist)
    return answer


def Call_TypeD(list):
    newlist = []
    newlist.append(instruction(list[0]))
    newlist.append(getRegister(list[1]))
    newlist.append(decimal_to_binary(str(l_count+var_lst.index(list[2])+1)))
    answer = ''.join(newlist)
    return answer


def Call_TypeE(list):
    newlist = []
    newlist.append(instruction(list[0]))
    newlist.append("000")
    newlist.append(decimal_to_binary(str(l_count+var_lst.index(list[2])+1)))
    answer = ''.join(newlist)
    return answer


def Call_TypeF(list):
    newlist = []
    newlist.append(instruction(list[0]))
    newlist.append("00000000000")
    answer = ''.join(newlist)
    return answer


def Call_Func(str, list):
    if str == "typeA":
        return Call_TypeA(list)
    elif str == "typeB":
        return Call_TypeB(list)
    elif str == "typeC":
        return Call_TypeC(list)
    elif str == "typeD":
        return Call_TypeD(list)
    elif str == "typeE":
        return Call_TypeE(list)
    elif str == "typeF":
        return Call_TypeF(list)

def lastcount():
    lcount = 0
    with open("test_cases.txt","r") as f:
        for line in f:
            line=line.split()
            if line[0] == "var":
                pass
            else:
                lcount += 1
    return lcount-1



#main function 
check = 0
count = 1
var_lst=[]
l_count=lastcount()

f=open("test_cases.txt","r")
while True:
    line = f.readline()
    cmd = line.split()
    if cmd[0]=="var":
      var_lst.append(cmd[1])
    if cmd[0][0:2] == "la":
        for item in Instruc:
            if cmd[1] in item:
                print(Call_Func(item[0], cmd[1:]))
            else:
                pass
    if cmd[0] == "hlt":
        print(Call_Func("typeF",cmd))
        f.close()
        break
    elif cmd[0] == "mov":
        if cmd[2][0] == "$":
            print(mov_B(cmd))
        else:
            print(mov_c(cmd))
    else:
        for item in Instruc:
            if cmd[0] in item:
                print(Call_Func(item[0], cmd))
                check = 1
                break
            else:
                pass
        # if check==0:     #if the command is not found in the list of instructions
        #     print("Invalid Instruction")
    check = 0
    count += 1
