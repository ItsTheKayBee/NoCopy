import hashlib
import PyPDF2
import docx2txt
from PIL import Image
import imagehash
import distance
from mp3hash import mp3hash


def txt_hash():
    file = "myfile.txt"
    BLOCK_SIZE = 65536

    file_hash = hashlib.sha3_256()
    with open(file, 'rb') as f:
        fb = f.read(BLOCK_SIZE)
        while len(fb) > 0:
            file_hash.update(fb.strip())
            fb = f.read(BLOCK_SIZE)

    return file_hash.hexdigest()


def pdf_hash():
    pdfFileObject = open('myfile.pdf', 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObject)
    count = pdfReader.numPages
    fb = ''
    for i in range(count):
        page = pdfReader.getPage(i)
        fb += page.extractText().strip()

    return hashlib.sha3_256(fb.encode('utf-8')).hexdigest()


def word_hash():
    result = docx2txt.process("myfile.docx").strip()
    return hashlib.sha3_256(result.encode('utf-8')).hexdigest()


def image_hash():
    file = imagehash.phash(Image.open("myfile.jpg"))
    return str(file)


def audio_hash():
    file = "myfile.mp3"
    return mp3hash(file, None, hashlib.sha3_256())


def image_dist(a, b):
    return distance.hamming(a, b)

