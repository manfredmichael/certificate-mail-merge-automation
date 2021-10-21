from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import os
import pdf2image 

class Generator:
    def __init__(self, template_filepath, font='OpenSans-SemiBold.ttf', font_size=72, output='certificates'):
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

        self.font = ImageFont.truetype(font, font_size)
        self.template = template_filepath
        self.output = output


    def generate(self, name, certificate_code):
        name = name.upper()

        certificate = Image.open(self.template)
        draw = ImageDraw.Draw(certificate)

        # write name 
        W, H = certificate.size
        w, h = self.font.getsize(name)
        draw.text(xy=((W-w)/2, 435), 
                  text=name,
                  fill='black',
                  font=self.font)

        # save as pdf
        filename = name + '.pdf'
        filepath = os.path.join(self.output, filename)
        certificate.save(filepath) 

