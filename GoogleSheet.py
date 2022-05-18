from RLTracker import *
import gspread
import pandas as pd
from google.oauth2.credentials import Credentials

class UpdateSheet:
	SCOPES = None
	creds = None
	client = None
	google_sh = None
	sheet1 = None
	df = None
	key = None
	def __init__(self, key):
		try:
			self.key = key
			self.SCOPES = ['https://www.googleapis.com/auth/docs', 'https://www.googleapis.com/auth/spreadsheets']
			self.creds = Credentials.from_authorized_user_file('creds.data', self.SCOPES)
			self.client = gspread.authorize(self.creds)
			self.google_sh = self.client.open_by_key(key)
			self.sheet1 = self.google_sh.get_worksheet(0)
			self.df = pd.DataFrame(data=self.sheet1.get_all_records())
		except:
			print("Error initializing Google Sheet")

	def UpdateSheet(self, overview):
		try:
			self.sheet1.append_rows(
				values= [[
					overview.platformUserHandle, 
					overview.ThreesMMR,
					overview.TwosMMR,
					overview.wins,
					overview.goals,
					overview.shots,
					overview.saves
					]])
			return True
		except:
			return False