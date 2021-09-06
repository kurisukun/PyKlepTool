steps_tab1 = [f'RSA is an public-key cryptosystem widely used to secure data transmission. This means if two people, ' 
            f'let\'s say Alice and Bob, want to communicate securely, they will have to generate a pair of key:'
            f'\n- The public key E known by everyone. This one is used by the receiver to encrypt the message he wants to send'
            f'\n- The private key D kept secret. This one is used to decrypt the messages received and encryted '
            f'with the corresponding public key E \n\n'
            
            f'The public and private key generation works normally this way:\n'
            f'  1. Draw 2 prime numbers P and Q randomly\n'
            f'  2. Compute N = P · Q. This is called the modulus and it is used to operate the encryption computations using modular arithmetic\n'
            f'  3. Compute φ(N) = (P -1) · (Q - 1)\n'
            f'  4. Choose the public key E to be equal to 65537. It may happen we draw it randomly but this is not the usual method used\n'
            f'  5. Calculate D as the inverse of e modulo φ(N)\n\n'
            f'The security of RSA is based on the fact that it is difficult to decompose the number n into the two prime '
            f'numbers P and Q that were randomly drawn to compute φ(N). Indeed, if it were possible to find P and Q, '
            f'everyone could take the public key E and compute in turn D and thus decrypt the messages normally '
            f'intended for us.\n\n'
            f'Now enter a message to be encrypted using the public key E.\n'
            ,
            f'The text is encrypted. When done correctly, the text can\'t be retrived by any person which does not know '
            f'the private key D. Click on the next button to decrypt the ciphertext and get your original message.\n'
            ,
            f'As you see, you get the same text you wrote. Now click on the next button to see how a SETUP attack can '
            f'destroy the security of RSA.\n'
            ]


steps_tab2 = [f'A SETUP attack permits to leak encrypted data out of a cryptogryphic device. With this example, we assume '
         f'that the attacker has compromised the device to contain his/her public key.\n'
         f'However, all the parameters of the attacker are generated as if it was a normal RSA key generation.\n'
        ,
         f'The prime q is generated randomly. Then p is selected so that it will permit the user\'s public e to be '
         f'prime with phi, this way the device will compute d by using the inverse of e (mod ϕ)\n'
         f'WARNING: it may take time for large key size!\n'
        ,
         f'RSA is not used for encryption of data because of its slowness. Instead, we use symmetric cryptographic '
         f'that for this purpose. But to secure the transmission of the symmetric key, we encrypt it with RSA\n'
         f'Generate a symmetric key to encrypt it then!\n'
        ,
         f'To a normal observer, this output seem encrypted and the keys seem absolutely random. The attacker, however'
         f', knows that the private key is hidden inside of the user\'s public key.\n'
        ,
         f'The attacker computes p by using the user\'s public key and his/her own private key D. Since the attacker '
         f'is the only one who knows the private key D and the key was generated using a normal RSA, then he is the '
         f'only one who can obtain the user\'s private key,\n'
         f'Finally, as we can see, the attacker was able to find the user\'s symmetric key, giving him the possibility '
         f'to decrypt all the encrypted communications that will be made.\n']
