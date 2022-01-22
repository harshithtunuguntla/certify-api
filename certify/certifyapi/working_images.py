from io import BytesIO
import base64
from . import config
import pyrebase
from PIL import Image
from PIL import ImageDraw, ImageFont
# import requests






# img.show()
# img.save('result.png')
# print(img)


firebaseConfig = {
    "apiKey": config.apiKey,
    "authDomain": config.authDomain,
    "projectId": config.projectId,
    "databaseURL": config.databaseURL,
    "storageBucket": config.storageBucket,
    "messagingSenderId": config.messagingSenderId,
    "appId": config.appId,
    "measurementId": config.measurementId,
    "serviceAccount": config.serviceAccount
}


firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()

metadata = '"contentType": "image/jpeg" "size":"262144"'
filepath = "official_certificates/"

# metadata = '"contentType": "image/jpeg","size":"262144"'
# metadata = {"size":262144}
# storage.child(filepath).put("media/images/certificate.png",metadata)

# bucket = "imageupload-19537"

# blob = bucket.blob(filepath, chunk_size=262144) # 256KB
# blob.upload_from_file(img)

# img_url = storage.child(filepath).get_url(None)

# print(img_url)

# --------------------------------

# import io
# rgb_im = img.convert('RGB')
# buffer = io.BytesIO()
# rgb_im.save(buffer, format='JPEG', quality=75)

# # You probably want
# desiredObject = buffer.getbuffer()

# print(desiredObject)
# filepath = "cer/" + "certf"
# storage.child(filepath).put(rgb_im)

# ---------------------------------

# from google.cloud import storage

# client = storage.Client()
# bucket = client.get_bucket('imageupload-19537')
# blob = bucket.blob('certificate.png')

# blob.upload_from_file(img)
# # or... (no need to use pillow if you're not transforming)
# blob.upload_from_filename(filename=img)

# -------------------------


def generate_certificate(uid_number,name,storage_path,content_to_write,acheived_position):

    font_path = "media/fonts/MonoLisa-Black.ttf"
    font = ImageFont.truetype(font_path, 60)


    img = Image.open('media/images/certificate.png')
    I1 = ImageDraw.Draw(img)
    I1.text((610, 740), name, font=font, fill=(0, 0, 0))


    




    img = img.convert('RGB')

    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())
    img_str = base64.b64decode(img_str)

    filename = str(uid_number)+".png"

    new_file_path = storage_path+filename
    print(new_file_path)

    storage.child(new_file_path).put(img_str, metadata)
    img_url = storage.child(new_file_path).get_url(None)

    return img_url


generate_certificate("d19929ccd19c43b9c0a9","Harshith Sai Tunuguntla","off/","For Being Volunter","1")