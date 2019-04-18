# ML_AntiSpam

Master proyect for "Máster Universitario en Ciberseguridad", Universidad Politécnica de Madrid.

 
### Requirements

- PostFix 
- Python 3.7
- Scikit-learn

### Installation

Follow the instructions in: [postfix-filter-loop](https://github.com/MiroslavHoudek/postfix-filter-loop). Once PostFix is correctly configured to relay messages to the STMP server, reload the PostFix service 


``sudo postfix reload``

And run the python script in 

``python /path/to/filter/filter.py`` 


To see if the server and the relay are up try the command:

``sudo lsof -i -P | grep -i "listen"``

Try sending mail, it the behaviour is not as expected, check logs at (debian/ubuntu):

``/var/log/mail.log``


### Special thanks/Mentions

 Special thanks to [MiroslavHoudek](https://github.com/MiroslavHoudek) for his contribution of [postfix-filter-loop](https://github.com/MiroslavHoudek/postfix-filter-loop)
