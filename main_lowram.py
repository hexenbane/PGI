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

if file_path == '':
    print(" ----> Cancelar Proceso")
    exit()


# print("tkinter OK")
i = i + 1
time.sleep(0.5)
update_progress("tkinter OK", i / 8.0)

# Una vez teniendo el archivo se extrae su ruta, folder y tipo de archivo
ruta = os.path.splitext(file_path)[0]
filetype = os.path.splitext(file_path)[1]
folder = os.path.dirname(file_path)

# Con la libreria de PyPDF se cuentan las hojas contenidas en el PDF
pdf = PyPDF2.PdfFileReader(open(file_path, "rb"), strict=False)
pags = pdf.getNumPages()

i = i + 1
time.sleep(0.5)
update_progress("Path OK", i / 8.0)

# Se arma el comando completo para GhostScript y convertir cada hoja del pdf en un Bitmap
# Esto es para mantener las imagenes lo mejor posible y eliminar capas transparentes
# en esta parte se puede seleccionar la resolucion, parece que 150 a 300 es lo mas ideal

# GSPath = "C:/Program Files/gs/gs9.19/bin/gswin64.exe"
GSPath = "C:/Users/[____]/Portable Software/Ghostscript/bin/gswin32c"


GSDevice = "-sDEVICE=bmpgray"
GSDevice_pdf = "-sDEVICE=pdfwrite"
GSOption1 = "-dNOPAUSE"
GSOption2 = "-dBATCH"
GSRes = "-r300"
GSOption3 = "-o"
GSQuite= "-q"
GSPdf = file_path
GSOutput = "-sOutputFile=" + ruta + GSRes + ".pdf"

#IMPath = "C:/Program Files/ImageMagick-7.0.5-Q16/convert.exe"

IMPath = "C:/Users/[___]/Portable Software/ImageMagick/convert.exe"

IMOption1_a = "-threshold"
IMOption1_b = "75%"
IMOption2_a = "-compress"
IMOption2_b = "group4"


NewPDFs_list=[]

for pag in range(1, pags + 1, 1):
	GSBatchBitmap = str(pag) + ".bmp"
	GSRuta = folder + "/" + GSBatchBitmap
	GSPageStart = "-dFirstPage=" + str(pag)
	GSPageLast = "-dLastPage=" + str(pag)
	argsa = [GSPath, GSDevice, GSOption1, GSOption2, GSRes, GSOption3, GSRuta, GSQuite, GSPageStart, GSPageLast, GSPdf]
	
	subprocess.call(argsa)
	
	BitmapNames = folder + "/" + str(pag) + ".bmp"

	
	IMFullCommand = [IMPath]
	
	IMFullCommand.append(BitmapNames)
	IMFullCommand.append(IMOption1_a)
	IMFullCommand.append(IMOption1_b)
	IMFullCommand.append(IMOption2_a)
	IMFullCommand.append(IMOption2_b)
	
	NewPDFPath = ruta + "_" + str(pag) + "_" + GSRes + filetype
	NewPDFs_list.append(NewPDFPath)
	
	IMFullCommand.append(NewPDFPath)
	
	subprocess.call(IMFullCommand)
	
	os.remove(BitmapNames)

argsb = [GSPath, GSDevice_pdf, GSOption1, GSOption2, GSQuite, GSOutput]
argsb.extend(NewPDFs_list)

subprocess.call(argsb)

for x in NewPDFs_list:
	os.remove(x)
 
i = i + 1
time.sleep(0.5)
update_progress("Count Pages OK", i / 8.0)

# Sabiendo el numero de hojas entonces genero la lista de nombres para integrarlo en un comando

# Agrego las opciones finales despues de los nombres de los archivos



# Mando el commando para que se ejecute en ImageMagick


# print("ImageMagick OK")
i = i + 1
time.sleep(0.5)
update_progress("ImageMagick OK", i / 8.0)

# Con esta ultima parte se borran los bitmaps generados temporalmente



# print("Clean OK")
i = i + .90
time.sleep(0.5)
update_progress("Clean OK", i / 8.0)

# print("Completo")
update_progress("Compression Complete", 8.0 / 8.0)
