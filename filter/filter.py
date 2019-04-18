#Special thanks to https://github.com/MiroslavHoudek for his contribution of https://github.com/MiroslavHoudek/postfix-filter-loop

import smtpd
import asyncore
import smtplib
import traceback
import sys
    
class CustomSMTPServer(smtpd.SMTPServer):

    def process_message(self, peer, mailfrom, rcpttos, data, mail_options=None, rcpt_options=None):

        mailfrom.replace('\'', '')
        mailfrom.replace('\"', '')

        for recipient in rcpttos:
            recipient.replace('\'', '')
            recipient.replace('\"', '')
		
        print('Receiving message from:', peer)
        print('Message addressed from:', mailfrom)
        print('Message addressed to  :', rcpttos)
        print('MSG >>')
        print(data)
        print('>> EOT')

        try:
            with open('./filter/log.txt', 'a') as output_file:
                output_file.write(str(peer))
                output_file.write('\n')
                output_file.write(str(mailfrom))
                output_file.write('\n')
                output_file.write(str(rcpttos))
                output_file.write('\n')
                output_file.write(str(data))
                output_file.write('\n\n\n')


            pass
        except:
            pass
            print('Something went south')
            print(traceback.format_exc())
        try:
            server = smtplib.SMTP('localhost', 10026)
            server.sendmail(mailfrom, rcpttos, data)
            server.quit()
            print('send successful')
        except smtplib.SMTPServerDisconnected:
            print('Exception SMTPServerDisconnected')
            pass
        except smtplib.SMTPSenderRefused:
            print('Exception SMTPSenderRefused')
            pass
        except smtplib.SMTPAuthenticationError:
            print('Exception SMTPAuthenticationError')
            pass
        except smtplib.SMTPRecipientsRefused:
            print('Exception SMTPRecipientsRefused')
            pass
        except smtplib.SMTPDataError:
            print('Exception SMTPDataError')
            pass
        except smtplib.SMTPConnectError:
            print('Exception SMTPConnectError')
            pass
        except smtplib.SMTPHeloError:
            print('Exception SMTPHeloError')
            pass
        except smtplib.SMTPResponseException:
            print('Exception SMTPResponseException')
            pass
        except smtplib.SMTPException:
            print('Exception SMTPException')
            pass
        except:
            print('Undefined exception')
            print(traceback.format_exc())
        return

server = CustomSMTPServer(('127.0.0.1', 10025), None)

asyncore.loop()