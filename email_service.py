def form_email_body(user_name, user_email, question, email_description):
    return 'Email from: '+ user_name + '\nEmail address: '+user_email+'\nQuestion: '+ question +'\nDescription: '+ email_description


# If we want to use this feature, we should have another json file that contains email and password and igonre it by github
def send_email(message, user_email):
    gmail_user = ''
    gmail_password = ''
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    msg = 'Subject: {}\n\n{}'.format("New ticket from Chatbot", message)
    server.sendmail(gmail_user, user_email, msg)
    server.close()
    return True