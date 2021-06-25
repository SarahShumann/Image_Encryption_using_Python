from Crypto.Cipher import AES
from pbkdf2 import PBKDF2
from PIL import Image
class Decryption: 
    def __init__(self, file_name_key):
        self.file_name_key = file_name_key

    def set_config(self,source_directory, decrypt_directory, transformed_file_extension):
        self.sd = source_directory
        self.ed = decrypt_directory
        self.tfe = transformed_file_extension

    def __cryptify_key(self, key):
        print ("Hashing Key...")
        return PBKDF2(key, self.salt,10000).read(32)

    def __decrypt(self, encrypted_message, secret_key, IV):
        print ("Decrypting Image...")
        aes = AES.new(secret_key, AES.MODE_CFB, IV)
        decrypted_message = aes.decrypt(IV+encrypted_message)
        return decrypted_message

    def __extract_image_data(self, image):
        print ("Getting Data From Image...")
        image_data = list(image.getdata())
        return ''.join([chr(pixel) for pixel_set in image_data for pixel in pixel_set])

    def __read_image_data(self, file_name):
        print ("Extracting Ciphertext From Image...")
        image = Image.open(file_name, "r")
        return (image.mode, image.size, self.__extract_image_data(image))

    def __get_key_from_image(self, file_name):
        print ("Getting Key From Image...")
        return self.__cryptify_key(self.__extract_image_data(Image.open(file_name, "r")))

    def generate_decrypted_image(self, file_name_source, file_name_dec):
        sep = "-"
        image_mode, image_size, image_data = self.__read_image_data(self.sd +"/" +file_name_source)
        counter = ''.join([chr(int(i)) for i in file_name_source[:-5].split(sep)[0].split(",")])
        self.salt = ''.join([chr(int(i)) for i in file_name_source[:-5].split(sep)[1].split(",")])
        dec_data = self.__decrypt(image_data, self.__get_key_from_image(self.file_name_key), counter)
        print ("Saving Decrypted Image...")
        dec_image = Image.frombytes(image_mode, image_size, dec_data)
        dec_image.save(self.ed+"/"+file_name_dec+"."+self.tfe)
        print ("Image Saved...")