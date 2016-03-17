from kivy.network.urlrequest import UrlRequest
import json
import random
import urllib2
import os

class LevelData():
	def __init__(self, image, answers, data_id):
		self.image = image
		self.answers = answers
		self.data_id = data_id

class GameData():
	def __init__(self):
		self.level_data = []
		self.get_game_data()

	def get_level_data(self):
		#gets all data_id
		data_ids =[datum.data_id for datum in self.level_data]
		#gets all level completed from json file
		levels_completed = self.read_data('levels_completed.json')
		try:
			#all data minus level completed then random
			random_no = random.sample(set(data_ids) - set(levels_completed),1)[0]
			return self.level_data[random_no]
		#no more data
		except ValueError:
			return ''
	
	#gets all game data from images json file
	def get_game_data(self):		
		with open(os.getcwd()+'/data/images-test.json') as json_file:
			json_data = json.load(json_file)
			for datum in json_data:
				self.level_data.append(LevelData(datum["image"], 
											datum["answers"],
											datum["data_id"]))

	#saves data (json files)
	def store_data(self, id_data, filename):
		if filename == 'levels_completed.json':
			data = self.read_data(filename)
			data.append(id_data)
		else:
			data = id_data
		with open(os.getcwd()+'/data/'+filename, 'w') as outfile:
			json.dump(data, outfile)
		#print(os.getcwd())

	#reads data (json files) 
	def read_data(self, filename):		
		with open(os.getcwd()+'/data/'+filename) as json_file:
			json_data = json.load(json_file)
		return json_data

	
	#for future data update (not working yet)
	def update(self):
		url = 'http://apiquiz.herokuapp.com/export.json'
		response = urllib2.urlopen(url)
		data = json.load(response)

		with open(os.getcwd()+'/data/images.json', 'w') as outfile:
			json.dump(data, outfile)
		#print(os.getcwd())



