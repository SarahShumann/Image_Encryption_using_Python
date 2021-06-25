import os
from Encryption import Encryption
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

BASE_URL = "profilee"
END_URL = "Encrypted"
EncrKernel = Encryption("test.jpg")
EncrKernel.set_config(BASE_URL, END_URL, "tiff")
i = 1
for file_name in os.listdir(BASE_URL):
    print (i)
    EncrKernel.generate_encrypted_image(file_name)
    i += 1
