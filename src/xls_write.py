import logging
import xlsxwriter
from typing import List
from xlsxwriter.worksheet import Worksheet

from alarm import Alarm
from alarm_category import AlarmCategory
from symbol import Symbol

logger = logging.getLogger(__name__)


alarm_categories = [
    AlarmCategory(r'stS\d+DefImdt\w*\.', (165,42,42), (0,0,0)),
    AlarmCategory(r'stS\d+DefFcy\w*\.', (165,42,42), (0,0,0)),
    AlarmCategory(r'stS\d+DefAttente\w*\.', (0,0,255), (255,255,255)),
    AlarmCategory(r'stS\d+Avert\w*\.', (255,215,0), (0,0,0)),
    AlarmCategory(r'stS\d+Message\w*\.', (0,0,255), (255,255,255)),
]


def write_headers(worksheet: Worksheet):
    worksheet.write('A1', 'VERSION')
    worksheet.write('B1', '4')
    worksheet.write('C1', 'HARDWARE_VERSION')
    worksheet.write('D1', '159')

    headers = [
        "Catégorie",
        "Priorité",
        "Type Adresse",
        "Nom API (Lecture)",
        "Type variable (Lecture)",
        "Tag Système (lecture)",
        "Tag Utilisateur (Lecture)",
        "Adresse (Lecture)",
        "Index (Lecture)",
        "Format donnée (Lecture)",
        "Notification activé",
        "Activé (Notification)",
        "Nom API (Notification)",
        "Type variable (Notification)",
        "Tag Système (Notification)",
        "Tag Stilisateur (Notification)",
        "Adresse (Notification)",
        "Index (Notification)",
        "Condition",
        "Valeur de déclenchement",
        "Contenu",
        "bibliothèque de Labels activé",
        "Nom de label",
        "Police",
        "Couleur",
        "Valeur Acquittement",
        "Son activé",
        "Nom de la bibliothèque de sons",
        "Index son",
        "Nombre de multi-watch",
        "Nom API (WATCH1)",
        "Type variable (WATCH1)",
        "Tag Système (WATCH1)",
        "Tag Utilisateur (WATCH1)",
        "Addresse (WATCH1)",
        "Index (WATCH1)",
        "Format de donnée (WATCH1)",
        "Nbr. De mots (WATCH1)",
        "Nom API (WATCH2)",
        "Type variable (WATCH2)",
        "Tag Système (WATCH2)",
        "Tag Utilisateur (WATCH2)",
        "Addresse (WATCH2)",
        "Index (WATCH2)",
        "Format de donnée (WATCH2)",
        "Nbr. De mots (WATCH2)",
        "Nom API (WATCH3)",
        "Type variable (WATCH3)",
        "Tag Système (WATCH3)",
        "Tag Utilisateur (WATCH3)",
        "Addresse (WATCH3)",
        "Index (WATCH3)",
        "Format de donnée (WATCH3)",
        "Nbr. De mots (WATCH3)",
        "Nom API (WATCH4)",
        "Type variable (WATCH4)",
        "Tag Système (WATCH4)",
        "Tag Utilisateur (WATCH4)",
        "Addresse (WATCH4)",
        "Index (WATCH4)",
        "Format de donnée (WATCH4)",
        "Nbr. De mots (WATCH4)",
        "Nom API (WATCH5)",
        "Type variable (WATCH5)",
        "Tag Système (WATCH5)",
        "Tag Utilisateur (WATCH5)",
        "Addresse (WATCH5)",
        "Index (WATCH5)",
        "Format de donnée (WATCH5)",
        "Nbr. De mots (WATCH5)",
        "Nom API (WATCH6)",
        "Type variable (WATCH6)",
        "Tag Système (WATCH6)",
        "Tag Utilisateur (WATCH6)",
        "Addresse (WATCH6)",
        "Index (WATCH6)",
        "Format de donnée (WATCH6)",
        "Nbr. De mots (WATCH6)",
        "Nom API (WATCH7)",
        "Type variable (WATCH7)",
        "Tag Système (WATCH7)",
        "Tag Utilisateur (WATCH7)",
        "Addresse (WATCH7)",
        "Index (WATCH7)",
        "Format de donnée (WATCH7)",
        "Nbr. De mots (WATCH7)",
        "Nom API (WATCH7)",
        "Type variable (WATCH8)",
        "Tag Système (WATCH8)",
        "Tag Utilisateur (WATCH8)",
        "Addresse (WATCH8)",
        "Index (WATCH8)",
        "Format de donnée (WATCH8)",
        "Nbr. De mots (WATCH8)",
        "Bip continu",
        "Condition d’arrêt du bip continu",
        "Intervalle des bips",
        "Envoyer e-mail au déclenchement de l'alarme",
        "Envoi e-mail au retour à la normale de l'alarme",
        "Destinataires (déclenchement)",
        "Destinataires Cc (déclenchement)",
        "Destinataires Cci (déclenchement)",
        "Utilise contenu de l'alarme comme sujet (déclenchement)",
        "Sujet (déclenchement)",
        "Utilise la bibliothèque label (déclenchement)",
        "Nom du label (déclenchement)",
        "Entête (déclenchement)",
        "Utilise la bibliothèque label (déclenchement)",
        "Nom du label (Entête)",
        "Signature (déclenchement)",
        "Utilise la bibliothèque label (signature)",
        "Nom du label (signature)",
        "Capture écran",
        "Destinataires (Retour à la normale)",
        "Destinataires Cc (Retour à la normale)",
        "Destinataires Cci (Retour à la normale)",
        "Utilise contenu de l'alarme comme sujet (Retour à la normale)",
        "Sujet (Retour à la normale)",
        "Utilise la bibliothèque label (Retour à la normale)",
        "Nom du label (Retour à la normale)",
        "Entête (Retour à la normale)",
        "Utilise la bibliothèque label (Retour à la normale)",
        "Nom du label (Entête)",
        "Signature (Retour à la normale)",
        "Utilise la bibliothèque label (signature)",
        "Nom du label (signature)",
        "Délais",
        "Condition dynamique",
        "Nom API (Condition)",
        "Type variable (Condition)",
        "Tag Système (Condition)",
        "Tag Utilisateur (Condition)",
        "Adresse (Condition)",
        "Index (Condition)",
        "Format donnée (Condition)",
        "Occurrence",
        "Nom API (Occurrence)",
        "Type variable (Occurrence)",
        "Tag Système (Occurrence)",
        "Tag Utilisateur (Occurrence)",
        "Adresse (Occurrence)",
        "Index (Occurrence)",
        "Format donnée (Occurrence)",
        "Dans tolérance",
        "Hors tolérance",
        "Suivre",
        "Utiliser chaine de caractère",
        "ID Section",
        "Dynamique",
        "ID chaine enregistrement"
        "ID Chaine",
        "Nom API (ID Chaine)",
        "Type variable (ID Chaine)",
        "Tag Système (ID Chaine)",
        "Tag Utilisateur (ID Chaine)",
        "Adresse (ID Chaine)",
        "Index (ID Chaine)",
        "Format donnée (ID Chaine)",
        "Push Notification",
        "Temps écoulé",
        "Nom API (Temps écoulé)",
        "Type variable (Temps écoulé)",
        "Tag Système (Temps écoulé)",
        "Tag Utilisateur (Temps écoulé)",
        "Adresse (Temps écoulé)",
        "Index (Temps écoulé)",
        "Format donnée (Temps écoulé)",
        "Couleur de fond",
        "Couleur (Couleur de fond)",
        "Sous-catégorie 1",
        "Sous-catégorie 2",
        "Contrôle (Activer/Désactiver)",
        "Mise à ON (Activer/Désactiver)",
        "Nom du périphérique (Activer/Désactiver)",
        "Type de périphérique (Activer/Désactiver)",
        "Tag système (Activer/Désactiver)",
        "Tag définie par l’utilisateur (Activer/Désactiver)",
        "Adresse (Activer/Désactiver)",
        "Index (Activer/Désactiver)"
    ]

    for i, header in enumerate(headers):
        worksheet.write(1, i, header)


