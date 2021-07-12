step1 = f'A SETUP attack permits to leak encrypted data out of a cryptogryphic device. With this example, we assume ' \
        f'that the attacker has compromised the device to contain his/her public key.\n' \
        f'However, all the parameters of the attacker are generated as if it was a normal RSA key generation.\n'

step2 = f'The prime q is generated randomly. Then p is selected so that it will permit the user\'s public e to be ' \
        f'prime with phi, this way the device will compute d by using the inverse of e (mod ϕ)\n' \
        f'WARNING: it may take time for large key size!\n'

step3 = f'RSA is not used for encryption of data because of its slowness. Instead, we use symmetric cryptographic ' \
        f'that for this purpose. But to secure the transmission of the symmetric key, we encrypt it with RSA\n' \
        f'Generate a symmetric key to encrypt it then!\n'

step4 = f'To a normal observer, this output seem encrypted and the keys seem absolutely random. The attacker, however' \
        f', knows that the private key is hidden inside of the user\'s public key.'