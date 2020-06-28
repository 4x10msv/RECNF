"""
普通子句集归结
输入子句的合法性需要用户自行保证
"""

import re
import copy

literalPattern = r'(~?[A-Z]\w*)\((.*)\)'
functionPattern = r'([a-z]+)\((.*)\)'
termPattern = r'([a-z]+\(.*\)|\w+)'

class Term:
    def __init__(self, rawStr):
        if re.search(functionPattern, rawStr) is not None:
            self.isFunction = True
            self.isVariable = False
            self.argNum = 0
            self.argList = []
            m = re.search(functionPattern, rawStr)
            self.funName = m.group(1)
            rawArgList = re.findall(termPattern, m.group(2))
            for rawArg in rawArgList:
                self.argList.append(Term(rawArg))
                self.argNum += 1
        else:
            self.isFunction = False
            self.isVariable = rawStr.islower()
            self.content = rawStr
    def __eq__(self, other):
        if self.isFunction:
            if not other.isFunction:
                return False
            if self.funName != other.funName:
                return False
            for i in range(0, self.argNum):
                if self.argList[i] != other.argList[i]:
                    return False
            return True
        else:
            if other.isFunction:
                return False
            return self.toString() == other.toString()
    def toString(self):
        if self.isFunction:
            result = self.funName + '('
            for i in range(0, self.argNum):
                if i != 0:
                    result += ','
                result += self.argList[i].toString()
            result += ')'
            return  result
        else:
            return self.content
    def has(self, var):
        if self.isFunction:
            if var.isFunction:
                if var == self:
                    return True
            for arg in self.argList:
                if arg.has(var):
                    return True
            return False
        else:
            return var == self
    def argSubstitute(self, subst):
        if not self.isFunction:
            return
        for i in range(0, self.argNum):
            if self.argList[i].isFunction:
                self.argList[i].argSubstitute(subst)
            else:
                if self.argList[i].toString() in subst:
                    self.argList[i] = Term(subst[self.argList[i].toString()])

class Literal:
    def __init__(self, rawStr):
        self.termNum = 0
        self.termList = []
        m = re.search(literalPattern, rawStr)
        if m.group(1)[0] == '~':
            self.predicate = m.group(1)[1:]
            self.isPositive = False
        else:
            self.predicate = m.group(1)
            self.isPositive = True
        rawTermList = re.findall(termPattern, m.group(2))
        for rawTerm in rawTermList:
            self.termList.append(Term(rawTerm))
            self.termNum += 1
    def toString(self):
        result = ''
        if not self.isPositive:
            result += '~'
        result += self.predicate + '('
        for i in range(0, self.termNum):
            if i != 0:
                result += ','
            result += self.termList[i].toString()
        result += ')'
        return result
    def contradictPredicate(self, other):
        return (self.predicate == other.predicate) and (self.isPositive != other.isPositive)
    def contradictLiteral(self, other):
        if not self.contradictPredicate(other):
            return False
        for i in range(0, self.termNum):
            if self.termList[i] != other.termList[i]:
                return False
        return True
    def unify(self, other):
        subst = {}
        firstInstance = copy.deepcopy(self)
        secondInstance = copy.deepcopy(other)
        for i in range(0, firstInstance.termNum):
            firstTerm = firstInstance.termList[i]
            secondTerm = secondInstance.termList[i]
            if secondTerm.isVariable:
                if firstTerm.isFunction and firstTerm.has(secondTerm):
                    return [False, None]
                else:
                    subst[secondTerm.toString()] = firstTerm.toString()
            elif firstTerm.isVariable:
                if secondTerm.isFunction and secondTerm.has(firstTerm):
                    return [False, None]
                else:
                    subst[firstTerm.toString()] = secondTerm.toString()
            else:
                if firstTerm != secondTerm:
                    return [False, None]
            firstInstance.substitute(subst)
            secondInstance.substitute(subst)
        return [True, subst]
    def substitute(self, subst):
        for i in range(0, self.termNum):
            if self.termList[i].isFunction:
                self.termList[i].argSubstitute(subst)
            else:
                if self.termList[i].toString() in subst:
                    self.termList[i] = Term(subst[self.termList[i].toString()])

