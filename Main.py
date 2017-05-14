import os.path
import sys
import time
import PyPDF2
import tkinter
from tkinter import filedialog
import subprocess


# Defines un Progress Bar
def update_progress(job_title, progress):
    length = 20  # modify this to change the length
    block = int(round(length * progress))
    msg = "\r{0}: [{1}] {2}%".format(job_title, "#" * block + "-" * (length - block), round(progress * 100, 2))
    if progress >= 1:
        msg += " DONE\r\n"
    sys.stdout.write(msg)
    sys.stdout.flush()

# Con este bloque se actualiza el Progress Bar
i = 1
time.sleep(0.1)
update_progress("Start Compression", i / 8.0)

# Llamar a tkinter para poder seleccionar el PDF a Comprimir
root = tkinter.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()

# print("tkinter OK")
i = i + 1
time.sleep(0.5)
update_progress("tkinter OK", i / 8.0)

# Una vez teniendo el archivo se extrae su ruta, folder y tipo de archivo
ruta = os.path.splitext(file_path)[0]
filetype = os.path.splitext(file_path)[1]
folder = os.path.dirname(file_path)

i = i + 1
time.sleep(0.5)
update_progress("Path OK", i / 8.0)

# Se arma el comando completo para GhostScript y convertir cada hoja del pdf en un Bitmap
# Esto es para mantener las imagenes lo mejor posible y eliminar capas transparentes
# en esta parte se puede seleccionar la resolucion, parece que 150 a 300 es lo mas ideal

# GSPath = "C:/Program Files/gs/gs9.19/bin/gswin64.exe"
GSPath = "C:/Program Files/gs/gs9.21/bin/gswin64.exe"
GSBatchBitmap = "%d.bmp"
GSDevice = "-sDEVICE=bmpgray"
GSOption1 = "-dNOPAUSE"
GSOption2 = "-dBATCH"
GSRes = "-r300"
GSOption3 = "-o"
GSRuta = folder + "/" + GSBatchBitmap
GSPdf = file_path

argsa = [GSPath, GSDevice, GSOption1, GSOption2, GSRes, GSOption3, GSRuta, GSPdf]
subprocess.call(argsa)

# print("Ghostscript OK")
i = i + 1
time.sleep(0.5)
update_progress("Ghostscript OK", i / 8.0)

# Se arma el comando en ImageMagick, siendo un TIFF G4, se tiene que hacer un pdf directo
# Pero en PDF muy largos usa mucha memoria, puede que lo ideal sea despues ir imagen por imagen y comprimir
# Para despues integrar en un solo PDF

IMPath = "C:/Program Files/ImageMagick-7.0.5-Q16/convert.exe"

IMOption1_a = "-threshold"
IMOption1_b = "50%"
IMOption2_a = "-compress"
IMOption2_b = "group4"
NewPDFPath = ruta + GSRes + filetype
IMFullCommand = [IMPath]

i = i + 1
time.sleep(0.5)
update_progress("Variable ImageMagick OK", i / 8.0)

# Aqui doy de alta dos variables que guardaran los nombres de los bitmaps y sus rutas

BitmapNames = ""
BitmapNames_list = []

# Con la libreria de PyPDF se cuentan las hojas contenidas en el PDF
pdf = PyPDF2.PdfFileReader(open(file_path, "rb"))
pags = pdf.getNumPages()
# pags = 88

# print("PyPDF OK")
i = i + 1
time.sleep(0.5)
update_progress("Count Pages OK", i / 8.0)

# Sabiendo el numero de hojas entonces genero la lista de nombres para integrarlo en un comando

for j in range(1, pags + 1, 1):
    BitmapNames = folder + "/" + str(j) + ".bmp"
    IMFullCommand.append(BitmapNames)
    BitmapNames_list.append(BitmapNames)

# Agrego las opciones finales despues de los nombres de los archivos

IMFullCommand.append(IMOption1_a)
IMFullCommand.append(IMOption1_b)
IMFullCommand.append(IMOption2_a)
IMFullCommand.append(IMOption2_b)
IMFullCommand.append(NewPDFPath)

# Mando el commando para que se ejecute en ImageMagick
subprocess.call(IMFullCommand)

# print("ImageMagick OK")
i = i + 1
time.sleep(0.5)
update_progress("ImageMagick OK", i / 8.0)

# Con esta ultima parte se borran los bitmaps generados temporalmente

for bitmaps in BitmapNames_list:
    os.remove(bitmaps)

# print("Clean OK")
i = i + .90
time.sleep(0.5)
update_progress("Clean OK", i / 8.0)

# print("Completo")
update_progress("Compression Complete", 8.0 / 8.0)
