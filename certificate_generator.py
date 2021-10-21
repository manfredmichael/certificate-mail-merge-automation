from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import os
import pdf2image 
import qrcode

class Generator:
    def __init__(self, template_filepath, font='OpenSans-SemiBold.ttf', name_size=72, code_size=32, output='certificates'):
        # create output dir
        if not os.path.isdir(output):
            os.makedirs(output)

        # convert pdf template to jpg
        if template_filepath.split('.')[-1] == 'pdf':
            png_filepath = template_filepath[:-4] + '.png'
            if not os.path.isfile(png_filepath):
                img = pdf2image.convert_from_path(template_filepath)[0]
                img.save(png_filepath)
            template_filepath = png_filepath

        self.font_name = ImageFont.truetype(font, name_size)
        self.font_code = ImageFont.truetype(font, code_size)
        self.template = template_filepath
        self.output = output


    def generate(self, name, code):
        name = name.upper()

        certificate = Image.open(self.template)
        W, H = certificate.size

        # draw qrcode
        qr = self.get_qrcode(code)
        w, h = qr.size
        certificate.paste(qr, (40, 330))

        # write certificate code
        draw = ImageDraw.Draw(certificate)
        draw.rounded_rectangle((50, 250, 330, 310), 
                fill="#65b5f5",
                width=3, radius=20)
        draw.text(xy=(85, 256), 
                  text=code,
                  fill='white',
                  font=self.font_code)

        # write name 
        w, h = self.font_name.getsize(name)
        draw.text(xy=((W-w)//2, 435), 
                  text=name,
                  fill='black',
                  font=self.font_name)

        # save as pdf
        filename = name + '.pdf'
        filepath = os.path.join(self.output, filename)
        certificate.save(filepath) 

    def get_qrcode(self, code):
        url = 'https://dscug.club/certificate/{}'.format(code)
        qr = qrcode.QRCode(
            version=1,
            box_size=5,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        return qr.make_image()



