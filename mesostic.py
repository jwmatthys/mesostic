# mesostic maker
# copyright 2012 by Joel Matthys
# released under GPL license

from re import split
from Tkinter import *
import tkFileDialog as openpanel

def load_text():
    root.infile = openpanel.askopenfilename()
    print 'infile: '+root.infile

def go_mesostic():
    tex.delete(1.0,END)
    if root.infile == None:
        tex.insert(END,'--- no input text selected ---')
    elif spine_in.get() == '':
        tex.insert(END,'--- no spine chosen ---')
    else:
        f = open(root.infile, 'r')
        s = f.read()
        s = s.lower()
        s = s.replace('\n',' ')
        s = s.replace('\r',' ')
        s = s.replace('\t',' ')
        cleaned_text = ''.join(i for i in s if i in 'abcdefghijklmnopqrstuvwxyz-\' ')

# silly little function to remove extra spaces
        for _ in range(10):
            cleaned_text = cleaned_text.replace('  ',' ')
        tokens = cleaned_text.split(' ')
        textlen = len(tokens)

        spine = spine_in.get()
        spine = spine.lower()
        spine = ''.join(i for i in spine if i in 'abcdefghijklmnopqrstuvwxyz')
        max_indent = 36
        max_phraselen = 6

        spine_index = 0
        winglen = 0
        wing = ''
        found = False
        foundNext = False
        outfile = root.infile+'.mesostic.txt'
        output = open(outfile, 'w')

        for word in tokens:
            wing = wing + word + ' '
            winglen += 1

            if winglen >= max_phraselen or foundNext:
                if found == True:
                    spine_pos = wing.find(spine[spine_index])
                    indent = max_indent - spine_pos
                    if indent >= 0:
                        textline =  ' ' * indent + wing[:spine_pos] + spine[spine_index].upper() + wing[spine_pos+1:] + '\n'
                        output.write(textline)
                        tex.insert(END,textline)
                        spine_index += 1

                    wing = ''
                    winglen = 0
                    found = False
                    foundNext = False
                    if spine_index >= len(spine):
                        output.write('\n')
                        tex.insert(END,'\n')
                        spine_index = 0

                if spine[spine_index] in wing:
                    if found:
                        foundNext = True
                    found = True

        print "wrote mesostic to "+outfile
    output.close()

# Tk window setup
root = Tk()
root.title("Mesostic Generator")
root.infile = None
scroll = Scrollbar(root)
tex = Text(root)
tex.config(width=90, yscrollcommand=scroll.set, wrap=WORD)
scroll.config(command=tex.yview)
b = Button(root,text='Create Mesostic',command=go_mesostic)
f_in = Button(root,text='Find Text',command=load_text)
spine_label = Label(root,text='Enter Spine:')
spine_in = Entry(root)
dummy_label = Label(root,text='------------')
end = Button(root,text='Exit',command=exit)
title = Label(root,text='Mesostic Generator',bg='red',fg='white')

tex.pack(fill=BOTH,side=RIGHT,expand=1)
scroll.pack(fill=Y,side=RIGHT)
title.pack(side=TOP,fill=X,pady=10)
f_in.pack(side=TOP)
spine_label.pack(side=TOP)
spine_in.pack(side=TOP)
b.pack(side=TOP,fill=X,expand=Y)
end.pack(side=BOTTOM,fill=X)

mainloop()
