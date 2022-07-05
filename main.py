import sys

fininp = [i.split() for i in sys.stdin.readlines()]

typeA = ["typeA", "add", "sub", "mul", "and", "or", "xor"]
typeB = ["typeB", "mov", "ls", "rs"]
typeC = ["typeC", "not", "cmp", "div", "mov"]
typeD = ["typeD", "ld", "st"]
typeE = ["typeE", "je", "jgt", "jlt", "jmp"]
typeF = ["typeF", "hlt"]
Instruc = [typeA, typeB, typeC, typeD, typeE, typeF]

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
    global dict_ins
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
    newlist.append(decimal_to_binary(str(l_count + var_lst.index(list[2]) +
                                         1)))
    answer = ''.join(newlist)
    return answer


def Call_TypeE(list):
    newlist = []
    newlist.append(instruction(list[0]))
    newlist.append("000")
    newlist.append(decimal_to_binary(str(dict_label[list[1] + ":"])))
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
    for i in fininp:
        if len(i) == 0:
            pass
        else:
            if i[0] == "var":
                pass
            else:
                lcount += 1
    return lcount - 1


def isImmediate(imm):
    if imm[0] == "$":
        if imm[1:].isdigit() == True:
            if int(imm[1:]) >= 0 and int(imm[1:]) <= 255:
                return True
            else:
                return False
        else:
            return False
    else:
        return False


def isRegister(reg):
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
    if reg in dict_reg and reg != "FLAGS":
        return 1
    else:
        return 0


