import tkinter as tk
from tkinter import NORMAL,DISABLED
from tkinter import scrolledtext as st
import horn
import cnf

'''
    调用horn子句归结程序
    增加窗口用于显示归结过程
    打印归结过程
'''
def horn_run_and_get_detail(s):
    #运行horn子句归结
    horn.horn_run(inputText.get('1.0', 'end-1c'))
    
    #绘制窗口
    showText = st.ScrolledText(
        master=window,
        width='50',
        height='10'
    )
    showText.pack()
    showText.config(state = NORMAL)
    #窗口插入归结过程
    
    chars1 = "请在这里放上归结过程"
    chars2 = "\n测试多行输出"
    #请在str_list中插入归结过程
    str_list = [chars1,chars2]
    for i in str_list:
        showText.insert("insert",i)
    
    #禁止用户输入
    showText.config(state = DISABLED)

'''
题目求解演示程序
输入的正确性需要由用户自行保证
progText为过程字符串
'''
def runCnfResolution(rawStr):
    progText = cnf.cnfResolution(rawStr)
    #todo
    #print(progText)

if __name__ == '__main__':
    window = tk.Tk()
    window.title('归结原理演示程序')
    window.geometry('800x600')

    inputText = tk.Text(
        master=window,
        width='50',
        height='10'
    )
    inputText.pack()

    runButton = tk.Button(
        master=window,
        text='题目求解',
        command=lambda : runCnfResolution(inputText.get('1.0', 'end-1c'))
    )
    runButton.pack()

    hornButton = tk.Button(
        master=window,
        text="horn子句归结求解",
        command=lambda : horn_run_and_get_detail(inputText.get('1.0','end-1c'))
    )
    hornButton.pack()

    window.mainloop()