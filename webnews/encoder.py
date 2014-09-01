from Crypto.Cipher import AES # encryption library
import base64

BLOCK_SIZE = 32

# the character used for padding--with a block cipher such as AES, the value
# you encrypt must be a multiple of BLOCK_SIZE in length.  This character is
# used to ensure that your value is always a multiple of BLOCK_SIZE
PADDING = '{'

# one-liner to sufficiently pad the text to be encrypted
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

# one-liners to encrypt/encode and decrypt/decode a string
# encrypt with AES, encode with base64
EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)

cipher = AES.new('aaaaaaaaaa123456')
#cipher = AES.new('0000000000000000')



class EncryptClass:


    def EncodeStr(args,Arr):
        try:
            return EncodeAES(cipher, str(Arr))
        except:
            return Arr

    def DecodeStr(args,Arr):
        try:
            return DecodeAES(cipher, str(Arr).replace(" ", "+"))
        except:
            return Arr



def Encode(Arr):
    #x=EncryptClass()
    #return x.EncodeStr(Arr)
    return Arr

def Decode(Arr):
    #x=EncryptClass()
    #return x.DecodeStr(Arr)
    return Arr