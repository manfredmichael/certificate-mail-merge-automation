from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import os, io
import pdf2image 
import qrcode_styled

class Generator:
    def __init__(self, template_filepath, font='OpenSans-SemiBold.ttf', name_size=72, code_size=30, output='certificates'):
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
        self.qrcode = qrcode_styled.QRCodeStyled() 

    def generate(self, name, code, qr_logo=None):
        name = name.upper()

        certificate = Image.open(self.template)
        W, H = certificate.size

        # draw qrcode
        qr = self.get_qrcode(code, qr_logo)
        w, h = qr.size
        certificate.paste(qr, (60, 340))

        # write certificate code
        draw = ImageDraw.Draw(certificate)
        draw.rounded_rectangle((50, 250, 343, 310), 
                fill="#65b5f5",
                width=3, radius=20)
        draw.text(xy=(73, 258), 
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
        return filepath 

    def get_qrcode(self, code, qr_logo):
        url = 'https://dscug.club/certificate/{}'.format(code)
        if qr_logo:
            logo = Image.open(qr_logo)
            im_bytes = self.qrcode.get(url, logo)
        else:
            im_bytes = self.qrcode.get(url, )
        return Image.open(im_bytes).resize((210, 210))



