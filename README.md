# Disclaimer

This password manager is a work in progress, it is not as secure as it could be yet, use at your own risk

# letmein

Letmein is a simple easy to use password manager that that uses `AES-256` encryption to store your password in a SQLite database file with a single master password, from this master password a encryption key is generated that is never stored decrypted or seen decrypted. The generated keys length is between 100-500 characters long and is randomly generated, this key is used to encrypt the passwords. The master password's hashed content is stored in it's own separate `.pass` file under the projects home directory (`~/.letmein`), and is hashed using two million rounds of Pythons builtin `PBKDF2-HMAC-SHA-256` implementation. In order for the contents to be decrypted the master passwords hash must match the hash stored in the password file, if after three attempts the hashes do not match, the contents of the home directory is securely deleted. 

# Directory
 - [Usage](https://github.com/Ekultek/letmein/wiki/Usage)
 - [Information](https://github.com/Ekultek/letmein/wiki/Encryption-Precaution-information)
 - [Installation](https://github.com/Ekultek/letmein/wiki/Installation)
 

# Why should I use this?

You shouldn't. The password file is stored in your home directory under `.letmein`. If someone gets access to that key file it is possible for them to change the hash to match whatever they want and decrypt your data into it's plaintext equivalent, a smarter idea would be to use a password manager that has been proven to work. However, keep in mind that if someone is able to get into your system, you have much bigger problems then getting your passwords decrypted.