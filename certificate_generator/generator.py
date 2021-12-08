from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import os, io
import pdf2image 
import qrcode_styled

class Generator:
    def __init__(self, template_filepath, 
                name=(435, 72), \
                code=(71, 258, 30), \
                qrcode =(60, 340), \
                font='OpenSans-SemiBold.ttf', \
                output='certificates', \
                use_qrcode=False, qr_logo_path=None):

        self.check_arguments(name, code, qrcode)
        self.initialize_project_tree(output)
        template_filepath = self.convert_template_to_jpg(template_filepath)
       
        # load logo for qrcode decoration
        self.qr_logo = None
        if qr_logo_path:
            self.qr_logo = Image.open(qr_logo_path)

        self.y_name = name[0]
        self.pos_code = tuple(code[:2])
        self.pos_qrcode = tuple(qrcode)
        self.size_name = name[-1]
        self.size_code = code[-1]

        self.font_name = ImageFont.truetype(font, self.size_name)
        self.font_code = ImageFont.truetype(font, self.size_code)
        self.template = template_filepath
        self.output = output
        self.use_qrcode = use_qrcode
        self.qrcode = qrcode_styled.QRCodeStyled() 

    def convert_template_to_jpg(self, template_filepath):
        template_filename, template_format = os.path.splitext(template_filepath)
        png_filepath = template_filename + '.png'
        if template_format == 'pdf':
            self.create_png_template(template_filepath, png_filepath)
        return template_filename + '.png'

    def create_png_template(self, template_filepath, png_filepath):
        # convert pdf template to jpg
        if not os.path.isfile(png_filepath):
            img = pdf2image.convert_from_path(template_filepath)[0]
            img.save(png_filepath)

    def initialize_project_tree(self, output):
        # create output dir
        if not os.path.isdir(output):
            os.makedirs(output)

    def check_arguments(self, name, code, qrcode):
        assert len(name) == 2    # (y, fontsize)
        assert len(code) == 3    # (x, y, fontsize) 
        assert len(qrcode) == 2  # (x, y)

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



