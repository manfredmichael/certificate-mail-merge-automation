import certificate_generator 

FONT = 'NotoSans-SemiCondensedSemiBold.ttf'

generator ={
    'COMITTEE':certificate_generator.Generator("templates/CERTIFICATE OF COMITTEE.pdf", font=FONT)
}



def main():
    generator['COMITTEE'].generate('Manfred Michael Pangaribuan', '001')


if __name__ == '__main__':
    main()

