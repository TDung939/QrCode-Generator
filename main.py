from __future__ import print_function
from googleapiclient.discovery import build
from google.oauth2 import service_account
import io
import qrcode

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1jiWgMKMsIiTXWnAM50G42F26dkd3LXvD7zgZwNH2VQA'

def printQr(name, value):
  qr = qrcode.QRCode()
  qr.add_data(value)
  f = io.StringIO()
  qr.print_ascii(out=f)
  f.seek(0)
  print(f.read())

def generateQr(name, value):
  img = qrcode.make(value)
  img.save('./qrcodes/' + name + '.jpg')
  
def main():
    creds = None
    creds = service_account.Credentials.from_service_account_file('token.json', scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range='qrcode!A1:G13').execute()

    values = result.get('values', [])
    for value in values:
      print(value)
      try:
        generateQr(value[0], value[1])
      except:
        print('no id')

if __name__ == '__main__':
    main()