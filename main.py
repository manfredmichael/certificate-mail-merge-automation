import certificate_generator 

FONT = 'NotoSans-SemiCondensedSemiBold.ttf'

generator ={
    'COMITTEE':certificate_generator.Generator("templates/CERTIFICATE OF COMITTEE.pdf", font=FONT),
    'PARTICIPANT':certificate_generator.Generator("templates/CERTIFICATE OF PARTICIPANT.pdf", font=FONT),
    'SPEAKER':certificate_generator.Generator("templates/CERTIFICATE OF SPEAKER.pdf", font=FONT)
}



def main():
    generator['SPEAKER'].generate('abadi suryo', '001')


if __name__ == '__main__':
    main()

