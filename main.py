from tkinter import *
from tkinter.messagebox import *
import math
import threading
import os

try:
    from audio import audiof
    ob = audiof()
    AUDIO_AVAILABLE = True
except ImportError:
    ob = None
    AUDIO_AVAILABLE = False
    print("Audio module not available - running without audio support")

font = ('Times New Roman', 20, 'bold')
audiomode = False
normalcalc = True

def toggleaudiomode():
    global audiomode
    if not AUDIO_AVAILABLE:
        showerror("Audio Error", "Audio module not available")
        return
    
    audiomode = not audiomode
    if audiomode:
        print("Audio mode enabled")
        if ob:
            ob.speak('Audio mode enabled')
    else:
        print("Audio mode disabled")
        if ob:
            ob.speak('Audio mode disabled')

def speak_text(text):
    """Thread-safe audio speaking"""
    if audiomode and ob:
        ob.speak(text)

def clickbtn(event):
    print("Button clicked")
    b = event.widget
    text = b['text']
    print(text)
    
    if audiomode and ob:
        ob.speak(text)
    
    if text == 'x':
        textfield.insert(END, '*')
        return
    
    if text == '=':
        try:
            ex = textfield.get()
            if not ex.strip():
                return
            answer = eval(ex)
            textfield.delete(0, END)
            textfield.insert(0, str(answer))
        except ZeroDivisionError:
            showerror("Error", "Division by zero")
            textfield.delete(0, END)
        except Exception as e:
            print("Error", e)
            showerror("Error", "Invalid expression")
            textfield.delete(0, END)
        return
    
    textfield.insert(END, text)

def allclear():
    textfield.delete(0, END)
    if audiomode and ob:
        ob.speak('AC')

def clr():
    ex = textfield.get()
    if ex:
        ex = ex[:-1]
        textfield.delete(0, END)
        textfield.insert(0, ex)
    if audiomode and ob:
        ob.speak('<--')

def calcscientific(event):
    btn = event.widget
    text = btn['text']
    ex = textfield.get()
    
    if audiomode and ob:
        ob.speak(text)
    
    ans = ''
    try:
        if text == '^':
            if ',' in ex:
                base, pow_val = ex.split(',')
                ans = str(math.pow(float(base), float(pow_val)))
            else:
                showerror("Error", "Use format: base,power")
                return
        elif text == 'x!':
            num = float(ex)
            if num < 0 or num != int(num):
                showerror("Error", "Factorial only for non-negative integers")
                return
            ans = str(math.factorial(int(num)))
        elif text == 'rad':
            ans = str(math.radians(float(ex)))
        elif text == '√':
            num = float(ex)
            if num < 0:
                showerror("Error", "Cannot take square root of negative number")
                return
            ans = str(math.sqrt(num))
        elif text == 'x°':
            ans = str(math.degrees(float(ex)))
        elif text == 'sin(x)':
            ans = str(math.sin(math.radians(float(ex))))
        elif text == 'cos(x)':
            ans = str(math.cos(math.radians(float(ex))))
        elif text == 'tan(x)':
            ans = str(math.tan(math.radians(float(ex))))
        elif text == 'ln':
            num = float(ex)
            if num <= 0:
                showerror("Error", "Natural log undefined for non-positive numbers")
                return
            ans = str(math.log(num))
        elif text == 'e^x':
            ans = str(math.exp(float(ex)))
        elif text == 'π':
            ans = str(math.pi)
        elif text == 'e':
            ans = str(math.e)
    except ValueError:
        showerror("Error", "Invalid input")
        return
    except Exception as e:
        print("Error", e)
        showerror("Error", str(e))
        return

    textfield.delete(0, END)
    textfield.insert(0, ans)

def sciclick():
    global normalcalc
    if normalcalc:
        frame.pack_forget()
        sciframe.pack(side=TOP)
        frame.pack(side=TOP, pady=20)
        sciframe.config(bg='gray')
        window.geometry('480x650')
        print('show scientific')
        normalcalc = False
        if ob:
            ob.speak('Scientific mode enabled')
    else:
        sciframe.pack_forget()
        window.geometry("450x480")
        print('show normal')
        normalcalc = True
        if ob:
            ob.speak('Scientific mode disabled')

