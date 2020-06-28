import tkinter as tk
import horn

def getInputText(inputText):
    rawInput = inputText.get('1.0', 'end-1c')
    print(rawInput)

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
        text='开始求解',
        command=lambda : getInputText(inputText)
    )
    runButton.pack()

    hornButton = tk.Button(
        master=window,
        text="字句归结求解",
        command=lambda : horn.horn_run(inputText.get('1.0', 'end-1c'))
    )
    hornButton.pack()

    window.mainloop()