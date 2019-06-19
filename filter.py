import smtpd
import asyncore
import smtplib
import pickle
import datetime
from mailUtils.featureExtractor import featExt


class CustomSMTPServer(smtpd.SMTPServer):
    def __init__(self, *args, **kwargs):
        super(CustomSMTPServer, self).__init__(*args, **kwargs)
        with open('./model/NBfullcsv_trained.pickle', 'rb') as handle:
            self.cls = pickle.load(handle)
        with open('./model/TfidfVectorizer_fitted.pickle', 'rb') as handle:
            self.tfidf_vec = pickle.load(handle)

    def process_message(self, peer, mailfrom, rcpttos, data, mail_options=None,
                        rcpt_options=None, fe=featExt()):

        mailfrom.replace('\'', '')
        mailfrom.replace('\"', '')

        for recipient in rcpttos:
            recipient.replace('\'', '')
            recipient.replace('\"', '')

        # print('Receiving message from:', peer)
        # print('Message addressed from:', mailfrom)
        # print('Message addressed to  :', rcpttos)
        # print('MSG >>')
        # print(data.decode())
        # print('>> EOT')

        ext_fet = fe.getFeatures(data.decode('iso-8859-15'))

        # TODO Needs to use more than just words in final version
        veridict = self.cls.predict(self.tfidf_vec
                                    .transform([ext_fet['words']]))
        # ext_fet['classification'] = 'spam' if veridict == 0 else 'ham'

        classification = veridict[0]
        print(classification)

        try:
            with open('./log/filter.log', 'a+') as output_file:
                output_file.write('Email received: ' + str(datetime.datetime.now()) + '\n')
                output_file.write(str(peer) + '\n')
                output_file.write(str(mailfrom) + '\n')
                output_file.write(str(rcpttos) + '\n')
                output_file.write(str(data.decode('iso-8859-15')) + '\n')
                output_file.write('Extracted features' + str(ext_fet) +'\n')
                output_file.write('Classification: ' + classification)
                output_file.write('\n\n\n')
                pass
        except Exception as e:
            print('Something went south')
            print(e)
            pass
        try:
            if classification == 'spam':
                print('spam email detected, not sending\n\n')
            else:
                server = smtplib.SMTP('localhost', 10026)
                server.sendmail(mailfrom, rcpttos, data)
                server.quit()
                print('send successful\n\n')
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
        except Exception as e:
            print('Undefined exception')
            print(e)
            pass
        return

server = CustomSMTPServer(('127.0.0.1', 10025), None)

asyncore.loop()
