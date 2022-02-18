import time
import pandas as pd
from tkinter import *
from tkinter import ttk
from datetime import date
from tkinter import messagebox
from PIL import Image, ImageTk
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer


# main window
window = Tk()
window.title("Main Detection System")
window.geometry('700x500')
window.minsize(700, 500)


# progress_bar loader function
def progress():
    global progress_bar
    start_detection_btn['state'] = DISABLED
    clear_btn['state'] = DISABLED

    # progress bar
    empty_lbl.destroy()

    progress_bar = ttk.Progressbar(frame_5, length=200, mode='determinate')
    progress_bar.pack(side='bottom', padx=5,pady=5, fill='x')

    x = 0
    while(x<20):
        time.sleep(.050)
        progress_bar['value'] += 5
        x+=1
        window.update_idletasks()

# function to clear text_box input
def clear_all():
    text_box.delete(1.0, END)

# assigns spam or ham to the output
def check_result(result):
    if(result == 0):
        messagebox.showinfo(title='RESULT', message='Not Spam')
    else:
        messagebox.showwarning(title='RESULT', message='Spam')


# function to extract text from text_box and passes to model
def getTextInput():
    global empty_lbl
    text = text_box.get(1.0, END+"-1c")
    if len(text)==0:
        messagebox.showerror(title="WARNING", message= "PLEASE ENTER THE EMAIL")
        empty_lbl.destroy()
    else:
        progress()
        result = model(text)
        check_result(result)
        progress_bar.destroy()

    
    empty_lbl = Label(frame_5, text='')
    empty_lbl.pack(side='bottom', pady=4)

    start_detection_btn['state'] = NORMAL
    clear_btn['state'] = NORMAL

# creation of about_us window
def create_about_us():
    about = Toplevel()
    about.geometry('700x500')
    about.minsize(506,234)
    about.title('ABOUT US')

    about_text =  "We have created an email fraud detection system. \n In which we are going to check whether the received email is \n spam or not spam. We will be doing this\n with the help Supervised Machine Learning technique,\n more specifically by using:  \n Frontend: Python (using tkinter) \n Backend: Python.Algorithm: Naive Bayes Algorithm \n Libraries: Pandas, Scikit-Learn, Numpy"
    about_lbl = Label(about, text=about_text, font=20)
    members_text =  "TEAM MEMBERS\n 1. Anirudh Verma   2. Shubhankar Mittal\n  3. Chandan Singh Rawat  4. Yash Bansal"
    members_lbl = Label(about, text=members_text, font=30)

    about_lbl.pack(fill='x', expand=True)
    members_lbl.pack(fill='x', expand=True, side='bottom')

def create_tips_window():
    tips = Toplevel()
    tips.geometry('700x500')
    tips.minsize(506,330)
    tips.title('TIPS')
    tips.configure(pady=30)

    frame = Frame(tips)
    frame.pack(expand=True)

    tips_text =  "Here are some techniques you can use to identify whether the email you received is Spam or not:"
    tip1 = "1. Carefully look at the sender's email address to check that the email is sent from a valid email id (fraud email id generally contains illogical domain name)."
    tip2 = "2. Emails that says you have won lottery or hit a jackpot and you need to fill your bank details to claim that reward are for sure fraud. Because a legitimate email will never asks you to enter your bank details like PIN, etc."
    tip3 = "3. Verify the authenticity of any link that the email contains. Spam emails generally contains links that can install malware on our devices once you click on them."
    
    lbl_1 = Label(frame, text=tips_text, wraplength=450, justify='left', font=10)
    lbl_1.pack(fill='x', pady=5)
    lbl_2 = Label(frame, text=tip1, wraplength=450, justify='left', font=10)
    lbl_2.pack(fill='x', pady=5)
    lbl_3 = Label(frame, text=tip2, wraplength=450, justify='left', font=10)
    lbl_3.pack(fill='x', pady=5)
    lbl_4 = Label(frame, text=tip3, wraplength=450, justify='left', font=10)
    lbl_4.pack(fill='x', pady=5)

def create_info_window():
    info = Toplevel()
    info.geometry('700x500')
    info.minsize(506,300)
    info.title('INFO')

    spam_definition =  "What is a SPAM Email?"
    spam_definition_lbl = Label(info, text=spam_definition, font=10)
    spam_definition_lbl.pack(fill='x', expand=True)

    spam_definition_ans = "SPAM emails also referred to as JUNK EMAILS are unwanted or illegitimate emails that are sent in order to lure user into a traps that may lead to a money fraud or credential fraud if not dealed in proper manner.These Types of emails may also contain Viruses or Spywawre in them which can seriously compromise the user's or victim's system."
    spam_definition_ans_lbl = Label(info, text=spam_definition_ans, font=10, wraplength=500, justify='center')
    spam_definition_ans_lbl.pack()
    
    spam_example =  "Example of Spam Email:"
    spam_example_ex = "We are sorry to inform you but your account has been blocked due to some policy violations.To unblock your account please download the file attached and fill the login and account details!"
    spam_example_lbl = Label(info, text=spam_example, font=10, underline=True)
    spam_example_lbl.pack(fill='x', expand=True)
    spam_example_ex_lbl = Label(info, text=spam_example_ex, font=10, wraplength=500, justify='center')
    spam_example_ex_lbl.pack()
    spam_report =  "If you ever fall under a cyberattack you should report it on cybercrime.gov.in as soon as possible."
    spam_report_lbl = Label(info, text=spam_report, font=10, wraplength=500, justify='center')
    spam_report_lbl.pack(fill='x', expand=True)