def get_row_data(category_id: int, symbol: Symbol):
    # TODO: Use a parameter instead for plc_name
    plc_name = "PZ_PLC"
    address = symbol.name
    message = symbol.comment

    font_color = str(alarm_categories[category_id].font_color)
    bg_color = str(alarm_categories[category_id].bg_color)

    return [
        f"{category_id}: Category {category_id}",   # Catégorie
        "Low",                  # Priorité
        "Bit",                  # Type Adresse
        plc_name,               # Nom API (Lecture)
        "BOOL",                 # Type variable (Lecture)
        "False",                # Tag Système (lecture)
        "False",                # Tag Utilisateur (Lecture)
        address,                # Adresse (Lecture)
        "null",                 # Index (Lecture)
        " ",                    # Format donnée (Lecture)
        "False",                # Notification activé
        "False",                # Activé (Notification)
        "",                     # Nom API (Notification)
        "",                     # Type variable (Notification)
        "False",                # Tag Système (Notification)
        "False",                # Tag Stilisateur (Notification)
        "",                     # Adresse (Notification)
        "null",                 # Index (Notification)
        "bt: 1",                # Condition
        "0",                    # Valeur de déclenchement
        message,                # Contenu
        "False",                # bibliothèque de Labels activé
        "",                     # Nom de label
        "Droid Sans Fallback",  # Police
        font_color,             # Couleur
        "11",                   # Valeur Acquittement
        "False",                # Son activé
        "",                     # Nom de la bibliothèque de sons
        "0",                    # Index son
        "0",                    # Nombre de multi-watch
        "",                     # Nom API (WATCH1)
        "",                     # Type variable (WATCH1)
        "False",                # Tag Système (WATCH1)
        "False",                # Tag Utilisateur (WATCH1)
        "",                     # Addresse (WATCH1)
        "null",                 # Index (WATCH1)
        "",                     # Format de donnée (WATCH1)
        "",                     # Nbr. De mots (WATCH1)
        "",                     # Nom API (WATCH2)
        "",                     # Type variable (WATCH2)
        "False",                # Tag Système (WATCH2)
        "False",                # Tag Utilisateur (WATCH2)
        "",                     # Addresse (WATCH2)
        "null",                 # Index (WATCH2)
        "",                     # Format de donnée (WATCH2)
        "",                     # Nbr. De mots (WATCH2)
        "",                     # Nom API (WATCH3)
        "",                     # Type variable (WATCH3)
        "False",                # Tag Système (WATCH3)
        "False",                # Tag Utilisateur (WATCH3)
        "",                     # Addresse (WATCH3)
        "null",                 # Index (WATCH3)
        "",                     # Format de donnée (WATCH3)
        "",                     # Nbr. De mots (WATCH3)
        "",                     # Nom API (WATCH4)
        "",                     # Type variable (WATCH4)
        "False",                # Tag Système (WATCH4)
        "False",                # Tag Utilisateur (WATCH4)
        "",                     # Addresse (WATCH4)
        "null",                 # Index (WATCH4)
        "",                     # Format de donnée (WATCH4)
        "",                     # Nbr. De mots (WATCH4)
        "",                     # Nom API (WATCH5)
        "",                     # Type variable (WATCH5)
        "False",                # Tag Système (WATCH5)
        "False",                # Tag Utilisateur (WATCH5)
        "",                     # Addresse (WATCH5)
        "null",                 # Index (WATCH5)
        "",                     # Format de donnée (WATCH5)
        "",                     # Nbr. De mots (WATCH5)
        "",                     # Nom API (WATCH6)
        "",                     # Type variable (WATCH6)
        "False",                # Tag Système (WATCH6)
        "False",                # Tag Utilisateur (WATCH6)
        "",                     # Addresse (WATCH6)
        "null",                 # Index (WATCH6)
        "",                     # Format de donnée (WATCH6)
        "",                     # Nbr. De mots (WATCH6)
        "",                     # Nom API (WATCH7)
        "",                     # Type variable (WATCH7)
        "False",                # Tag Système (WATCH7)
        "False",                # Tag Utilisateur (WATCH7)
        "",                     # Addresse (WATCH7)
        "null",                 # Index (WATCH7)
        "",                     # Format de donnée (WATCH7)
        "",                     # Nbr. De mots (WATCH7)
        "",                     # Nom API (WATCH7)
        "",                     # Type variable (WATCH8)
        "False",                # Tag Système (WATCH8)
        "False",                # Tag Utilisateur (WATCH8)
        "",                     # Addresse (WATCH8)
        "null",                 # Index (WATCH8)
        "",                     # Format de donnée (WATCH8)
        "",                     # Nbr. De mots (WATCH8)
        "False",                # Bip continu
        "NONE",                 # Condition d’arrêt du bip continu
        "10",                   # Intervalle des bips
        "False",                # Envoyer e-mail au déclenchement de l'alarme
        "False",                # Envoi e-mail au retour à la normale de l'alarme
        "",                     # Destinataires (déclenchement)
        "",                     # Destinataires Cc (déclenchement)
        "",                     # Destinataires Cci (déclenchement)
        "",                     # Utilise contenu de l'alarme comme sujet (déclenchement)
        "",                     # Sujet (déclenchement)
        "",                     # Utilise la bibliothèque label (déclenchement)
        "",                     # Nom du label (déclenchement)
        "",                     # Entête (déclenchement)
        "",                     # Utilise la bibliothèque label (déclenchement)
        "",                     # Nom du label (Entête)
        "",                     # Signature (déclenchement)
        "",                     # Utilise la bibliothèque label (signature)
        "",                     # Nom du label (signature)
        "",                     # Capture écran
        "",                     # Destinataires (Retour à la normale)
        "",                     # Destinataires Cc (Retour à la normale)
        "",                     # Destinataires Cci (Retour à la normale)
        "",                     # Utilise contenu de l'alarme comme sujet (Retour à la normale)
        "",                     # Sujet (Retour à la normale)
        "",                     # Utilise la bibliothèque label (Retour à la normale)
        "",                     # Nom du label (Retour à la normale)
        "",                     # Entête (Retour à la normale)
        "",                     # Utilise la bibliothèque label (Retour à la normale)
        "",                     # Nom du label (Entête)
        "",                     # Signature (Retour à la normale)
        "",                     # Utilise la bibliothèque label (signature)
        "",                     # Nom du label (signature)
        "1",                    # Délais
        "0",                    # Condition dynamique
        plc_name,               # Nom API (Condition)
        "BOOL",                 # Type variable (Condition)
        "False",                # Tag Système (Condition)
        "False",                # Tag Utilisateur (Condition)
        address,                # Adresse (Condition)
        "null",                 # Index (Condition)
        "True",                 # Format donnée (Condition)
        "False",                # Occurrence
        "Local HMI",            # Nom API (Occurrence)
        "?",                    # Type variable (Occurrence)
        "False",                # Tag Système (Occurrence)
        "False",                # Tag Utilisateur (Occurrence)
        "0",                    # Adresse (Occurrence)
        "null",                 # Index (Occurrence)
        "16-bit Unsigned",      # Format donnée (Occurrence)
        "",                     # Dans tolérance
        "",                     # Hors tolérance
        "False",                # Suivre
        "False",                # Utiliser chaine de caractère
        "",                     # ID Section
        "",                     # Dynamique
        "",                     # ID chaine enregistrement
        "",                     # ID Chaine
        "",                     # Nom API (ID Chaine)
        "False",                # Type variable (ID Chaine)
        "False",                # Tag Système (ID Chaine)
        "",                     # Tag Utilisateur (ID Chaine)
        "null",                 # Adresse (ID Chaine)
        "",                     # Index (ID Chaine)
        "",                     # Format donnée (ID Chaine)
        "False",                # Push Notification
        "False",                # Temps écoulé
        "",                     # Nom API (Temps écoulé)
        "",                     # Type variable (Temps écoulé)
        "False",                # Tag Système (Temps écoulé)
        "False",                # Tag Utilisateur (Temps écoulé)
        "",                     # Adresse (Temps écoulé)
        "null",                 # Index (Temps écoulé)
        "",                     # Format donnée (Temps écoulé)
        "True",                 # Couleur de fond
        bg_color,               # Couleur (Couleur de fond)
        "",                     # Sous-catégorie 1
        "",                     # Sous-catégorie 2
        "False",                # Contrôle (Activer/Désactiver)
        "True",                 # Mise à ON (Activer/Désactiver)
        "",                     # Nom du périphérique (Activer/Désactiver)
        "",                     # Type de périphérique (Activer/Désactiver)
        "False",                # Tag système (Activer/Désactiver)
        "False",                # Tag définie par l’utilisateur (Activer/Désactiver)
        "",                     # Adresse (Activer/Désactiver)
        "null"                  # Index (Activer/Désactiver)
    ]


