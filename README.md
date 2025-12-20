# Tittle of the project: Secure Messaging System

## Short Description about the project

The Secure Messaging System is a cryptography-based project designed to provide a safe and reliable way to send messages over the internet.  
It demonstrates how modern cryptographic techniques can work together to protect digital communication:  
- **AES** encrypts messages than sent from the sender to receiver, so only the intended receiver can read them.  
- **RSA** encrypts the AES key and ecurely transmits the encryption key to the receiver.  
- **HMAC** checks the message for any changes during sending and ensures that messages have not been tampered with during transmission.  

## Features

- Secure message encryption using AES (CTR mode)
- Secure key exchange using RSA public-key cryptography
- Message integrity verification using HMAC (SHA-256)
- Detection of tampered or modified messages
- Simple two-user chat simulation using files
- Graceful chat termination using an /exit command

## Installation / Setup Instructions

### Requirements

- Python 3.8 or higher
- Operating System: Linux / macOS / Windows  

### Step 1: Clone or Download the Project
```bash
git clone https://github.com/Keo-Sokanya/Secure_Message.git
cd Secure_Message
```  
### Step 2: Install Dependencies 
```bash
pip install pycryptodome
```
## Project Structure

Secure_Message/
├── src/
│   ├── main.py
│   ├── rsa_crypto.py
│   ├── aes_crypto.py
│   ├── messaging.py
│   ├── hmac_utils.py
│   └── utils.py
└── data/
    ├── keys/
    └── messages/


## Usage

- Start the chat (User1)
```bash
    cd src 
    python main.py
```
- Join the chat (User2)
```bash
    cd src
    python main.py
```
- User1 or User2 send message
```
    [User1]: Hello, this is a secure message.
```
- Receive message, if User1 send a message User2 will receive the message, if User2 send a message User1 will receive the message
```
    [Message Received]: Hello, this is a secure message.
```
- Exit Chat
    /exit
- When one user exit, the other user is notified:
    User1 has left the chat.



## Libraries Used
- os: File handling and random number generation
- json: Message storage
- threading: Concurrent message listening
- time: Polling delay
- Crypto.PublicKey.RSA: RSA key generation and encryption
- Crypto.Cipher.AES: AES message encryption
- Crypto.Cipher.PKCS1_OAEP: Secure RSA padding
- hmac: Message authentication
- hashlib: SHA-256 hashing
- base64: Encoding binary data

## Security Notes

- AES keys are split into encryption and HMAC keys
- HMAC ensures messages are not modified in transit
- RSA keys are stored securely in PEM format
- Messages are never stored in plaintext
