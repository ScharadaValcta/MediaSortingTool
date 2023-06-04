#!/bin/env python

#für die liste
import glob

#für die liste und file date und verschieben,kopieren
import os

#für metadaten von bildern
from PIL import Image
from PIL.ExifTags import TAGS

#für metadaten von videos mp4
#from moviepy.editor import VideoFileClip
from mutagen.mp4 import MP4

#für metadaten von mov videos
import ffmpeg

#für metadaten von pdf
import PyPDF2

#für file date
from datetime import datetime

#from moviepy.video.io.ffmpeg_tools import ffmpeg_parse_infos

#fürs verschieben,kopieren
import shutil

def get_image_metadata(image_path):
    image = Image.open(image_path)
    #exif_data = image._getexif()
    exif_data = image.getexif()
    
    metadata = {}
    if exif_data is not None:
        for tag_id, value in exif_data.items():
            tag_name = TAGS.get(tag_id, tag_id)
            metadata[tag_name] = value
    return metadata

def get_video_metadata(video_path):
    video = MP4(video_path)
    metadata = {
        'Erstellungsdatum': video.get('creation_time'),
        'Aufnahmedatum': video.get('creation_time'),
        'Bearbeitungsdatum': video.get('moov/udta/meta/ilst/modification_time')
    }
    return metadata

def get_mov_metadata(video_path):
    metadata = ffmpeg.probe(video_path)
    format_tags = metadata['format']['tags']
    metadata = {
        'Erstellungsdatum': format_tags.get('creation_time'),
        'Aufnahmedatum': format_tags.get('creation_time'),
        'Bearbeitungsdatum': format_tags.get('modification_time'),
        'Zugriffsdatum':format_tags.get('access_time')
    }
    return metadata

