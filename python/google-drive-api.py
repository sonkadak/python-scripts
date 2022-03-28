import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint


scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

client = gspread.authorize(creds)

sheet = client.open("Rackmount").sheet1

json_data = sheet.get_all_records()

for item in json_data:
    print(item['Hostname'])
# pprint(target)