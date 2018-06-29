# letmein

Letmein is a light weight easy to use password manager that stores your passwords with AES-256 encryption into a sqlite3 database file. The database file itself when looked at looks something like this:

<img width="1581" alt="databasefile" src="https://user-images.githubusercontent.com/14183473/42097397-abc213fa-7b7d-11e8-92d4-19f3f9848892.png">

In order to decrypt the AES ciphers you will need the hashed master password that is stored in `~/.letmein/.key`. An example of the hashed password looks like this:

```bash
���M���c�3�^(rtmSQYNPHDCtbZYuyUXn1g8mRmfaZkjEk08nI_L4G214=�l���4�A�E�M�{:44
```

The hashed master password is sent through two million rounds of Pythons built-in `PBKDF2-HMAC-SHA-256` implementation, it will take around 1.9 seconds in order for hashing to complete:

```python
def sha256_rounds(raw, rounds=2000000, salt="vCui3d8,?j;%Rm#'zPs'Is53U:43DS%8rs$_FBsrLD_nQ"):
    obj = hashlib.pbkdf2_hmac
    return obj("sha256", raw, salt, rounds)
```

You are given three chances to enter the password, if you are unable to enter the master password in three chances all data stored in the projects home directory (`~/.letmein`) is securely deleted by filling (3 passes) each file in the home directory with random bytes, and taking another pass with NULL bytes:

```python
def secure_delete(path, random_fill=True, null_fill=True, passes=3):
    with open(path, "wr") as data:
        length = data.tell()
        if random_fill:
            for _ in xrange(passes):
                data.seek(0)
                data.write(os.urandom(length))
        if null_fill:
            for _ in xrange(passes):
                data.seek(0)
                data.write("\x00" * length)
    os.remove(path)
```

The point if this project is to better understand how hashing works and how password managers work. This project is not complete and is not ready for use (I highly recommend you use a well known password manager over this one). It is being stored on Github for review access.

# Example usage:

Displaying all passwords currently stored in the database:

```bash
(letmein) TBG-a0216:letmein admin$ python letmein.py -S
[09:12:52][PROMPT] enter your encryption key, 3 tries left: 
[09:12:57][INFO] key accepted!
[09:12:57][INFO] gathered 6 password(s) total
[09:12:57][INFO] decrypting stored information
------------------------------
INFO: some 2random info                 STORED PASSWORD: this is a testing password1             
INFO: some 7random info                 STORED PASSWORD: this is a test password2                
INFO: some random test info             STORED PASSWORD: this is a test password2                
INFO: some random test info             STORED PASSWORD: this is a test password2                
INFO: some random test info             STORED PASSWORD: this is a test password2                
INFO: some random test info             STORED PASSWORD: this is a test password2                
------------------------------
[09:13:09][WARNING] all output is displayed in plaintext
(letmein) TBG-a0216:letmein admin$ 
```

Storing a password:

```bash
(letmein) TBG-a0216:letmein admin$ python letmein.py -W
[09:14:45][PROMPT] enter your encryption key, 3 tries left: 
[09:14:50][INFO] key accepted!
[09:14:50][PROMPT] enter the information string associated with this password: this is a password storing teset
[09:15:01][PROMPT] enter the password to store: 
[09:15:08][INFO] password stored successfully
(letmein) TBG-a0216:letmein admin$ 
```

Displaying all passwords that match a regular expression:

```bash
(letmein) TBG-a0216:letmein admin$ python letmein.py -R test
[09:15:39][PROMPT] enter your encryption key, 3 tries left: 
[09:15:43][INFO] key accepted!
[09:15:43][INFO] a total of 4 item(s) matched your search
------------------------------
INFO: some random test info             STORED PASSWORD: this is a test password2                
INFO: some random test info             STORED PASSWORD: this is a test password2                
INFO: some random test info             STORED PASSWORD: this is a test password2                
INFO: some random test info             STORED PASSWORD: this is a test password2                
------------------------------
[09:15:51][WARNING] all output is displayed in plaintext
(letmein) TBG-a0216:letmein admin$ 
```
