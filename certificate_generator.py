from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import os


class CertificateGenerator:
    def __init__(self, template_filepath, font_style='arial.ttf', font_size=60, output='certificates'):
        self.font = ImageFont.truetype(font_style, font_size)
        self.template = template_filepath
        self.output = output

        if not os.path.isdir(output):
            os.makedirs(output)

    def generate(self, name, certificate_code):
        certificate = Image.open(self.template)
        draw = ImageDraw.Draw(certificate)
        draw.text(xy=(725,760), 
                  text='{}'.format(name),
                  fill=(0,0,0),
                  font=self.font)

        filename = name + '.pdf'
        filepath = os.path.join(self.output, filename)
        certificate.save(filepath) 