def enterclick(event):
    """Handle Enter key press"""
    try:
        ex = textfield.get()
        if not ex.strip():
            return
        answer = eval(ex)
        textfield.delete(0, END)
        textfield.insert(0, str(answer))
    except ZeroDivisionError:
        showerror("Error", "Division by zero")
        textfield.delete(0, END)
    except Exception as e:
        showerror("Error", "Invalid expression")
        textfield.delete(0, END)

window = Tk()
window.title("Calculator")
window.geometry("450x480")
window.config(bg='lightgray')

try:
    if os.path.exists('imgg/keys.png'):
        img = PhotoImage(file='imgg/keys.png')
        imgwidth = 40
        imgheight = 40
        img = img.subsample(max(1, img.width() // imgwidth), max(1, img.height() // imgheight))
        headlabel = Label(window, image=img, bg='lightgray')
        headlabel.pack(side=TOP, pady=15)
    else:
        print("Image file not found: imgg/keys.png")
except Exception as e:
    print(f"Error loading image: {e}")

heading = Label(window, text='CALCULATOR', font=font, fg='darkblue', bg='lightgray')
heading.pack(side=TOP)

textfield = Entry(window, font=font, justify=CENTER, bg='white', bd=2)
textfield.pack(side=TOP, pady=10, fill=X, padx=10)

frame = Frame(window, bg='lightgray')
frame.pack(side=TOP, pady=20)

buttons = [
    ('1', 0, 0), ('2', 0, 1), ('3', 0, 2),
    ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
    ('7', 2, 0), ('8', 2, 1), ('9', 2, 2),
    ('0', 3, 1), ('.', 3, 0), (',', 4, 0),
    ('=', 3, 2), ('+', 0, 3), ('-', 1, 3),
    ('x', 2, 3), ('/', 3, 3)
]

for (text, row, column) in buttons:
    btn = Button(
        frame, 
        text=text, 
        font=font, 
        width=6, 
        relief='raised', 
        bg='lightblue', 
        fg='black', 
        activebackground='yellow', 
        activeforeground='black'
    )
    btn.grid(row=row, column=column)
    btn.bind('<Button-1>', clickbtn)

clearbtn = Button(
    frame, 
    text='<--', 
    font=font, 
    width=6, 
    relief='raised', 
    bg='lightcoral', 
    fg='black', 
    activebackground='red', 
    activeforeground='white', 
    command=clr
)
clearbtn.grid(row=4, column=1)

allclrbtn = Button(
    frame, 
    text='AC', 
    font=font, 
    width=13, 
    relief='raised', 
    bg='lightcoral', 
    fg='black', 
    activebackground='red', 
    activeforeground='white', 
    command=allclear
)
allclrbtn.grid(row=4, column=2, columnspan=2)

textfield.bind('<Return>', enterclick)

sciframe = Frame(window, bg='gray')

sci_buttons = [
    ('√', 0, 0), ('^', 0, 1), ('x!', 0, 2), ('rad', 0, 3),
    ('x°', 1, 0), ('sin(x)', 1, 1), ('cos(x)', 1, 2), ('tan(x)', 1, 3),
    ('ln', 2, 0), ('e^x', 2, 1), ('π', 2, 2), ('e', 2, 3)
]

for (text, row, column) in sci_buttons:
    btn = Button(
        sciframe, 
        text=text, 
        font=font, 
        width=6, 
        relief='raised', 
        bg='darkslategray', 
        fg='white', 
        activebackground='lightgray', 
        activeforeground='black'
    )
    btn.grid(row=row, column=column, padx=2)
    btn.bind('<Button-1>', calcscientific)

menubar = Menu(window)

mode = Menu(menubar, tearoff=0)
mode.add_checkbutton(label='Scientific Calculator', command=sciclick)
if AUDIO_AVAILABLE:
    mode.add_checkbutton(label='Audio mode', command=toggleaudiomode)

menubar.add_cascade(label='Mode', menu=mode)
window.config(menu=menubar)

textfield.focus_set()

window.mainloop()
