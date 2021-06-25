from Crypto.Cipher import AES
from Crypto import Random
from pbkdf2 import PBKDF2
from PIL import Image

import os

BLOCK_SIZE = 16
class Encryption:
    def __init__(self, file_name_key):
        self.file_name_key = file_name_key

    def set_config(self,source_directory, encrypt_directory, transformed_file_extension):
        self.sd = source_directory
        self.ed = encrypt_directory
        self.tfe = transformed_file_extension

    def __cryptify_key(self, key):
        print ("Hashing Key...")
        self.salt = Random.new().read(16)
        return PBKDF2(key, self.salt, 10000).read(32)

    def __encrypt(self, plain_text, secret_key):
        print ("Encrypting Plaintext...")
        IV = Random.new().read(BLOCK_SIZE)
        cipher = AES.new(secret_key, AES.MODE_CFB,IV)
        return IV,cipher.encrypt(plain_text)

    def __extract_image_data(self, image):
        print ("Getting Data From Image...")
        image_data = list(image.getdata())
        return ''.join([chr(pixel) for pixel_set in image_data for pixel in pixel_set])

    def __read_image_data(self,file_name):
        image = Image.open(file_name, "r")
        return (image.mode, image.size, self.__extract_image_data(image))

    def __get_key_from_image(self, file_name):
        print ("Getting Key From Image...")
        return self.__cryptify_key(self.__extract_image_data(Image.open(file_name, "r")))

    def generate_encrypted_image(self, file_name_source):
        image_mode, image_size, image_data = self.__read_image_data(self.sd+"/"+file_name_source)
        counter, enc_data = self.__encrypt(image_data, self.__get_key_from_image(self.file_name_key))
        print ("Saving Encrypted Image...")
        enc_image = Image.frombytes(image_mode, image_size, enc_data)
        file_name1 = ",".join([str(ord(i)) for i in counter]) + "-" + \
            ",".join([str(ord(j)) for j in self.salt])
        path = os.path.join(self.ed, file_name1+"."+self.tfe)
        enc_image.save(path)
        print ("Image Saved...")