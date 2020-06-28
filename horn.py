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
        self.name = ""
        #函数的参数列表
        self.parameter = []
        if string == "":
            return

        string.replace(" ", "")
        string.replace("\t", "")
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
        self.left_fun = Fun("")
        #右端函数列表
        self.right_fun = []
        if string == "":
            return

        string.replace(" ", "")
        string.replace("\t", "")
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
        return {}
    if len(left_fun.parameter)!=len(right_fun.parameter):
        return {}
    #随便写的数，防止为空
    mm={1.78:2}
    for i in range(len(right_fun.parameter)):
        if not is_var(right_fun.parameter[i]) and not is_var(left_fun.parameter[i]) and right_fun.parameter[i]!=left_fun.parameter[i]:
            return {}
        if is_var(right_fun.parameter[i]):
            mm[right_fun.parameter[i]]=left_fun.parameter[i]
        elif is_var(left_fun.parameter[i]):
            mm[left_fun.parameter[i]]=right_fun.parameter[i]

    return mm


#clause1是推断，clause2是推论或者断言不能搞错顺序
#如果合并出现问题或者无法合并，返回false，如果是空子句，说明正确，返回映射
#正常合并返回生成的新子句
def merge(clause1:Clause,clause2:Clause):
    if clause1.left_fun.name!="":
        return False
    ans_clause=Clause("")
    left_fun=clause2.left_fun
    #对于集合1的右端中的每一个集合，都去集合列表中寻找有没有可能匹配的左端
    flag=0
    par_to_par_convert={}
    need_to_convert_right_fun=Fun("")
    for right_fun in clause1.right_fun:
        par_to_par_convert=match(right_fun,left_fun)
        if len(par_to_par_convert)!=0:
            flag=1
            need_to_convert_right_fun=right_fun
            break
    if flag==1:
        for i in range(len(clause1.right_fun)):
            right_fun=clause1.right_fun[i]
        #for right_fun in clause1.right_fun:
            if right_fun==need_to_convert_right_fun:   
                for clu2_right_fun in clause2.right_fun:
                    tem_fun=Fun("")
                    tem_fun.name=clu2_right_fun.name
                    for par in clu2_right_fun.parameter:
                        tem_fun.parameter.append(par_to_par_convert.get(par,par))
                    ans_clause.right_fun.append(tem_fun)
            else:
                tem_fun=Fun("")
                tem_fun.name=right_fun.name
                for par in right_fun.parameter:
                    tem_fun.parameter.append(par_to_par_convert.get(par,par))
                ans_clause.right_fun.append(tem_fun)
        if ans_clause.left_fun.name=="" and ans_clause.right_fun==[]:
            return par_to_par_convert
        return ans_clause
    else:
        return False


def horn_run(ss):

    clause_list=deal_string(ss)

    del_index=[]
    need_to_solve=[]
    for i in range(len(clause_list)):
        clause=clause_list[i]
        if clause.left_fun.name=="":
            need_to_solve.append(clause)
            del_index.append(i)
            #clause_list.remove(clause)
    cnt=0
    for i in del_index:
        clause_list.pop(i-cnt)
        cnt+=1
    #目前need_to_solve中是待解决集合，clause_list是已知条件的集合
    for q in need_to_solve:
        question_list=[q]
        while True:
            flag=0
            possible_result=[]
            for question in question_list:
                for know_clause in clause_list:
                    merge_result=merge(question,know_clause)
                    if not isinstance(merge_result,bool):
                        possible_result.append(merge_result)
                        flag=1
            if flag==0:
                print("该项错误")
                break
            else:
                question_list=possible_result
                flag=0
                for result in possible_result:
                    if isinstance(result,dict):
                        flag=1
                        print("该项正确")
                        #如果集合中有字符映射，输出对应的求解值
                        for key in result:
                            if isinstance(key,str):
                                print(key+":"+result[key])
                        break
                if flag:
                    break

'''
test1:
Father(Bob,Allan)<-
Brother(y,z)<-Father(x,y),Father(x,z)
Father(Bob,Nick)<-
<-Brother(Allan,Nick)
'''

'''
test2:
AT(dog,x)<-AT(zhangsan,x)
AT(zhangsan,train)<-
<-AT(dog,train)
'''

'''
test3:
mother(linda,bob)<-
mother(linda,john)<-
mother(linda,mary)<-
mother(mary,bill)<-
father(bob,allan)<-
father(bob,nick)<-
father(bob,kevin)<-
husband(lary,linda)<-
brother(y,z)<-mother(x,y),mother(x,z)
brother(y,z)<-father(x,y),father(x,z)
brother(x,z)<-brother(x,y),brother(y,z)
<-brother(allan,nick)
<-brother(kevin,nick)
'''

'''
test4:
cousin(x,y)<-parent(u,x),parent(v,y),brother(u,v)
parent(贾政,贾宝玉)<-
parent(贾敏,林黛玉)<-
brother(贾政,贾敏)<-
<-cousin(贾宝玉,林黛玉)
'''
