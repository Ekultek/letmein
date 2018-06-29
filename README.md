# letmein

Letmein is a simple easy to use password manager that that uses `AES-256` encryption to store your password in a SQLite database file with a single master password. The master password is stored in it's own seperate `.key` file under the projects home directory (`~/.letmein`), and is hashed using two million rounds of Pythons builtin `PBKDF2-HMAC-SHA-256` implementation.

# Why should I use this?

You shouldn't. The key file is stored in your home directory under `.letmein`. If someone gets access to that key file it is possible for them to change the hash to match whatever they want and decrypt your data into it's plaintext equivalent, a smarter idea would be to use a password manager that has been proven to work. However, keep in mind that if someone is able to get into your system, you have much bigger problems then getting your passwords decrypted.

# Encryption information and precautions

#### Encryption used:

- All passwords that are stored in the database use the `AES-256` cipher. The cipher key is the master password stored in the home directory. An example of what the information looks like while sitting in the database can be found below:
<img width="1574" alt="passwordsstoredandencrypted" src="https://user-images.githubusercontent.com/14183473/42105246-4a668268-7b95-11e8-813c-38758638e61a.png">

- The master password is encrypted using Pythons implementation of the `PBKDF2-HMAC-SHA-256` hashing algorithm. The password goes through two million rounds before it is stored and takes around 1.9 seconds to complete the rotation. An example of what the end result looks like can be found below:
```bash
��' }]J��3�QjT8ZDmmxuwaLKeCP-GjbW05R-V-iLsF2UAS7jdi34NHY=�����[�)��ܦ�:44
```

#### Precautions taken

- Every password is encrypted and irreversible without the master password.
- If you fail to put in the correct master password three times, all the data and files in the home directory are removed.
- Each removed file goes through three passes of random data filling, and then also goes through three passes of NULL byte filling. This makes the file practically impossible to restore (on a normal system).
- Bruteforce is possible, but each encryption takes around 1.9 seconds to complete using a normal computer.

# Example usage

Running without a command will drop you directly into the help menu:
```bash
python letmein.py
[12:44:39][FATAL] no arguments passed, dropping to help page
usage: letmein.py [-h] [-p PASSWORD] [-i INFORMATION] [-S]
                  [-s INFORMATION-STRING] [-R REGEX] [-W] [-u [INFO]]
                  [--clean]

optional arguments:
  -h, --help            show this help message and exit
  -p PASSWORD, -P PASSWORD, --password PASSWORD
                        provide a plaintext password to store
                        (*default=prompt)
  -i INFORMATION, -I INFORMATION, --info INFORMATION
                        provide information about the password to store
                        alongside (*default=prompt)
  -S, --show-all        display all stored passwords
  -s INFORMATION-STRING, --show INFORMATION-STRING
                        provided the information string stored alongside the
                        password to show the stored password
  -R REGEX, --regex REGEX
                        provided a string that will be searched as a regular
                        expression and pull all the passwords that match the
                        given expression
  -W, --store           store the provided password into the encrypted
                        database
  -u [INFO], --update [INFO]
                        update an existing password by looking for the
                        associated information string
  --clean               erase everything in the home folder
```

If there is not password stored in the key file, you will be prompted to create a new one:
```bash
python letmein.py -W
[12:45:27][PROMPT] you have not provided an encryption key, please provide one: 
[12:45:33][INFO] key has been stored successfully and securely. you will be given three attempts to successfully enter your stored key at each login, after three failed attempts all data in the programs home directory will be securely erased. you will need to re-run the application now.
```

To store a password you need to provide the `-W/--store` flag, you will be prompted for the information to identify the password along with the password itself:
```bash
python letmein.py -W
[12:47:26][PROMPT] enter your encryption key, 3 tries left: 
[12:47:30][INFO] key accepted!
[12:47:30][PROMPT] enter the information string associated with this password: ekultek/password
[12:47:38][PROMPT] enter the password to store: 
[12:47:44][INFO] password stored successfully
```

To skip the prompts you can provide either the `-i/-I/--info` flag to skip the information prompt:
```bash
python letmein.py -W -I ekultek/2ndpassword
[12:50:09][PROMPT] enter your encryption key, 3 tries left: 
[12:50:14][INFO] key accepted!
[12:50:14][PROMPT] enter the password to store: 
[12:50:22][INFO] password stored successfully
```

OR you can provide the `-p/-P/--password` flag to skip the password prompt:
```bash
python letmein.py -W -P password0988
[12:51:13][PROMPT] enter your encryption key, 3 tries left: 
[12:51:18][INFO] key accepted!
[12:51:18][PROMPT] enter the information string associated with this password: ekultek/3rdpassword
[12:51:27][INFO] password stored successfully
```

OR you can skip both and provide each at runtime:
```bash
python letmein.py -W -I ekultek/4thpassword -P password67463
[12:52:02][PROMPT] enter your encryption key, 3 tries left: 
[12:52:06][INFO] key accepted!
[12:52:08][INFO] password stored successfully
```

To show all stored passwords plaintext, you can provide the `-S/--show-all` flag:
```bash
python letmein.py -S
[12:53:26][PROMPT] enter your encryption key, 3 tries left: 
[12:53:29][INFO] key accepted!
[12:53:29][INFO] gathered 4 password(s) total
[12:53:29][INFO] decrypting stored information
------------------------------
INFO: ekultek/password                  STORED PASSWORD: password123                             
INFO: ekultek/2ndpassword               STORED PASSWORD: password54321                           
INFO: ekultek/3rdpassword               STORED PASSWORD: password0988                            
INFO: ekultek/4thpassword               STORED PASSWORD: password67463                           
------------------------------
[12:53:37][WARNING] all output is displayed in plaintext
```

You can also search a password by regular expression using the `-R/--regex` flag, the regex will search the information strings associated with each password:
```bash
python letmein.py -R th
[12:54:57][PROMPT] enter your encryption key, 3 tries left: 
[12:55:02][INFO] key accepted!
[12:55:02][INFO] a total of 1 item(s) matched your search
------------------------------
INFO: ekultek/4thpassword               STORED PASSWORD: password67463                           
------------------------------
[12:55:04][WARNING] all output is displayed in plaintext
```

To update an existing password you can pass the `-u/--update` flag along with a string that will match the information associated with the password:
```bash
python letmein.py -u th
[12:57:51][PROMPT] enter your encryption key, 3 tries left: 
[12:57:55][INFO] key accepted!
[12:57:55][INFO] 1 possible passwords found to edit
[0] ekultek/4thupdatedpassword
[12:57:55][PROMPT] choose an item to edit[0-0]: 0
[12:57:57][PROMPT] enter the new information for the update: ekultek/4thpasswordupdated
[12:58:04][PROMPT] enter the new password to update: 
[12:58:11][INFO] password updated successfully

python letmein.py -R 4th
[12:59:01][PROMPT] enter your encryption key, 3 tries left: 
[12:59:05][INFO] key accepted!
[12:59:05][INFO] a total of 1 item(s) matched your search
------------------------------
INFO: ekultek/4thpasswordupdated        STORED PASSWORD: password64756382673                     
------------------------------
[12:59:07][WARNING] all output is displayed in plaintext
```