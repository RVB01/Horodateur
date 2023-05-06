from PIL import Image, ImageFont, ImageDraw, UnidentifiedImageError
import pathlib
import os
import datetime
import argparse
import re
import locale
from dateutil import relativedelta


def age(date_photo, naissance):
    date_naissance = datetime.datetime.strptime(naissance, '%d/%m/%Y')
    age = relativedelta.relativedelta(date_photo, date_naissance)
    return "{mois}m. {jours}j.".format(mois=age.months, jours=age.days)

locale.setlocale(locale.LC_ALL, 'fr_FR.utf8') # excuse I'm french

format_date = re.compile('.*(\d{4}-\d{2}-\d{2}).*')

parser = argparse.ArgumentParser(
                    prog='horodateur',
                    description='Ajoute la date des photos sur l\'image',
                    epilog='')

parser.add_argument('-s', '--source', type=pathlib.Path, required=True, help='dossier contenant les photos à traiter')
parser.add_argument('-d', '--destination', type=pathlib.Path, required=True, help='dossier de destination des photos traitées, crée si inexistant')
parser.add_argument('-p', '--prenom', nargs="*", type=str, required=False, help='ajoute le prénom et l\'age de l\'enfant à partir de sa date de naissance avec le format suivant : Prénom:01/01/2000')
parser.add_argument('-m', '--methode', choices=['nom', 'metadonnees', 'metadonnées'], required=True, help='méthode de récupération de la date (dans le nom du fichier format YYYY-MM-DD ou dans les métadonnées)')
args = parser.parse_args()

args.destination.mkdir(exist_ok=True)
photos = [f for f in args.source.iterdir() if f.is_file()]
for photo in photos:
    try:
        if args.methode == 'nom':
            date_brute = re.search(format_date, photo.name).groups()
            if len(date_brute) == 1:
                date_photo_daytime = datetime.datetime.strptime(date_brute[0], "%Y-%m-%d")
                date_photo = str(date_photo_daytime.strftime("%d %b %Y"))
            else:
                raise RuntimeError("Erreur lors de la récupération de la date dans le nom du fichier")
        elif args.methode == 'metadonnees' or args.methode == 'metadonnées':
            date_unix = os.path.getmtime(photo)
            date_photo_daytime = datetime.datetime.fromtimestamp(date_unix)
            date_modif = date_photo_daytime.strftime('%d %b %Y')
            date_photo = str(date_modif)

        # On retire éventuellement le 1er zéro de la date
        date_photo = date_photo.lstrip('0')
        for prenom in args.prenom:
            date_photo += '\n{prenom} ({age})'.format(prenom=prenom.split(':')[0], age=age(date_photo_daytime, prenom.split(':')[1]))

        fond = Image.open(photo).convert('RGBA')
        police = ImageFont.truetype("calibri.ttf", 40)
        
        surcouche = Image.new('RGBA', fond.size, (255, 255, 255, 0))
        dessin_surcouche = ImageDraw.Draw(surcouche)

        larg, haut = fond.size
        position = (larg*0.7, haut*0.8)
        bbox = dessin_surcouche.textbbox(position, date_photo, font=police)

        dessin_surcouche.rectangle(bbox, fill=(10,10,25,100))
        dessin_surcouche.text(position, f"{date_photo}", font=police, fill=(255,255,255))
        out = Image.alpha_composite(fond, surcouche).convert('RGB')
        out.save(args.destination / photo.name)
    except FileNotFoundError as fnfe:
        print('Erreur du traitement de '+ str(photo)+ ": " + str(fnfe))
    except UnidentifiedImageError as uie:
        pprint('Erreur du traitement de '+ str(photo)+ ": " + str(uie))
    except ValueError as ve:
        print('Erreur du traitement de '+ str(photo)+ ": " + str(ve))
    except OSError as ose:
        print('Erreur du traitement de '+ str(photo)+ ": " + str(ose))
    except RuntimeError as rte:
        print('Erreur du traitement de '+ str(photo)+ ": " + str(rte))
    except IndexError as ie:
        print('Erreur du traitement de '+ str(photo)+ ": " + str(ie) + '\nAvez vous précisé la date de naissance ?')