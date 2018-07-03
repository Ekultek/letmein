# Disclaimer

This password manager is a work in progress, it is not as secure as it could be yet, use at your own risk

# letmein

Letmein is a lightweight password manager that uses `AES-256` encryption to encrypt passwords and store them into a SQLite database file. The encryption is done via a pseudo random master key generated from a master password who's hash value is stored using two million rounds of Pythons implementation of `PBKDF2-HMAC-SHA-256`. I am so confident with the password encryption that below is my Github password ciphered using the programs `AES-256` implementation;

```bash
Hc24aS3k9WJ6x53UZzm88b0JdAHjNWcY5Q1Lr0XjgAQ=
```

If you can crack it, you can have my Github, no strings attached.

The encryption key is generated using half of the provided master password and a contingent length of 200-1000 pseudo random characters, along with 78 bytes of salt. An example of a deciphered encryption key generated from a weak password such as `password` would look like this:

```bash
$letmein$pass`9OVp.PZdubh8p^cE
                              w)5W7U81-9_Z|
                                           cj45un"RS7!mvUr(6@1H-f8&:9E^p
%p.sw\2wgkREQ}U[jEk* SakBJ
) DAXe4voZ6Q@KV3dGG7Oj[M  *%GPZv1bn]@I{[g]<A'5q<;ns9*) %        10UW]
f,5}Mf+A2xrB\QEH9s.=lRmgI)::}>Y^I-N]dkOnQ^]<Z.A`G-`j0&4,QEpI<|;kB_^}]Sw>|R]AqCI
FJy     hYyC
            :<{DtLj'$"<?I<
3a[HvF|"ro5Ky)K<n"06jhh
                   Mx6BdU+Y .6PUX
                                 B[Mz]|5' ?_\
                                             q<:7*JEIwKG*/hRiv6Vzv]w)?6t>9]Q:Od|        kD6pRBt\!UIys#gV#S@<4?#]3ezZ@yDJ=       K^tStj.uZ|2!s/b_)Gu=NP3T3[ff(>Nj[k
O'oj6q_&9y+"C1u0j
"'"Op_1
       i5f0uxD^#<TpP2{Pt6uwz:f2EXxf.S:T
                                       ,D~69?3&\U*(bC<qSDQ_I#^sKB
nU/[Z;7K
        C2JtBiVHxz'kIS.W/`^/o%3A)/
                                  M`=;>E(s8yjQ
/fL(*;NX^$nmU9WT9[XCh&Fc(4cb)%>)Z*IJ          _ =][[g~,J
                                    Y@I;aJ%V"#uP]|m\"   k{4(r!JMpGu|X
                                                                     J4;MQ<yJ]/@pt
v^cH02b(Mj0BF[hrQK,mf*l=qH[HNz^Vj:E$q7;cy`
      eh=Ng-$z/!?1~1LwZY
                        |Zd`AeV*>=(e[,)C/
                                         Io0VRhY#SmbkxM PpO2S/Iep'S-G,Gj ~,-Vg*d[)?Yjlq.UY*9mtF:G
                                                                                                 AjjkX<y6Hf.DdVj'b+BCz(Q12='>L5iqG*I`Eeeg2@,?Mas^F,
                                                                                                                                                   4
                                                                                                                                                    c8tJ`2I9v=LYQ;Mv]+9[D       Flq0*SsKL&XW 
q_.\#;ByA#.
4"c&8e<\G]5T0A
              Lhs61\T   f}N9y"$vD��5jӨ�Z�L�8��Q�K2hK�乯y�Ҥ��X;ۭ�/���G�:�d�"��h����.��Zc:�
                                                                                         ]��`

```

This encryption key will be used as the cipher key to encrypt each password stored in the SQLite database file.

# Directory
 - [Usage](https://github.com/Ekultek/letmein/wiki/Usage)
 - [Information](https://github.com/Ekultek/letmein/wiki/Encryption-Precaution-information)
 - [Installation](https://github.com/Ekultek/letmein/wiki/Installation)
 

# Why should I use this?

You shouldn't. The password file is stored in your home directory under `.letmein`. If someone gets access to that key file it is possible for them to change the hash to match whatever they want and decrypt your data into it's plaintext equivalent, a smarter idea would be to use a password manager that has been proven to work. However, keep in mind that if someone is able to get into your system, you have much bigger problems then getting your passwords decrypted.