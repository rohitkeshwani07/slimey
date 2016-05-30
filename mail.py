import smtplib
import sys

# Specifying the from and to addresses

fromaddr = 'rohitkeshwani07@gmail.com'
toaddrs  = 'rohitkeshwani07@gmail.com'

# Writing the message (this message will appear in the email)

msg = str(sys.argv[1])

# Gmail Login

username = 'postmaster@sandboxf7c644d3e8994485a7207039a70287fe.mailgun.org'
password = 'db477bcc645ead1e548ffd78f328c84d'

# Sending the mail  

server = smtplib.SMTP('smtp.mailgun.org:587')
server.starttls()
server.login(username,password)
server.sendmail(fromaddr, toaddrs, msg)
server.quit()