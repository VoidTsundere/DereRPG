import json, os, random

class System:
	def NewSave(name):
		rawPlayerData = {
			"name":name,
			"race":"Humano",
			"hp":100,
			"mp":10,
			"maxHp":100,
			"marMp":10,
			"power":0,
			"agility":0,
			"senses":0,
			"magic":0,
			"lvl":0,
			"upPoints":0,
			"local":0,
			"localList":0,
			"history":0,
			"inv1":0,
			"inv2":0,
			"inv3:":0,
			"inv4":0,
			"inv5":0,
			"deff":0
			}
		saveName = 'Saves/'+name+'.JDere'
		jsonPlayerData = json.dumps(rawPlayerData, indent=2)
		openFile = open(saveName,'w')
		openFile.write(jsonPlayerData)
		openFile.close()

	def LoadData(name):
		saveName = 'Saves/'+name+'.JDere'
		global rawData
		with open(saveName, 'r') as rawData:
			global pld
			pld = json.load(rawData)
			global nameVar
			nameVar = name
			rawData.close()

	def CheckSave(name):
		saveName = 'Saves'+name+'.JDere'
		if os.path.exists(saveName) == True:
			return 0
		if os.path.exists(saveName) == False:
			return 1

class Player:
	class Get:
		def name():
			return pld["name"]
		def hp():
			return pld["hp"]
		def mp():
			return pld["mp"]
		def maxHp():
			return pld["maxHp"]
		def maxMp():
			return pld["maxMp"]
		def power():
			return pld["power"]
		def agility():
			return pld["agility"]
		def senses():
			return pld["senses"]
		def magic():
			return pld["magic"]
		def lvl():
			return pld["lvl"]
		def upPoints():
			return pld["upPoints"]
		def local():
			return pld["local"]
		def localList():
			return pld["localList"]
		def history():
			return pld["history"]
		def inv1():
			return pld["inv1"]
		def inv2():
			return pld["inv2"]
		def inv3():
			return pld["inv3"]
		def inv4():
			return pld["inv4"]
		def inv5():
			return pld["inv5"]
		def deff():
			return pld["deff"]

	class Update:
		global _UPDATE_

		def _UPDATE_(up,value):
			saveName = 'Saves/'+nameVar+'.JDere'
			with open(saveName, 'r+') as rawData:
				data = json.load(rawData)
				data[up] = value
				rawData.seek(0)
				json.dump(data, rawData, indent=2)
				rawData.close()

		def local(upLocal):
			_UPDATE_('local',upLocal)

		def hp(hpUp):
			_UPDATE_('hp',hpUp)
