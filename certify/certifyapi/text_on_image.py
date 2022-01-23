from io import BytesIO
import base64
import config
import pyrebase
from PIL import Image
from PIL import ImageDraw, ImageFont
# import requests


font_path = "media/fonts/MonoLisa-Black.ttf"
font = ImageFont.truetype(font_path, 60)

img = Image.open('media/images/certificate.png')

I1 = ImageDraw.Draw(img)
I1.text((610, 740), "Hakuna Matata", font=font, fill=(0, 0, 0))
# img.show()
# img.save('result.png')
print(img)


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
# metadata = '"contentType": "image/jpeg","size":"262144"'
# metadata = {"size":262144}


filepath = "cers/" 


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


img = img.convert('RGB')

buffered = BytesIO()
img.save(buffered, format="PNG")
img_str = base64.b64encode(buffered.getvalue())
img_str = base64.b64decode(img_str)


print(img_str)

storage.child("new.png").put(img_str, metadata)

img_url = storage.child("cers/new.png").get_url(None)

print(img_url)