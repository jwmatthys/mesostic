# mesostic maker
# copyright 2012 by Joel Matthys
# released under GPL license

from re import split
from Tkinter import *
import tkFileDialog
from random import choice

def drunk_constrain (prev, low, high):
    val = prev + choice([-1, 0, 1])
    if val < low:
        return low
    if val > high:
        return high
    return val

def load_text():
    root.infile = tkFileDialog.askopenfilename()
    print 'infile: '+root.infile
    tempname = root.infile
    tempname = tempname.lower()
    tempname = tempname.split('/')[-1]
    tempname = ''.join(i for i in tempname if i.islower() or i in '-_.')
    fname.set(tempname)

def clean_text(input):
    output = input.lower() # lowercase
    output = output.replace('\n',' ') # change newlines to spaces
    output = output.replace('\r',' ') # change CRs to spaces
    output = output.replace('\t',' ') # change tabs to spaces
    output = ''.join(i for i in output if i.islower() or i in '-\' ')
    for _ in range(20):
        output = output.replace('  ',' ') # get rid of extra spaces
    return output

def go_mesostic():
    tex.delete(1.0,END)
    if indent_in.get() == '':
        max_indent = 42
    else:
        max_indent = int (indent_in.get())
    if max_indent <= 0:
        max_indent = 42
    if root.infile == None:
        tex.insert(END,'--- no input text selected ---')
    elif spine_in.get() == '':
        tex.insert(END,'--- no spine chosen ---')
    else:
        s = open(root.infile, 'r').read()
        root.title(root.infile)
        cleaned_text = clean_text(s)
        tokens = cleaned_text.split(' ')
        textlen = len(tokens)

        spine = spine_in.get()
        spine = clean_text(spine)
        spine_tokens = spine.split(' ') # individual words of spine
        spine = ''.join(i for i in spine if i.islower())

        # set outfile name, open outfile
        outfile = root.infile
        outfile = outfile.lower()
        outfile = outfile.split('/')[-1]
        if '.' in outfile:
            outfile = outfile.split('.')[-2]
        outfile = ''.join(i for i in outfile if i.islower())
        outfile += '_mesostic.txt'
        output = open(outfile, 'w')
        tex.insert(END,'\n')

        # FIX LATER: wing lengths
        leftwinglen = int (lwing_in.get())
        rightwinglen = int (rwing_in.get())
        tolerance = int (tolerance_in.get())
        max_leftwinglen = 2 * leftwinglen
        max_rightwinglen = 2 * leftwinglen
        spine_index = 0
        previousletter = '@'
        currentletter = spine[0]
        nextletter = spine[1]

        # here we go!
        first_token_of_line = 0
        while (first_token_of_line < textlen - (leftwinglen + rightwinglen + 1)):
            wing_fail = False
            spineword_found = False
            testpos = first_token_of_line
            
            for _ in range (0, leftwinglen - tolerance):
                testword = tokens[testpos]
                if currentletter in testword: # fail, spine letter found in L wing
                    wing_fail = True
                if previousletter in testword: # fail, prev letter found in L wing
                    wing_fail = True
                testpos += 1
            
            if (not wing_fail):
                # So far so good; check next couple of words for possible spine
                words_to_check = 2 * tolerance
                
                while (words_to_check > 0 and spineword_found == False):
                    testword = tokens[testpos]
                    # check if testword is one of the actual spine words
                    for spinetest in spine_tokens:
                        if testword == spinetest:
                            spineword_found = False
                    if currentletter in testword:
                        c = testword.find(currentletter)
                        if previousletter in testword and not (previousletter == currentletter):
                            p = testword.find(previousletter)
                            if p < c:
                                wing_fail = True
                        if nextletter in testword and not (nextletter == currentletter):
                            n = testword.find(nextletter)
                            if n > c:
                                wing_fail = True
                        spineword_found = True                                
                    words_to_check = words_to_check - 1
                    testpos += 1

            if (spineword_found):
                # Another hurdle passed
                for _ in range (0, rightwinglen - tolerance):
                    testword = tokens[testpos]
                    if currentletter in testword: # fail, spine letter found in R wing
                        wing_fail = True
                    if nextletter in testword: # fail, next letter found in R wing
                        wing_fail = True
                    testpos +=  1

            # WIN! We found an eligible line. Now, first let's see if the next
            # word or words (tolerance) also fit. This is a bonus.
            if (spineword_found and not wing_fail):
                words_to_check = tolerance
                bonus = True
                while (words_to_check > 0 and bonus == True):
                    testword = tokens[testpos]
                    if currentletter in testword:
                        bonus = False
                    if nextletter in testword:
                        bonus = False
                    testpos += 1
                    words_to_check = words_to_check - 1

                if (drunk.get() == 1):
                    leftwinglen = drunk_constrain (leftwinglen, 1, max_leftwinglen)
                    rightwinglen = drunk_constrain (rightwinglen, 1, max_rightwinglen)

                output_line = ''
                for word in range(first_token_of_line, testpos - 1):
                    output_line = output_line + tokens[word] + ' '

                spine_pos = output_line.find(currentletter)
                indent = max_indent - spine_pos
                if indent > 0:
                    output_line = ' ' * indent + output_line[:spine_pos] + currentletter.upper() + output_line[spine_pos+1:-1] + '\n'
                tex.insert(END,output_line)
                output.write(output_line)
                spine_index += 1
                first_token_of_line = testpos

                # newline if end of spine
                if spine_index >= len(spine):
                    output.write('\n')
                    tex.insert(END,'\n')
                    spine_index = 0

                # establish current, next, and previous letter
                currentletter = spine[spine_index]
                nextletter = spine[(spine_index + 1) % len(spine)]
                if (spine_index > 0):
                    previousletter = spine[spine_index-1]
                else:
                    previousletter = spine[len(spine)-1] # last letter
            else: # spineword not found or wing fail
                first_token_of_line += 1

        # color spine word red
        for i in range(int(float(tex.index(END)))):
            tex.tag_add(tex.index(END),i+max_indent/100.0)
            tex.tag_config(tex.index(END),foreground='red')
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
f_in = Button(root,text='Find Text File',command=load_text)
fname = StringVar()
fname.set("No File Selected")
fname_label = Label(root,textvariable=fname)
spine_label = Label(root,text='Enter Spine Word:')
spine_in = Entry(root, justify=CENTER)
lwing_label = Label(root,text='Enter L Wing Size:')
lwing_in = Entry(root, justify=CENTER)
lwing_in.insert(0, '4')
rwing_label = Label(root,text='Enter R Wing Size:')
rwing_in = Entry(root, justify=CENTER)
rwing_in.insert(0, '4')
tolerance_label = Label(root,text='Enter Tolerance:')
tolerance_in = Entry(root, justify=CENTER)
tolerance_in.insert(0, '1')
drunk = IntVar()
toggle_drunk = Checkbutton(root, text="Vary Randomly", variable=drunk)
indent_label = Label(root,text='Enter Indent:')
indent_in = Entry(root, justify=CENTER)
indent_in.insert(0,'61')
dummy_label = Label(root,text='------------')
end = Button(root,text='Exit',command=exit)
title = Label(root,text='Mesostic Generator',bg='red',fg='white')

scroll.pack(fill=Y,side=RIGHT)
tex.pack(fill=BOTH,side=RIGHT,expand=1)
title.pack(side=TOP,fill=X,pady=10)
f_in.pack(side=TOP)
fname_label.pack(side=TOP)
spine_label.pack(side=TOP)
spine_in.pack(side=TOP)
lwing_label.pack(side=TOP)
lwing_in.pack(side=TOP)
rwing_label.pack(side=TOP)
rwing_in.pack(side=TOP)
toggle_drunk.pack()
tolerance_label.pack(side=TOP)
tolerance_in.pack(side=TOP)
indent_label.pack(side=TOP)
indent_in.pack(side=TOP)
b.pack(side=TOP,fill=X,expand=Y)
end.pack(side=BOTTOM,fill=X)

mainloop()