# model to classify emails
def model(text):
    df = pd.read_csv("spamdataset.csv")
    df['SPAM'] = df['Category'].apply(lambda x: 1 if x=='spam' else 0)
    xtrain = df.Message
    ytrain = df.SPAM
    cv = CountVectorizer()
    x_train_count = cv.fit_transform(xtrain.values)
    x_train_count.toarray()    
    model = MultinomialNB()
    model.fit(x_train_count, ytrain)
    email = list()
    email.append(text)
    email_count = cv.transform(email)
    modelresult = model.predict(email_count)
    return modelresult

# frame_1_img resizer
def resize_frame_1_img(e):
    global frame_1_img
    frame_1_img = Image.open('logo.jpg')
    frame_1_img = frame_1_img.resize((e.width, e.height), Image.ANTIALIAS)
    frame_1_img = ImageTk.PhotoImage(frame_1_img)
    frame_1_canvas.create_image(0,0, image=frame_1_img, anchor='nw')

# frame_4_img resizer
def resize_frame_4_img(e):
    global frame_4_img, frame_4_height, frame_4_width
    frame_4_height = e.height
    frame_4_width = e.width
    frame_4_img = Image.open('logo2.jpg')
    frame_4_img = frame_4_img.resize((e.width, e.height), Image.ANTIALIAS)
    frame_4_img = ImageTk.PhotoImage(frame_4_img)
    frame_4_canvas.create_image(0,0, image=frame_4_img, anchor='nw')

# image for frame_1
frame_1_img = Image.open('logo.jpg')
frame_1_img = frame_1_img.resize((250, 500), Image.ANTIALIAS)
frame_1_img = ImageTk.PhotoImage(frame_1_img)

# frame_1
frame_1 = Frame(window, height=500, width=250, bd=0, highlightthicknes=0)
frame_1.pack(side='left', fill='both', expand=True)

# canvas for frame_1
frame_1_canvas = Canvas(frame_1, width=250, height=500, bd=0, highlightthicknes=0)
frame_1_canvas.pack(fill='both', expand=True)
frame_1_canvas.create_image(0, 0, image=frame_1_img, anchor='nw')

# frame_2
frame_2 = Frame(window, height=500, width=450, bd=0, highlightthicknes=0)
frame_2.pack(side='right', fill='both', expand=True)

# frame_3
frame_3 = Frame(frame_2, height=50, width=450, bg='#1a1818', padx=5, bd=0, highlightthicknes=0)
frame_3.pack(side='top', fill='both')

# buttons for frame_3
info_btn = Button(frame_3, text='INFO', bg='#1a1818', fg='white', bd=0, highlightthicknes=0, underline=True, command=create_info_window)
tips_btn = Button(frame_3, text='TIPS', bg='#1a1818', fg='white', bd=0, highlightthicknes=0, underline=True, command=create_tips_window)
about_btn = Button(frame_3, text='ABOUT US', bg='#1a1818', fg='white', bd=0, highlightthicknes=0, command=create_about_us, underline=True)
close_btn = Button(frame_3, text='CLOSE', bg='#bd0024', fg='white', bd=0, highlightthicknes=0, command=exit, underline=True)

close_btn.pack(side='right')
about_btn.pack(side='right')
tips_btn.pack(side='right')
info_btn.pack(side='right')

# image for frame_4
frame_4_img = Image.open('logo2.jpg')
frame_4_img = frame_4_img.resize((450, 450), Image.ANTIALIAS)
frame_4_img = ImageTk.PhotoImage(frame_4_img)

# frame_4
frame_4 = Frame(frame_2, height=450, width=450, bd=0, highlightthicknes=0)
frame_4.pack(fill='both', expand=True)

# canvas for frame_4
frame_4_canvas = Canvas(frame_4, height=450, width=450, bd=0, highlightthicknes=0)
frame_4_canvas.pack(fill='both', expand=True)
frame_4_canvas.create_image(0, 0, image=frame_4_img, anchor='nw')

# frame_5
frame_5 = Frame(frame_4_canvas, padx=5, pady=10, bd=0, highlightthicknes=0)
frame_5.pack(expand=True)

# frame_6, it contains text_box_lbl, text_box, scrollbar
frame_6 = Frame(frame_5, bd=0, highlightthicknes=0)
frame_6.pack(side='top', fill='both', expand=True)

# label for text_box
text_box_lbl = Label(frame_6, text='Enter EMAIL:-')
text_box_lbl.pack(side='top', anchor='w', padx=5, pady=2)

# Textbox for email input
text_box = Text(frame_6, height=8, width=30)
text_box.pack(side='left', padx=5, fill='both', expand=True)

# scrollbar for text_box
scrollbar = Scrollbar(frame_6, command=text_box.yview)
text_box['yscroll'] = scrollbar.set
scrollbar.pack(side='right', fill='y', padx=5)

# frame_7, it contains start_detection_btn and close_btn
frame_7 = Frame(frame_5, bd=0, highlightthicknes=0)
frame_7.pack(side='bottom', padx=5, fill='x')

# start_detection button
start_detection_btn = Button(frame_7, text='START DETECTION', command=getTextInput)
start_detection_btn.pack(side='left')
# close button
clear_btn = Button(frame_7, text='CLEAR', command=clear_all)
clear_btn.pack(side='right')

# label to occupy space for progress bar
empty_lbl = Label(frame_5, text='')
empty_lbl.pack(side='bottom', pady=4)

frame_1.bind('<Configure>', resize_frame_1_img)
frame_4.bind('<Configure>', resize_frame_4_img)
window.mainloop()
