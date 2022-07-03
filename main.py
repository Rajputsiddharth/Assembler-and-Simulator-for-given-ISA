typeA =["typeA","add","sub","mul","and","or","xor"]
typeB = ["typeB","mov","ls","rs"]
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
    if list[1][0:5] == "label":
        new_str = list[1] + ":"
        newlist.append(decimal_to_binary(str(dict_label[new_str])))
    else:
        newlist.append(decimal_to_binary(str(l_count+var_lst.index(list[1])+1)))
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
            if len(line) == 0:
                pass
            else:
                if line[0] == "var":
                    pass
                else:
                    lcount += 1
    return lcount-1








def isImmediate(imm):
    if imm[0]=="$":
        if imm[1:].isdigit()==True:
            if int(imm[1:])>=0 and int(imm[1:])<=255:
                return True
            else:
                return False
        else:
            return False
    else:
        return False



def isRegister(reg):
    dict_reg = {
        "R0": "000","R1": "001","R2": "010","R3": "011","R4": "100","R5": "101","R6": "110","FLAGS": "111"
    }
    if reg in dict_reg and reg != "FLAGS":
        return 1
    else:
        return 0




def Error():
    E=0
    Flaag=0
    k=open("test_cases.txt","r")
    lst=[]
    lst_str=[]
    for line in k:
        lst_str.append(line)
        line = line.strip()
        line = line.split()
        if len(line) == 0:
            pass
        else:
            lst.append(line)
    k.close()
    
    for i in range(len(lst)):
        if lst[i][0] == "var":
            if len(lst[i]) != 2:
                print(f"Error in line {i+1}: var statement does not follow the syntax")
                quit()
            if Flaag==1:
                print(f'Error in line {i+1} : Variables should be declared in the beginning') 
                quit()
            else:
                if (lst[i][1]).isidentifier():
                    pass
                else:
                  print(f'Error in line {i+1} : not a valid variable name')
                  quit()

        # if ":" in lst[i][0] and not((lst[i][0][:-1]).isidentifier()):
        #     print(f'Error in line {i+1} : Illegal label name') 
        #     quit()
        # elif ":" in lst[i][0] and (lst[i][0][:-1]).isidentifier():

        elif lst[i][0] == "mov" and lst[i][2][0]=="$":
            if len(lst[i]) == 3:
                if isRegister(lst[i][1])==0 :
                    print(f'Error in line,{i+1} : not a valid register')
                    quit()
                elif isRegister(lst[i][1])==1 and isImmediate(lst[i][2])==0:
                    print(f'Error in line,{i+1} : not a valid immediate')
                    quit()
            else:
                print(f'Error in line {i+1} : Invalid format of instruction')
                quit()

     #To seperate out mov commands as they might create problems in Instruc[] loop.
        elif lst[i][0] == "mov" and lst[i][2][0]!= "$":
            if len(lst[i]) == 3:
                    
                if isRegister(lst[i][1])==1 and isRegister(lst[i][2])==1:
                    pass
                elif lst[i][1]=="FLAGS" and isRegister(lst[i][2])==1:
                    pass
            
                elif "FLAGS" in lst[i]:
                    print(f'Error in line,{i+1} : invalid use of flags')
                    quit()
                else:
                    print(f'Error in line,{i+1} : not a valid register')
                    quit()
            else:
                print(f'Error in line {i+1} : Invalid format of instruction')
                quit()


        elif lst[i][0] in Instruc[0] or lst[i][0] in Instruc[1] or lst[i][0] in Instruc[2] or lst[i][0] in Instruc[3] or lst[i][0] in Instruc[4] or lst[i][0] in Instruc[5]:
            Flaag=1
            if lst[i][0] in Instruc[0]:
                if len(lst[i]) == 4:
                    if isRegister(lst[i][1])==0 or isRegister(lst[i][2])==0 or isRegister(lst[i][3])==0:
                        print(f'Error in line {i+1} : not a valid register')
                        quit()
                else:
                    print(f'Error in line {i+1} : Invalid format of instruction')
                    quit()

            elif lst[i][0] in Instruc[1]:
                if len(lst[i]) == 3:
                    if isRegister(lst[i][1])==0 :
                        print(f'Error in line {i+1} : not a valid register')
                        quit()
                    elif isRegister(lst[i][1])==1 and isImmediate(lst[i][2])==0:
                        print(f'Error in line {i+1} : not a valid immediate')
                        quit()
                else:
                    print(f'Error in line {i+1} : Invalid format of instruction')
                    quit()

            elif lst[i][0] in Instruc[2]:
                if len(lst[i]) == 3:
                    if isRegister(lst[i][1])==0 or isRegister(lst[i][2])==0:
                        print(f'Error in line,{i+1} : not a valid register')
                        quit()
                else:
                    print(f'Error in line {i+1} : Invalid format of instruction')
                    quit()

            elif lst[i][0] in Instruc[3]:
                if len(lst[i]) == 3:
                    if isRegister(lst[i][1])==0:
                        print(f'Error in line {i+1} : not a valid register')
                        quit()
                    elif isRegister(lst[i][1])==1 and lst[i][2] not in var_lst:
                        print(f'Error in line {i+1} : variable not declared')
                        quit()
                else:
                    print(f'Error in line {i+1} : Invalid format of instruction')
                    quit()

            elif lst[i][0] in Instruc[4]:
                if len(lst[i]) == 2:
                    if lst[i][1]==1 not in dict_label.keys():
                        print(f'Error in line {i+1} : label not declared')
                        quit()
                else:
                    print(f'Error in line {i+1} : Invalid format of instruction')
                    quit()

            elif lst[i][0] in Instruc[5]:
                if len(lst[i]) == 1:

                    if i != len(lst)-1:
                        print(f"Error in line {i+1} : hlt not used as last instruction.")
                        quit()
                else:
                    print(f'Error in line {i+1} : Invalid format of instruction')
                    quit()

        else:
            print(f'Error in line,{i+1} : General syntax error')
            quit()
    if lst[-1][0] == "hlt":
        pass
    else:
        print(f"Error in last line: hlt missing")
        quit()
       