def Error():
    Flaag = 0
    lst = []
    for i in fininp:
        if len(i) == 0:
            pass
        else:
            lst.append(i)

    for i in range(len(lst)):
        if lst[i][0] == "var":
            if len(lst[i]) != 2 or lst[i][1] == "":
                print(
                    f"Error in line {i+1}: var statement does not follow the syntax"
                )
                quit()
            if Flaag == 1:
                print(
                    f'Error in line {i+1} : Variables should be declared in the beginning'
                )
                quit()
            else:
                if (lst[i][1]
                    ).isidentifier() and lst[i][1] not in dict_ins.keys():
                    pass
                else:
                    print(f'Error in line {i+1} : not a valid variable name')
                    quit()
        elif lst[i][0][-1] == ":":
            if not ((lst[i][0][:-1]).isidentifier()):
                print(f'Error in line {i+1} : not a valid label name')
                quit()
            elif len(lst[i]) != 1:
                if lst[i][1:][0] == "mov" and lst[i][1:][2][0] == "$":  #CHECK
                    Flaag = 1
                    if len(lst[i][1:]) == 3:
                        if isRegister(lst[i][1:][1]) == 0:
                            print(
                                f'Error in line {i+1} : not a valid register')
                            quit()
                        elif isRegister(lst[i][1:][1]) == 1 and isImmediate(
                                lst[i][1:][2]) == 0:
                            print(
                                f'Error in line {i+1} : not a valid immediate')
                            quit()
                    else:
                        print(
                            f'Error in line {i+1} : Invalid format of instruction'
                        )
                        quit()

                elif lst[i][1:][0] == "mov" and lst[i][1:][2][0] != "$":
                    Flaag = 1
                    if len(lst[i][1:]) == 3:
                        if isRegister(lst[i][1:][1]) == 1 and isRegister(
                                lst[i][1:][2]) == 1:
                            pass
                        elif lst[i][1:][1] == "FLAGS" and isRegister(
                                lst[i][1:][2]) == 1:
                            pass

                        elif "FLAGS" in lst[i][1:]:
                            print(
                                f'Error in line {i+1} : invalid use of flags')
                            quit()
                        else:
                            print(
                                f'Error in line,{i+1} : not a valid register')
                            quit()
                    else:
                        print(
                            f'Error in line {i+1} : Invalid format of instruction'
                        )
                        quit()

                elif lst[i][1:][0] in Instruc[0] or lst[i][1:][0] in Instruc[
                        1] or lst[i][1:][0] in Instruc[2] or lst[i][1:][
                            0] in Instruc[3] or lst[i][1:][0] in Instruc[
                                4] or lst[i][1:][0] in Instruc[5]:
                    Flaag = 1
                    if lst[i][1:][0] in Instruc[0]:
                        if len(lst[i][1:]) == 4:
                            if isRegister(lst[i][1:][1]) == 0 or isRegister(
                                    lst[i][1:][2]) == 0 or isRegister(
                                        lst[i][1:][3]) == 0:
                                print(
                                    f'Error in line {i+1} : not a valid register'
                                )
                                quit()
                        else:
                            print(
                                f'Error in line {i+1} : Invalid format of instruction'
                            )
                            quit()

                    elif lst[i][1:][0] in Instruc[1]:
                        if len(lst[i]) == 3:
                            if isRegister(lst[i][1:][1]) == 0:
                                print(
                                    f'Error in line {i+1} : not a valid register'
                                )
                                quit()
                            elif isRegister(
                                    lst[i][1:][1]) == 1 and isImmediate(
                                        lst[i][1:][2]) == 0:
                                print(
                                    f'Error in line {i+1} : not a valid immediate'
                                )
                                quit()
                        else:
                            print(
                                f'Error in line {i+1} : Invalid format of instruction'
                            )
                            quit()

                    elif lst[i][1:][0] in Instruc[2]:
                        if len(lst[i][1:]) == 3:
                            if isRegister(lst[i][1:][1]) == 0 or isRegister(
                                    lst[i][1:][2]) == 0:
                                print(
                                    f'Error in line {i+1} : not a valid register'
                                )
                                quit()
                        else:
                            print(
                                f'Error in line {i+1} : Invalid format of instruction'
                            )
                            quit()

                    elif lst[i][1:][0] in Instruc[3]:
                        if len(lst[i][1:]) == 3:
                            if isRegister(lst[i][1:][1]) == 0:
                                print(
                                    f'Error in line {i+1} : not a valid register'
                                )
                                quit()
                            elif isRegister(
                                    lst[i][1:]
                                [1]) == 1 and lst[i][1:][2] not in var_lst:
                                print(
                                    f'Error in line {i+1} : variable not declared'
                                )
                                quit()
                        else:
                            print(
                                f'Error in line {i+1} : Invalid format of instruction'
                            )
                            quit()

                    elif lst[i][1:][0] in Instruc[4]:
                        if len(lst[i][1:]) == 2:
                            if lst[i][1:][1] in var_lst:
                                print(
                                    f'Error in line {i+1} : Use of variable instead of label'
                                )
                                quit()
                            if (lst[i][1:][1] + ":") not in dict_label.keys():
                                print(
                                    f'Error in line {i+1} : label not declared'
                                )
                                quit()
                        else:
                            print(
                                f'Error in line {i+1} : Invalid format of instruction'
                            )
                            quit()
                else:
                    print(f'Error in line {i+1} : General Syntax Error')
                    quit()

        elif lst[i][0] == "mov" and lst[i][2][0] == "$":
            if len(lst[i]) == 3:
                if isRegister(lst[i][1]) == 0:
                    print(f'Error in line {i+1} : not a valid register')
                    quit()
                elif isRegister(lst[i][1]) == 1 and isImmediate(
                        lst[i][2]) == 0:
                    print(f'Error in line {i+1} : not a valid immediate')
                    quit()
            else:
                print(f'Error in line {i+1} : Invalid format of instruction')
                quit()

    #To seperate out mov commands as they might create problems in Instruc[] loop.
        elif lst[i][0] == "mov" and lst[i][2][0] != "$":
            if len(lst[i]) == 3:

                if isRegister(lst[i][1]) == 1 and isRegister(lst[i][2]) == 1:
                    pass
                elif lst[i][1] == "FLAGS" and isRegister(lst[i][2]) == 1:
                    pass

                elif "FLAGS" in lst[i]:
                    print(f'Error in line {i+1} : invalid use of flags')
                    quit()
                else:
                    print(f'Error in line,{i+1} : not a valid register')
                    quit()
            else:
                print(f'Error in line {i+1} : Invalid format of instruction')
                quit()

        elif lst[i][0] in Instruc[0] or lst[i][0] in Instruc[1] or lst[i][
                0] in Instruc[2] or lst[i][0] in Instruc[3] or lst[i][
                    0] in Instruc[4] or lst[i][0] in Instruc[5]:
            Flaag = 1
            if lst[i][0] in Instruc[0]:
                if len(lst[i]) == 4:
                    if isRegister(lst[i][1]) == 0 or isRegister(
                            lst[i][2]) == 0 or isRegister(lst[i][3]) == 0:
                        print(f'Error in line {i+1} : not a valid register')
                        quit()
                else:
                    print(
                        f'Error in line {i+1} : Invalid format of instruction')
                    quit()

            elif lst[i][0] in Instruc[1]:
                if len(lst[i]) == 3:
                    if isRegister(lst[i][1]) == 0:
                        print(f'Error in line {i+1} : not a valid register')
                        quit()
                    elif isRegister(lst[i][1]) == 1 and isImmediate(
                            lst[i][2]) == 0:
                        print(f'Error in line {i+1} : not a valid immediate')
                        quit()
                else:
                    print(
                        f'Error in line {i+1} : Invalid format of instruction')
                    quit()

            elif lst[i][0] in Instruc[2]:
                if len(lst[i]) == 3:
                    if isRegister(lst[i][1]) == 0 or isRegister(
                            lst[i][2]) == 0:
                        print(f'Error in line {i+1} : not a valid register')
                        quit()
                else:
                    print(
                        f'Error in line {i+1} : Invalid format of instruction')
                    quit()

            elif lst[i][0] in Instruc[3]:
                if len(lst[i]) == 3:
                    if isRegister(lst[i][1]) == 0:
                        print(f'Error in line {i+1} : not a valid register')
                        quit()
                    elif isRegister(
                            lst[i][1]) == 1 and lst[i][2] not in var_lst:
                        print(f'Error in line {i+1} : variable not declared')
                        quit()
                else:
                    print(
                        f'Error in line {i+1} : Invalid format of instruction')
                    quit()

            elif lst[i][0] in Instruc[4]:
                if len(lst[i]) == 2:
                    if lst[i][1] in var_lst:
                        print(
                            f'Error in line {i+1} : Use of variable instead of label'
                        )
                        quit()
                    if (lst[i][1] + ":") not in dict_label.keys():
                        print(f'Error in line {i+1} : label not declared')
                        quit()
                else:
                    print(
                        f'Error in line {i+1} : Invalid format of instruction')
                    quit()

            elif lst[i][0] in Instruc[5]:
                if len(lst[i]) == 1:

                    if i != len(lst) - 1:
                        print(
                            f"Error in line {i+1} : hlt not used as last instruction."
                        )
                        quit()
                else:
                    print(
                        f'Error in line {i+1} : Invalid format of instruction')
                    quit()

        else:
            print(f'Error in line {i+1} : General syntax error')
            quit()
    if lst[-1][0] == "hlt" or lst[-1][-1] == "hlt":
        pass
    else:
        print(f"Error in last line: hlt missing")
        quit()


#main function
dict_label = {}
var_lst = []
counter = -1
for i in fininp:
    if len(i) == 0:
        pass
    else:
        if i[0] == "var" and len(i) == 2:
            var_lst.append(i[1])
        if i[0] != "var":
            counter += 1
        if i[0][-1] == ":":
            dict_label[i[0][0::]] = counter
        if i[0] == "hlt":
            break

count = 1
l_count = lastcount()
Error()
var_lst = []

for cmd in fininp:
    if len(cmd) != 0:
        if cmd[0] == "var":
            var_lst.append(cmd[1])
        if cmd[0][-1] == ":":
            for item in Instruc:
                if cmd[1] in item:
                    if cmd[1] == "mov":
                        if cmd[3][0] == "$":
                            print(mov_B(cmd[1:]))
                        else:
                            print(mov_c(cmd[1:]))
                    else:
                        print(Call_Func(item[0], cmd[1:]))
                else:
                    pass
        if cmd[0] == "hlt":
            print(Call_Func("typeF", cmd))
            break
        elif cmd[-1] == "hlt":
            print(Call_Func("typeF", cmd[1:]))
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
                    break
                else:
                    pass
        count += 1
    else:
        pass
