from io import BytesIO
import base64
from re import template
from turtle import position
from . import config
# import config

import pyrebase
from PIL import Image
from PIL import ImageDraw, ImageFont

import qrcode
# import requests
from datetime import date
today = date.today()





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


def generate_certificate(uid_number,name,storage_path,content_to_write,acheived_position,template_number):

    monolisa_font_path = "media/fonts/MonoLisa-Black.ttf"
    arial_font_path = "media/fonts/arial.ttf"
    namefont = ImageFont.truetype(monolisa_font_path, 60)
    detailsfont = ImageFont.truetype(arial_font_path, 30)

    d4 = today.strftime("%b-%d-%Y")





    if(template_number=="1"):
        
        img = Image.open('media/images/certificate1.png')


        I1 = ImageDraw.Draw(img)
        I1.text((610, 740), name, font=namefont, fill=(0, 0, 0))
        I1.text((500, 840), content_to_write, font=detailsfont, fill=(0, 0, 0))
        # print("d4 =", d4)
        I1.text((440, 1130), d4, font=detailsfont, fill=(0, 0, 0))


        print('came')
        if(acheived_position!=None):
            new_c = "Standing at position '" + acheived_position + "'"
            print('--------------------')
            print(new_c)
            print('--------------------')

            I1.text((865, 900), new_c, font=detailsfont, fill=(0, 0, 0))
        print('passed by')


        qr = qrcode.QRCode(box_size=6)
        verification_link = "http://127.0.0.1:8000/verifycertificate?uid_number=" + uid_number
        qr.add_data(verification_link)

        qr.make()
        img_qr = qr.make_image(fill_color="#000000", back_color="#F8F7F2")

        print(img_qr.size)
        pos = (img.size[0] - 1120, img.size[1] - 390)
        img.paste(img_qr, pos)

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

        return img_url, d4

        # img.show()
    
    if(template_number=="2"):
    
        img = Image.open('media/images/certificate2.png')


        I1 = ImageDraw.Draw(img)
        I1.text((610, 740), name, font=namefont, fill=(0, 0, 0))
        I1.text((500, 840), content_to_write, font=detailsfont, fill=(0, 0, 0))
        I1.text((360, 1120), d4, font=detailsfont, fill=(0, 0, 0))

        print('came')
        if(acheived_position!=None):
            new_c = "Standing at position '" + acheived_position + "'"
            print('--------------------')
            print(new_c)
            print('--------------------')

            I1.text((865, 900), new_c, font=detailsfont, fill=(0, 0, 0))
        print('passed by')


        qr = qrcode.QRCode(box_size=6)
        verification_link = "http://127.0.0.1:8000/verifycertificate?uid_number=" + uid_number
        qr.add_data(verification_link)

        qr.make()
        img_qr = qr.make_image(fill_color="#000000", back_color="#F8F7F2")

        print(img_qr.size)
        pos = (img.size[0] - 1120, img.size[1] - 390)
        img.paste(img_qr, pos)

        # img.show()
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

        return img_url, d4



    # img = img.convert('RGB')

    # buffered = BytesIO()
    # img.save(buffered, format="PNG")
    # img_str = base64.b64encode(buffered.getvalue())
    # img_str = base64.b64decode(img_str)

    # filename = str(uid_number)+".png"

    # new_file_path = storage_path+filename
    # print(new_file_path)

    # storage.child(new_file_path).put(img_str, metadata)
    # img_url = storage.child(new_file_path).get_url(None)

    # return img_url, d4


# generate_certificate("d19929ccd19c43b9c0a9","Harshith Sai Tunuguntla","off/","For winning in Line Follower Competetion conducted by Robotics Club","1","2")