def get_pdf_metadata(pdf_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        info = pdf_reader.getDocumentInfo()
        metadata = {
            "Änderungsdatum": info.modified,
            "Erstellungsdatum": info.created,
            "Aufnahmedatum":  info.metadata.get('/CreationDate')
        }
    return metadata

def get_file_date(file_path):
    # Änderungsdatum der Datei
    timestamp_aenderung = os.path.getmtime(file_path)
    aenderungsdatum = datetime.fromtimestamp(timestamp_aenderung)
    # Erstellungsdatum der Datei
    timestamp_erstellung = os.path.getctime(file_path)
    erstellungsdatum = datetime.fromtimestamp(timestamp_erstellung)
    # Zugriffsdatum der Datei
    timestamp_zugriff = os.path.getatime(file_path)
    zugriffsdatum = datetime.fromtimestamp(timestamp_zugriff)
    date = {
        'Änderungsdatum': aenderungsdatum,
        'Erstellungsdatum':erstellungsdatum,
        'Zugriffsdatum':zugriffsdatum
    }
    return date

def checkvaliddate(jahr,monat):
    years = ["2010","2011","2012","2013","2014","2015","2016","2017","2018","2019","2020","2021","2022","2023"]
    month = ["01","02","03","04","05","06","07","08","09","10","11","12"]
    return jahr in years and monat in month

def convertfrommonthtonumber(kurzel):
    month = ["01","02","03","04","05","06","07","08","09","10","11","12"]
    months = {
        "Jan": "01",
        "Feb": "02",
        "Mar": "03",
        "Apr": "04",
        "May": "05",
        "Jun": "06",
        "Jul": "07",
        "Aug": "08",
        "Sep": "09",
        "Oct": "10",
        "Nov": "11",
        "Dec": "12"
    }
    if months[kurzel] in month:
        return months[kurzel]
    else:
        return ""

def get_date_out_of_mail(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("Date"):
                dateline = line 
                break
        part = dateline.split(" ")
        month = convertfrommonthtonumber(part[3])
        year = part[4]
        if checkvaliddate(year,month):
            return year + month
        else:
            return ""

def get_newpath_from_metadata(file_path):
    if file_path.endswith(".jpg") or file_path.endswith(".JPG") or file_path.endswith(".jpeg") or file_path.endswith(".JPEG") or file_path.endswith(".png") or file_path.endswith(".PNG"):
        datum = ""
        metadata = get_image_metadata(file_path)
        if metadata.get('DateTime') != None:
            datum = metadata.get('DateTime')
        elif metadata.get('DateTimeOriginal') != None:
            datum = metadata.get('DateTimeOriginal')
        elif metadata.get('DateTimeDigitized') != None:
            datum = metadata.get('DateTimeDigitized')
        elif metadata.get('DateTimeModified') != None:
            datum = metadata.get('DateTimeModified')
        if datum != "" and checkvaliddate(datum[0:4],datum[5:7]):
            newpath = "/" + datum[0:4] + "/" + datum[5:7] + "/"
            return newpath
        else:
            return ""
    elif file_path.endswith(".mp4") or file_path.endswith(".MP4"):
        #Hier funktioniert etwas nicht oder alle dateien die ich habe haben einfach keine metadaten
        metadata = get_video_metadata(file_path)
        if metadata["Erstellungsdatum"] != None or metadata["Aufnahmedatum"] != None or metadata["Bearbeitungsdatum"] != None:
            print("Erstellungsdatum", metadata["Erstellungsdatum"])
            print("Aufnahmedatum", metadata["Aufnahmedatum"])
            print("Bearbeitungsdatum", metadata["Bearbeitungsdatum"])
        return ""
    elif file_path.endswith(".pdf") or file_path.endswith(".PDF"):
        metadata = get_pdf_metadata(file_path)
        print("Änderungsdatum", metadata["Änderungsdatum"])
        print("Erstellungsdatum", metadata["Erstellungsdatum"])
        print("Aufnahmedatum", metadata["Aufnahmedatum"])
        return ""
    elif file_path.endswith(".MOV") or file_path.endswith(".mov"):
        metadata = get_mov_metadata(file_path)
        datum = ""
        if metadata["Erstellungsdatum"] != None:
            datum = metadata["Erstellungsdatum"]
        elif metadata["Aufnahmedatum"] != None:
            datum = metadata["Aufnahmedatum"]
        elif metadata["Bearbeitungsdatum"] != None:
            datum = metadata["Bearbeitungsdatum"]
        elif metadata["Zugriffsdatum"] != None:
            datum = metadata["Zugriffsdatum"]
        if datum != "" and checkvaliddate(datum[0:4],datum[5:7]):
            newpath = "/" + datum[0:4] + "/" + datum[5:7] + "/"
            return newpath
        else:
            print("Erstellungsdatum", metadata["Erstellungsdatum"])
            print("Aufnahmedatum", metadata["Aufnahmedatum"])
            print("Bearbeitungsdatum", metadata["Bearbeitungsdatum"])
            print("Zugriffsdatum", metadata["Zugriffsdatum"])
            return ""
    else:
        return ""

def createfolder(destination_path):
    if not os.path.exists(destination_path):
        # Erstelle den Ordner und alle übergeordneten Ordner
        os.makedirs(destination_path)
        print("Neuer Ordner wurde erstellt:", destination_path)
    else:
        print("Der Ordner existiert bereits:", destination_path)

def fileinteraction(source_path,destination_path,filename,interaction):
    #source_path  -> "Handy/S5Mini/phone/Pictures/Freunde/20150503_135229.jpg"
    #destination_path -> "2015/05/Handy - S5Mini - Freunde/20150503_135229.jpg"
    #filename -> "20150503_135229.jpg"
    destination_path_to_file = destination_path + "/" + filename
    #destination_path_to_file -> "2015/05/Handy - S5Mini - Freunde/20150503_135229.jpg"
    if os.path.exists(destination_path_to_file):
        print("Die Datei existiert bereits im Zielordner.")
        print("Versuche destination_path zu nummerieren.")
        alternatedestination_path = alternatedestinationpath(destination_path)
        createfolder(alternatedestination_path)
        fileinteraction(source_path,alternatedestination_path,filename,interaction)
    else:
        if interaction == "copy":
            shutil.copy(source_path, destination_path_to_file)
            print("Die Datei wurde erfolgreich kopiert.")
        elif interaction == "verschieben":
            shutil.move(source_path, destination_path_to_file)
            print("Die Datei wurde erfolgreich verschoben.")

def alternatedestinationpath(destination_path):
    #kann zu problemen führen da ich nicht abdecke das es mehr als nur ein klammerauf geben kann und mich nur das letzte klammerauf interessiert
    if destination_path.endswith(")") and destination_path.find("(") != -1:
        startpoint = destination_path.find("(")
        endpoint = len(destination_path)
        oldint = int(destination_path[startpoint+1:endpoint-1])
        newint = oldint + 1
        new_destination_path = destination_path[0:startpoint] + "(" + str(newint) + ")"
    else:
        new_destination_path = destination_path + " (1)"
    return new_destination_path


#filesmp4 = glob.glob('**/*.mp4', recursive=True)
#filesjpg = glob.glob('**/*.jpg', recursive=True)
#filespng = glob.glob('**/*.png', recursive=True)
#filespdf = glob.glob('**/*.pdf', recursive=True)
#filesext = filesmp4 + filesjpg + filespng + filespdf

#Hier wurde vergessen zu prüfen ob der pfad eine datei oder ein ordner ist. das müsste man noch einbauen
#es fässt auch keine dateien an die keine datei endung haben
filesext = glob.glob('**/*', recursive=True)

#Path generation
years = ["2001","2002","2003","2004","2005","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018","2019","2020","2021","2022","2023"]
month = ["01","02","03","04","05","06","07","08","09","10","11","12"]

#Foldername generation
notinfoldernameallowedpersonal = []
notinfoldernameallowedgeneral = []

notinfoldernameallowed = notinfoldernameallowedpersonal + notinfoldernameallowedgeneral + years + month

folderwillbeignoredpersonal = []
folderwillbeignoredgeneral = []

folderwillbeignored = folderwillbeignoredpersonal #+ folderwillbeignoredgeneral
allfoldername = []

for files in filesext:
    ignore = False
    if not os.path.isfile(files):
        ignore = True
        continue
    splittedpath = files.split("/")
    #Foldername generation
    newfoldername = ""
    for folder in splittedpath:
        if folder in folderwillbeignored:
            ignore = True
        elif folder.lower() in notinfoldernameallowed or folder in notinfoldernameallowed or folder.isnumeric() or (folder.startswith("-") and folder[1:].isnumeric()):
            continue
        elif newfoldername == "" and folder == splittedpath[-1]:
            newfoldername = "ZZZ"
        elif newfoldername == "" and folder != splittedpath[-1]:
            newfoldername = folder
        elif newfoldername != "" and folder != splittedpath[-1]:
            newfoldername += " - " + folder
        #wenn es eine Datei ist die per Whatsapp verschickt wurde soll das in den newfoldernem hinzugefügt werden
        if folder == splittedpath[-1] and folder.find("-WA") != -1 and newfoldername.find("Whatsapp") == -1:
            newfoldername += " - " + "Whatsapp"
        #wenn dateiname enthält Whatsapp soll das in den newfoldername hinzugefügt werden
        if folder == splittedpath[-1] and folder.find("Whatsapp") != -1 and newfoldername.find("Whatsapp") == -1:
            newfoldername += " - " + "Whatsapp"
        #wenn es eine Datei ist die Screenshot im namen hat soll Screenshot zum newfoldername hinzugefügt werden
        if folder == splittedpath[-1] and folder.find("Screenshot") != -1 and newfoldername.find("Screenshot") == -1:
            newfoldername += " - " + "Screenshot"
        if folder == splittedpath[-1] and folder.find("signal") != -1 and newfoldername.find("Signal") == -1:
            newfoldername += " - " + "Signal"
        if not ignore and folder != splittedpath[-1] and folder not in allfoldername:
            allfoldername.append(folder)
    if ignore:
        continue
    else:
        #Path generation
        splittedpath = files.split("/")
        newpath = ""
        appendtofoldernameifnotexits = ""
        filename = splittedpath[-1]
        if filename.startswith("VID-") and checkvaliddate(filename[4:8],filename[8:10]) :
            newpath = "/" + filename[4:8] + "/" + filename[8:10] + "/"
        elif filename.startswith("VID_") and checkvaliddate(filename[4:8],filename[8:10]):
            newpath = "/" + filename[4:8] + "/" + filename[8:10] + "/"
        elif filename.startswith("IMG-") and checkvaliddate(filename[4:8],filename[8:10]):
            newpath = "/" + filename[4:8] + "/" + filename[8:10] + "/"
        elif filename.startswith("IMG_") and checkvaliddate(filename[4:8],filename[8:10]):
            newpath = "/" + filename[4:8] + "/" + filename[8:10] + "/"
        elif filename.startswith("IMG_") and checkvaliddate(filename[4:8],filename[9:11]):
            newpath = "/" + filename[4:8] + "/" + filename[9:11] + "/"
        elif filename.startswith("JPEG") and checkvaliddate(filename[5:9],filename[9:11]):
            newpath = "/" + filename[5:9] + "/" + filename[9:11] + "/"
        elif filename.startswith("AUD-") and checkvaliddate(filename[4:8],filename[8:10]):
            newpath = "/" + filename[4:8] + "/" + filename[8:10] + "/"
        elif filename.startswith("PTT-") and checkvaliddate(filename[4:8],filename[8:10]):
            newpath = "/" + filename[4:8] + "/" + filename[8:10] + "/"
        elif filename.startswith("LOVOO") and checkvaliddate(filename[6:10],filename[11:13]):
            newpath = "/" + filename[6:10] + "/" + filename[11:13] + "/"
        elif filename.startswith("signal") and checkvaliddate(filename[7:11],filename[12:14]):
            newpath = "/" + filename[7:11] + "/" + filename[12:14] + "/"
        elif filename.startswith("Screenshot") and checkvaliddate(filename[11:15],filename[15:17]):
            newpath = "/" + filename[11:15] + "/" + filename[15:17] + "/"
        elif filename.startswith("Screenshot") and checkvaliddate(filename[11:15],filename[16:18]):
            newpath = "/" + filename[11:15] + "/" + filename[16:18] + "/"
        elif filename.startswith("Bildschirmfoto") and checkvaliddate(filename[15:19],filename[20:22]):
            #Bildschirmfoto 2018-07-10 um 15.35.02.png
            newpath = "/" + filename[15:19] + "/" + filename[20:22] + "/"
        elif filename.startswith("photo") and checkvaliddate(filename[6:10],filename[11:13]):
            #photo_2020-04-17_18-40-15.jpg
            newpath = "/" + filename[6:10] + "/" + filename[11:13] + "/"
        elif filename.startswith("Capture") and checkvaliddate(filename[8:12],filename[13:15]):
            #Capture_2018-04-05-12-57-21.png
            newpath = "/" + filename[8:12] + "/" + filename[13:15] + "/"
        elif filename.startswith("WhatsApp Video") and checkvaliddate(filename[15:19],filename[20:22]):
            newpath = "/" + filename[15:19] + "/" + filename[20:22] + "/"
        elif filename.startswith("Doc ") and filename.endswith(".pdf"):
            #Doc Feb 24 2022(2).pdf
            month = convertfrommonthtonumber(filename[4:7])
            year = filename[11:15]
            if checkvaliddate(year,month):
                newpath = "/" + year + "/" + month + "/"
        elif checkvaliddate(filename[0:4],filename[4:6]):
            newpath = "/" + filename[0:4] + "/" + filename[4:6] + "/"
        elif checkvaliddate(filename[0:4],filename[5:7]):
            #2020_09_13-22_Samuel_Mertins_Arbeitsnachweis.xlsx
            newpath = "/" + filename[0:4] + "/" + filename[5:7] + "/"
        elif filename.endswith(".eml"):
            #1009626642.171699735793507687.1.2.eml
            datum = get_date_out_of_mail(files)
            if datum != "":
                newpath = "/" + datum[0:4] + "/" + datum[4:6] + "/"
        #Wenn es bis hier hin leer ist checke die metadaten
        if newpath == "":
            try:
                newpath = get_newpath_from_metadata(files)    
            except Exception as e:
                newpath = ""
        #Wenn es bis hier hin leer ist checke die filesystem daten
        if newpath == "":
            date = get_file_date(files)
            #eigendlich noch prüfen welches das frühste ist
            aenderungsdatum = date["Änderungsdatum"]
            datum = aenderungsdatum.isoformat()
            if checkvaliddate(datum[0:4],datum[5:7]):
                newpath = "/" + datum[0:4] + "/" + datum[5:7] + "/"
        newfiles = "/4TB/medien/" + newpath[1:] + newfoldername
        #newfiles = newpath[1:] + newfoldername
        if files != newfiles + "/" + filename and not newfoldername.startswith("/4TB/medien/20") and files.startswith("20"):
            print(files)
            print(newfiles + "/" + filename)
            #print(files)
            #print(filename)
            #print("new:")
            #print(newpath[1:] + newfoldername)
            #print(newfoldername)
            example = files
            #decistion = "verschieben" #WARNUNG
            decistion = ""
            #decistion = input("1. nichts 2. copy 3. verschieben")
            if decistion == "nichts" or decistion == "":
                print("")
                continue
            elif decistion == "copy" or decistion == "verschieben":
                createfolder(newfiles)
                fileinteraction(files,newfiles,filename,decistion)
            print("")

#allfoldername

