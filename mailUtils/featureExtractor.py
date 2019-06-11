import mailparser
import datetime
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk.corpus import words

class featExt(object):
    """
    This class extracts the features of this project's model.
    """

    keys = ["origin_timezone", "hops", "has_defects", "from_user", "from_domain", "has_HTML", "has_attachment", "MIME", "Content_type", "sent_time", "words", "classification"]

    def __init__ (self, word_dict=set(words.words()), stop=set(stopwords.words('english'))):
        self.word_dict = word_dict
        self.stop = stop

    def getFeatures(self, raw_text, cls):
        parsedMail = mailparser.parse_from_string(raw_text)
        return {
            "origin_timezone": parsedMail.timezone,
            "hops": len(parsedMail.received),
            "has_defects": bool(parsedMail.defects),
            "from_user": parsedMail.from_[-1][-1].split('@')[0] if bool(parsedMail.from_) else 'None',
            "from_domain": parsedMail.from_[-1][-1].split('@')[-1] if bool(parsedMail.from_) else 'None',
            "has_HTML": bool(parsedMail.text_html),
            "has_attachment": bool(parsedMail.attachments),
            "MIME": parsedMail.headers["MIME-Version"] if "MIME-Version" in parsedMail.headers else "None",
            "Content_type": parsedMail.headers["Content-Type"].split(';')[0] if "Content-Type" in parsedMail.headers else "None",
            "sent_time": (parsedMail.date + datetime.timedelta(hours=int(parsedMail.timezone))).strftime("%H%M%S") if bool(parsedMail.date) else "None",
            "words": self._processWords(parsedMail.text_plain[0]) if bool(parsedMail.text_plain) else "_",
            "classification": cls
        }

    def _processWords(self, string):
        def getPOS(word):
            nltk2wordnet = {
                'J': wordnet.ADJ,
                'V': wordnet.VERB,
                'N': wordnet.NOUN,
                'R': wordnet.ADV
            }
            tag = nltk.pos_tag([word])[0][1][0].upper()

            return nltk2wordnet.get(tag, wordnet.NOUN)

        lemmatizer = WordNetLemmatizer()
        tokenized = [item for item in word_tokenize(re.sub("[^a-zA-Z]+", " ", string).casefold()) if item not in self.stop and item in self.word_dict]

        return ' '.join([lemmatizer.lemmatize(word, getPOS(word)) for word in tokenized])