def find_matching_category(symbol: Symbol, categories: List[AlarmCategory]):
    return next((cat for cat in categories if cat.is_match(symbol.name)), None)


def write_row(worksheet: Worksheet, row_id, row_data):
    for col_id, value in enumerate(row_data):
        worksheet.write(row_id, col_id, value)


def write_rows_from_symbols(worksheet: Worksheet, symbols: List[Symbol]):
    row_id = 2  # Starts writing at row 3
    for symbol in symbols:
        category = find_matching_category(symbol, alarm_categories)
        if category:
            row_data = get_row_data(category.id, symbol)
            write_row(worksheet, row_id, row_data)
            row_id += 1

def write_rows_from_alarms(worksheet: Worksheet, alarms: List[Alarm]):
    row_id = 2  # Starts writing at row 3
    for alarm in alarms:
        row_data = get_row_data(alarm.category.id, alarm.symbol)
        write_row(worksheet, row_id, row_data)
        row_id += 1


def write_xls_from_symbols(fname: str, symbols: List[Symbol]):
    with xlsxwriter.Workbook(fname) as workbook:
        worksheet = workbook.add_worksheet()
        write_headers(worksheet)
        write_rows_from_symbols(worksheet, symbols)


def write_xls_from_alarms(fname: str, alarms: List[Alarm]):
    with xlsxwriter.Workbook(fname) as workbook:
        worksheet = workbook.add_worksheet()
        write_headers(worksheet)
        write_rows_from_alarms(worksheet, alarms)