#main function 
dict_label = {}
counter = -1
f =  open("test_cases.txt","r")
for l in f:
    line = l
    line=line.split()
    if len(line) == 0:
        pass
    else:
        if line[0] != "var":
            counter += 1
        if line[0][-1] == ":":
            dict_label[line[0][0::]] = counter
        if line[0] == "hlt":
            break
check = 0
count = 1
var_lst=[]
l_count=lastcount()
Error()
g=open("output_CO.txt","w")
g.close

g=open("output_CO.txt","a")

f=open("test_cases.txt","r")
while True:
    line = f.readline()
    cmd = line.split()
    if len(cmd) != 0:
        if cmd[0]=="var":
            var_lst.append(cmd[1])
        if cmd[0][0:2] == "la":
            for item in Instruc:
                if cmd[1] in item:
                    g.write(Call_Func(item[0], cmd[1:]))
                    g.write("\n")
                    print(Call_Func(item[0], cmd[1:]))
                else:
                    pass
        if cmd[0] == "hlt":
            g.write(Call_Func("typeF", cmd))
            g.write("\n")
            print(Call_Func("typeF",cmd))
            f.close()
            g.close()
            break
        elif cmd[0] == "mov":
            if cmd[2][0] == "$":
                g.write(mov_B(cmd))
                g.write("\n")
                print(mov_B(cmd))
            else:
                g.write(mov_c(cmd))
                g.write("\n")
                print(mov_c(cmd))
        else:
            for item in Instruc:
                if cmd[0] in item:
                    g.write(Call_Func(item[0], cmd))
                    g.write("\n")
                    print(Call_Func(item[0], cmd))
                    check = 1
                    break
                else:
                    pass
            # if check==0:     #if the command is not found in the list of instructions
            #     print("Invalid Instruction")
        check = 0
        count += 1
    else:
        pass
