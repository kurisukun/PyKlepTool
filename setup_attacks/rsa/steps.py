steps = [f'A SETUP attack permits to leak encrypted data out of a cryptogryphic device. With this example, we assume '
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
