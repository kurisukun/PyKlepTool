steps_tab1 = [f'ECIES is a hybrid encryption scheme which means it\'s a combination '
            f'of symmetric and asymmetric encryption, mainly used for sending emails. Mathematically, '
            f'the operations are done on elliptic curves.\n'
            f'The cryptosystem combines the two cryptographic mechanisms with the concept of KEM-DEM:\n\n'
            f'KEM stands for Key Encapsulation Mechanism and represents the asymmetric part. The aim is to '
            f'protect the symmetric key used for the communications. Let\'s imagine Alice wants to send a '
            'mail to Bob. In ECIES: \n'

            f'  1. Randomly draw a interger between 0 and the order of the elliptic curve. This number '
            f'is the private key.\n'
            f'  2. Compute the public key by multiplicating the private key with G, the base point of the curve\n'
            f'  3. Draw an other random integer r and perform K = pk · r which is the session key\n'
            f'  4. Then generate C = r · G to obtain the "ciphertext" of the KEM which is used by the other user '
            f'to compute the shared secret\n\n'
            f'DEM stands for Data Encapsulation Mechanism and is mainly the fact of encrypting '
            f'the message to be sent with the session key produced with the KEM.\n\n'

            f'For this demonstration, send two messages as Alice to Bob. Then go to the next tab to see how '
            f'a ASA can be performed. You will see your message with its title in Bob\'s mailbox followed by '
            f'how normally the message is when it\'s still encrypted.\n'
            ]

steps_tab2 = [f'Here the KEM of ECIES has been a bit modifies by it\'s creator in a way it permits him to recover '
            f'the second session key of Alice\'s messages and the next ones. As we can see, the only known parameters '
            f'are the publicly known information as ciphertexts produced by the KEM, the public key of Bob. The '
            f'has nonetheless introduced his own pair of key (ssk, psk) in a way the KEM uses the public key psk '
            f'to perform the encapsuulation.\n\n'
            
            f'We can then find the second message Alice sent to Bob and all the next emails she will send to him until '
            f'he changes his keys. In this case, the attack will need again two exchanges to perform the attack.'
            ]