from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import os
import pdf2image 

class Generator:
    def __init__(self, template_filepath, font='OpenSans-SemiBold.ttf', font_size=60, output='certificates'):
        # create output dir
        if not os.path.isdir(output):
            os.makedirs(output)

        # convert pdf template to jpg
        if template_filepath.split('.')[-1] == 'pdf' and not os.path.isfile(template_filepath[:-4] + '.png'):
            img = pdf2image.convert_from_path(template_filepath)[0]

            template_filepath = template_filepath[:-4] + '.png'
            img.save(template_filepath)

        self.font = ImageFont.truetype(font, font_size)
        self.template = template_filepath
        self.output = output


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
