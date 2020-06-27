'''
horn子句定义的格式：
括号外大写字母开头的英文串为函数名，后面带有括号，括号内为变量与常量名
括号内非一个字母的英文串或者大写单个英文串为常量名
括号内单小写字母为变量名
推导符号用<-表示
各个函数的析取关系用,表示
变量常量之间用,分隔
A(aa,bb)<-          没有前件，只有后件，表示断言，永远成立
<-A(ab)             只有前件，没有后见，表示假设，是要求解的内容
一般的格式为 A(a,b)<-B(c,d),C(e,f)
'''

#函数的定义
class Fun:
    #函数名
    name = ""
    #函数的参数列表
    parameter = []

    def __init__(self, string):
        if string == "":
            return

        string.replace(" ", "")
        #寻找左右括弧的位置
        left_bracket_index = string.index("(")
        right_bracket_index = string.index(")")
        self.name = string[0:left_bracket_index]
        parameter_string = string[left_bracket_index + 1:right_bracket_index]
        self.parameter = parameter_string.split(",")


#子句的定义
class Clause:
    #左端函数
    left_fun = Fun("")
    #右端函数列表
    right_fun = []

    def __init__(self, string):
        if string == "":
            return

        string.replace(" ", "")
        #查找分隔符位置
        gap_index = string.index("<-")
        #获取左端函数
        self.left_fun = Fun(string[0:gap_index])
        #获取右端函数列表
        if gap_index + 2 == len(string):
            self.right_fun = []
        else:
            i = 0
            while i < len(string):
                if string[i] == ',' and string[i - 1] == ')':
                    string = list(string)
                    string[i] = '.'
                    string = "".join(string)
                i += 1
            right_string_list = string[gap_index + 2:].split(".")
            for string in right_string_list:
                self.right_fun.append(Fun(string))


#首先对于输入得到的串进行规范化处理,返回带有子句对象的列表
def deal_string(get_string: str):
    #以换行符进行分割
    string_list = get_string.split("\n")
    clause_list = []
    #在clause_list中添加子句
    for string in string_list:
        clause_list.append(Clause(string))

    return clause_list

#判断是否为变量
def is_var(string:str):
    if len(string)==1 and string.islower():
        return True
    return False

#监测两个函数是否能够匹配，认为
def match(right_fun:Fun,left_fun:Fun):
    if right_fun.name!=left_fun.name:
        return False
    if len(left_fun.parameter)!=len(right_fun.parameter):
        return False
    mm={}
    for i in range(len(right_fun.parameter)):
        if not is_var(right_fun.parameter[i]) and not is_var(left_fun.parameter[i]):
            if right_fun.parameter[i]!=left_fun.parameter[i]:
                return False
        

    return True


#clause1是推断，clause2是推论或者断言不能搞错顺序
#如果合并出现问题，返回false，如果合并出来的是停机语句，则返回true
#正常合并返回生成的新子句
def merge(clause1:Clause,clause2:Clause):
    if clause1.left_fun.name!="" or clause2.right_fun!=[]:
        return False
    ans_clause=Clause
    left_fun=clause2.left_fun
    #对于集合1的右端中的每一个集合，都去集合列表中寻找有没有可能匹配的左端
    for right_fun in clause1.right_fun:
        if match(right_fun,left_fun):
            tem_fun=Fun

            for i in range(len(right_fun.parameter)):
                if is_var(right_fun.parameter[i]) and not is_var(left_fun.parameter[i]):
                    pass
        else:
            ans_clause.right_fun.append(right_fun)          
            # for par in right_fun.parameter:
            #     if is_var(par) and !is_var()

    
    


ss = '''Father(Bob,Allan)<-
Brother(x2,x3)<-Father(x1,x2),Father(x1,x3)
Father(Bob,Nick)<-
<-Brother(Allan,Nick)'''

clause_list=deal_string(ss)

need_to_solve=[]
for clause in clause_list:
    if clause.left_fun.name=="":
        need_to_solve.append(clause)
        clause_list.remove(clause)
#目前need_to_solve中是待解决集合，clause_list是已知条件的集合
for question in need_to_solve:
    while 1:
        merge()



# for cc in clause_list:
#     print(cc.left_fun.name)
#     for kk in cc.left_fun.parameter:
#         print(kk)
#     for kk in cc.right_fun:
#         print(kk.name)
#         for mm in kk.parameter:
#             print(mm)