class Clause:
    def __init__(self, rawStr):
        self.literalNum = 0
        self.literalList = []
        if rawStr == '':
            return
        rawLiteralList = rawStr.split('|')
        for rawLiteral in rawLiteralList:
            self.literalList.append(Literal(rawLiteral))
            self.literalNum += 1
    def toString(self):
        if self.literalNum == 0:
            return 'NIL'
        result = ''
        for i in range(0, self.literalNum):
            if i != 0:
                result += '|'
            result += self.literalList[i].toString()
        return result
    def resolution(self, other):
        for firstLiteral in self.literalList:
            for secondLiteral in other.literalList:
                if firstLiteral.contradictPredicate(secondLiteral):
                    result = firstLiteral.unify(secondLiteral)
                    if result[0]:
                        subst = result[1]
                        firstInstance = copy.deepcopy(self)
                        secondInstance = copy.deepcopy(other)
                        firstInstance.substitute(subst)
                        secondInstance.substitute(subst)
                        newClause = firstInstance.getNewClause(secondInstance)
                        return [True, newClause]
        return [False, None]
    def substitute(self, subst):
        for i in range(0, self.literalNum):
            self.literalList[i].substitute(subst)
    def getNewClause(self, other):
        newClauseStr = ''
        for firstLiteral in self.literalList:
            isContradict = False
            for secondLiteral in other.literalList:
                if firstLiteral.contradictLiteral(secondLiteral):
                    isContradict = True
                    break
            if (not isContradict) and (not (firstLiteral.toString() in newClauseStr)):
                newClauseStr += firstLiteral.toString() + '|'
        for firstLiteral in other.literalList:
            isContradict = False
            for secondLiteral in self.literalList:
                if firstLiteral.contradictLiteral(secondLiteral):
                    isContradict = True
                    break
            if (not isContradict) and (not (firstLiteral.toString() in newClauseStr)):
                newClauseStr += firstLiteral.toString() + '|'
        newClauseStr = newClauseStr[:-1]
        return  Clause(newClauseStr)

class ClauseSet:
    def __init__(self, rawStr):
        self.clauseNum = 0
        self.clauseList = []
        self.resHistory = {}
        rawClauseList = rawStr.split('\n')
        for rawClause in rawClauseList:
            self.clauseList.append(Clause(rawClause))
            self.clauseNum += 1
    def addClause(self, newClause):
        self.clauseList.append(newClause)
        self.clauseNum += 1
    def solve(self, maxLoopCnt = 200):
        stepCnt = 0
        loopCnt = 0
        progText = ''
        while True:
            if loopCnt > maxLoopCnt:
                #print('循环次数超过上限，程序终止')
                progText += '循环次数超过上限，程序终止\n'
                break
            self.clauseList.sort(key=lambda x: x.literalNum)
            if self.clauseList[0].literalNum == 0:
                #print('归结成功')
                progText += '归结成功\n'
                break
            isFound = False
            for i in range(0, self.clauseNum):
                for j in range(i + 1, self.clauseNum):
                    firstClause = self.clauseList[i]
                    secondClause = self.clauseList[j]
                    resTag = firstClause.toString() + ' AND ' + secondClause.toString()
                    if resTag in self.resHistory:
                        continue
                    result = self.clauseList[i].resolution(self.clauseList[j])
                    if result[0]:  ## 归结成功
                        isFound = True
                        self.addClause(result[1])
                        self.resHistory[resTag] = True
                        stepCnt += 1
                        #print(resTag)
                        #print(result[1].toString())
                        #print('----------------------')
                        progText += resTag + '\n' + result[1].toString() + '\n'
                        progText += '---------------------------------------\n'
                        break
                if isFound:
                    break
            loopCnt += 1
        return progText
    def printClauses(self):
        for clause in self.clauseList:
            print(clause.toString())

# 接口，raw为调节字符串，返回过程的字符串
def cnfResolution(rawStr):
    clauseSet = ClauseSet(rawStr)
    return clauseSet.solve()

if __name__ == '__main__':
    testStr = '''~Killer(x)|Hate(x,A)
~Killer(A)
Killer(A)|Killer(B)|Killer(C)
~Killer(c)|~Rich(c,A)
~Hate(b,A)|~Hate(b,B)|~Hate(b,C)
Rich(z,A)|Hate(B,z)'''
    print(cnfResolution(testStr))
