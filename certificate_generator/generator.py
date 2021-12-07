from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import os, io
import pdf2image 
import qrcode_styled

class Generator:
    def __init__(self, template_filepath, name=(435, 72), code=(73, 258, 30) , qrcode =(60, 30), font='OpenSans-SemiBold.ttf', name_size=72, code_size=30, output_folder='certificates', use_qrcode=False, qr_logo_path=None):
        assert len(name) == 2    # (y, fontsize)
        assert len(code) == 3    # (x, y, fontsize) 
        assert len(qrcode) == 2  # (x, y)

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
       
        # load logo for qrcode decoration
        self.qr_logo = None
        if qr_logo_path:
            self.qr_logo = Image.open(qr_logo_path)

        self.y_name = tuple(name[0])
        self.pos_code = tuple(code[:2])
        self.pos_qrcode = tuple(qrcode)
        self.size_name = tuple(name[-1])
        self.size_code = tuple(code[-1])

        self.font_name = ImageFont.truetype(font, name_size)
        self.font_code = ImageFont.truetype(font, code_size)
        self.template = template_filepath
        self.output = output
        self.use_qrcode = use_qrcode
        self.qrcode = qrcode_styled.QRCodeStyled() 
        

    def generate(self, name, code):
        name = name.upper()

        certificate = Image.open(self.template)
        W, H = certificate.size

        # draw qrcode
        if self.use_qrcode:
            qr = self.get_qrcode(code)
            w, h = qr.size
            certificate.paste(qr, self.pos_qrcode)

        # write certificate code
        draw = ImageDraw.Draw(certificate)
        draw.text(xy=self.pos_code, 
                  text=code,
                  fill='white',
                  font=self.font_code)

        # write name 
        w, h = self.font_name.getsize(name)
        draw.text(xy=((W-w)//2, self.y_name), 
                  text=name,
                  fill='black',
                  font=self.font_name)

        # save as pdf
        filename = name + '.pdf'
        filepath = os.path.join(self.output, filename)
        certificate.save(filepath) 
        return filepath 

    def get_qrcode(self, code):
        url = 'https://dscug.club/certificate/{}'.format(code)
        if self.qr_logo:
            im_bytes = self.qrcode.get(url, self.qr_logo)
        else:
            im_bytes = self.qrcode.get(url, )
        return Image.open(im_bytes).resize((210, 210))



