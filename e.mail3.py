import imaplib
import email
from tkinter import *
import re
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from urllib.parse import urlparse
import winshell
import os
import zipfile
import shutil
def window(s):
    root = Tk()
    root.title("Warning")
    msg='\n The email from '+ str(s) +' is a phish mail \nOpen at your own risk'
    w=Label(root, text = msg) 
    w.pack()
    w = 450
    h = 100
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x=(ws/2)-(w/2)
    y=(hs/2)-(h/2)
    root.geometry('%dx%d+%d+%d' %(w,h,x,y))
    root.mainloop()

def login():
    global nameEL
    global pwordEL
    global rootA
    rootA = Tk() # This now makes a new window.
    rootA.title('Login') # This makes the window title 'login'
 
    intruction = Label(rootA, text='Please Login\n') # More labels to tell us what they do
    intruction.grid(sticky=E)
 
    nameL = Label(rootA, text='Username: ') # More labels
    pwordL = Label(rootA, text='Password: ') # ^
    nameL.grid(row=1, sticky=W)
    pwordL.grid(row=2, sticky=W)
 
    nameEL = Entry(rootA) # The entry input
    pwordEL = Entry(rootA, show='*')
    nameEL.grid(row=1, column=1)
    pwordEL.grid(row=2, column=1)
 
    loginB = Button(rootA, text='Login', command=perform_login) # This makes the login button, which will go to the CheckLogin def.
    loginB.grid(columnspan=2, sticky=W)
 
    rootA.mainloop()

def sel(url):
    browser = webdriver.Chrome()
    browser.get(url)# to open the url(link) in browser 
    time.sleep(1) # to wait for 10 secs to load the page
    username = browser.find_element_by_id("email") #to find the textbox which has the name as 'email' and store in variable
    password = browser.find_element_by_id("pass")#to find the password textbox which has a name field as "pass"
    username.send_keys("ajsfjshdjfhk") #enter fake email (random)
    password.send_keys("123456") #enter fake password(random)
    login_attempt = browser.find_element_by_xpath("//*[@type='submit']") #to find the submit button element
    login_attempt.submit() #to press submit(login)
    time.sleep(1) # wait for 10 secs to redirect the page
    o=urlparse(url)
    url_new=browser.current_url# store the url of the redirected page
    p=urlparse(url_new)
    if o.netloc!=p.netloc: #compare the previous and new urls
        return 1
    else:
        return 0
##def send_mail(urls):
##    content=''
##    for i in urls:
##        content = content+i
##        content = content+" "
##    mail = smtplib.SMTP('smtp.gmail.com',587)#smpt server and port
##    mail.ehlo()#eSMTP server(extended SMTP)
##    mail.starttls()#everything below will be encrypted (tls transport layer security)
##    mail.login('neelayrdw2@gmail.com','q1w2e3r4`')
##    mail.sendmail('neelayrdw2@gmail.com','neelayrdw1@gmail.com',content)#('from email(same as above)','receiver')
##    mail.close()#close connection
    
def perform_login():
    mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)
    mail.login(nameEL.get(),pwordEL.get())# type the username and password
    mail.list()# Out: list of "folders" aka labels in gmail.
    mail.select("inbox") # connect to inbox.
    result, data = mail.uid('search', None, "ALL") # search and return uids
    latest_email_uid = data[0].split()[-1] #to get the uid of the latest e-mail
    result, data = mail.uid('fetch', latest_email_uid, '(RFC822)') 
    raw_email = data[0][1]
    email_message = email.message_from_bytes(raw_email)
    rootA.destroy()
    #print (email_message.items())

    ################################# HTTP/HTTPS ####################################
    abc=''
    for part in email_message.walk():
        if part.get_content_type() == 'text/plain':
            abc=part.get_payload()
    print(abc)
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',abc)
##    urls=re.findall(r'"([^"]*)"', abc)
##    i=0
##    while i<len(urls):
##        if 'https' not in urls[i] and 'http' not in urls[i]:
##            urls.pop(i)
##        else:
##            i+=1
##    for i in urls:
##        for j in i:
##            if j=='=' or j=='/r' or j=='/n':
##                newstr = i.replace(j, "")
##                print(newstr)
##                i=newstr
    print(urls)
    #urls='http://facebook-it.byethost12.com/?id=facebook'
    #s=sel(urls)
    for i in urls:
        print (i)
        s=sel(i)
        if s==1:
            window(email.utils.parseaddr(email_message['From']))
            break
            sys.exit()
        
 
    ################################# ATTACHMENTS ####################################

    for part in email_message.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
    fileName = part.get_filename()# to get the name of the attachment
    if fileName:
        ext=['.ade', '.adp','.bat','.chm','.cmd','.com','.cpl','.exe','.hta','.ins','.isp','.jar','.jse','.lib','.lnk','.mde','.msc','.msp','.mst','.pif','.scr','.sct','.shb','.sys','.vb','.vbe','.vbs','.vxd','.wsc','.wsf','.wsh']
        for i in ext:
            if i in fileName:
                window(email.utils.parseaddr(email_message['From']))
                break
                sys.exit()
        if '.zip' in fileName:
            dirt="D:\\fun\\" #destination directory where the attachment will be downloaded
            att_path = os.path.join(dirt, fileName)
            if not os.path.isfile(att_path): #to check if the attachment is already downloaded in the destination folder
                fp = open(att_path, 'wb')
                fp.write(part.get_payload(decode=True))
            fp.close()
            zip_ref = zipfile.ZipFile(dirt+fileName,'r')
            l=zip_ref.namelist() # to store the name of all the files which were in the zip file
            zip_ref.close()
            for i in ext:
                if i in l:
                    window(email.utils.parseaddr(email_message['From']))
                    break
                    sys.exit()
login()
