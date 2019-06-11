# ML_AntiSpam

Master proyect for "Máster Universitario en Ciberseguridad", Universidad Politécnica de Madrid.

 
### Requirements

- postfix 
- python 3.7

### Dependencies (to build the environment)

- scikit-learn
- numpy
- pandas
- pip
- mailparser
- nltk

### Installation

Follow the instructions in: [postfix-filter-loop](https://github.com/MiroslavHoudek/postfix-filter-loop). Once PostFix is correctly configured to relay messages to the STMP server, reload the PostFix service 

``sudo postfix reload``


Change working directory to ML_AntiSpam and run the python script in 

``python filter/filter.py`` 


To see if the server and the relay are up try the command:

``sudo lsof -i -P | grep -i "listen"``

Try sending mail, it the behaviour is not as expected, check logs at (debian/ubuntu):

``/var/log/mail.log``

After setting up the environment, run the script nltk_setup.py on working directory to download the necessary nltk packages as such:

``python nltk_setup.py``

### Special thanks/Mentions

 Special thanks to [MiroslavHoudek](https://github.com/MiroslavHoudek) for his contribution of [postfix-filter-loop](https://github.com/MiroslavHoudek/postfix-filter-loop)
