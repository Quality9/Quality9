#TKinter:
from tkinter import *
from tkinter import ttk
from tkinter import font

#Web Scraping:
import requests
from bs4 import BeautifulSoup
import random

#Time:
import time
start_time = time.time()


def get_paragraph():

    #Helper Function- Removes ending of paragraph if it is a link to the full article/list
    def clean_end(paragraph):
        if paragraph[-6:] == 'e...)\n':
            return paragraph[:-19]
        elif paragraph[-6:] == 't...)\n':
            return paragraph[:-16]
        else:
            return paragraph.strip()

    #Getting the page (Main Page of Wiki, refreshed daily) using requests:
    page = requests.get("https://en.wikipedia.org/wiki/Main_Page")

    #Extract text from p tag
    soup = BeautifulSoup(page.content, 'html.parser')

    list(soup.children)

    result = []
    paragraphs = soup.find_all('p')
    #Screening out short 'paragraphs'
    for paragraph in paragraphs:
        if len(paragraph.get_text()) > 200:
            result.append(clean_end(paragraph.get_text()))
        #Choosing random paragraph
    return result[random.randint(0, len(result) - 1)]

#SET UP:
paragraph = get_paragraph()
paragraph_list = list(paragraph)

#Setting up TKinter Stuff:
root = Tk()
root.title('PyType')

my_font = font.Font(size=20)

mainframe = ttk.Frame(root)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

stats = StringVar()

ttk.Label(mainframe, textvariable=stats, font=my_font).grid(column=1, row=0)

t = Text(mainframe, width=80, height=20, wrap='word', font=my_font)
t.insert('end', paragraph)
t.grid(column=1, row=1, sticky = 'nwes')
t.tag_configure('right', background='green')
t.tag_configure('wrong', background='red')
t['state'] == 'disabled'


game_over = False

def end_game():
    global game_over
    game_over = True #Other functions need game_over to be false to occur
    t['state'] = 'normal' #TextBox needs to be editable to change it at all
    #Removing all tags
    t.tag_remove('right', '1.0', 'end')
    t.tag_remove('wrong', '1.0', 'end')
    #Removing all text
    t.delete('1.0', '1.end')
    #Making textbox uneditable again
    t['state'] = 'disabled'
    par_length = len(paragraph)
    stats.set(f"Congradulations! You finished typing {par_length} characters in {elapsed_time:.2f} seconds- that's {par_length / (elapsed_time):.2f} chars/second. You made {errors} total errors.")

index = 0
in_error = False
errors = 0
error_length = 0
next_char = paragraph_list.pop(0)

#Key-Pressing Event
def user_input(event):
    if game_over:
        return
    global index, in_error, errors, error_length, next_char

    character = event.char
    if character != '\x08' and character != '': #Checking if character is not shift or backspace
        if character == next_char: #Checking if user typed in correct character
            #Error variables (in_error and error_length) make sure that user isn't overly penalized for mistyping to characters in a row, which should just be one error but also so that the user cannot just mistype everything for completion of the text with just one error
            in_error = False
            error_length = 0
            #Adding Green Highlight and making sure player can't edit textbox
            t['state'] = 'normal'
            t.tag_add('right', f'1.{index}')
            t['state'] = 'disabled'
        else:
            if not in_error:
                errors += 1
                in_error = True
            else:
                #The player has typed at least one wrong character directly before this
                error_length += 1
                #If enough wrong characters have been typed, the next wrong character will be considered a part of a new error
                if error_length > 5:
                    error_length = 0
                    in_error = False

            #Adding error (red) highlight while keeping user from editing textbox
            t['state'] = 'normal'
            t.tag_add('wrong',f'1.{index}')
            t['state'] = 'disabled'
        index += 1
        #Getting next char to compare to next user input
        try:
            next_char = paragraph_list.pop(0)
        except:
            end_game()



    
elapsed_time = time.time()
def count():
    if game_over:
        return
    global elapsed_time
    #Elapsed time is difference between curent time and start_time 
    elapsed_time = time.time() - start_time
    stats.set(f'Errors: {errors} {' ' * 10} Seconds: {elapsed_time:.1f}')
    t.after(100, count)

#Starting Counter    
count()
#Enabling user input
root.bind('<KeyPress>', user_input)

#Enabling TKinter
root.mainloop()