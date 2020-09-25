import json, os, random, time

#Tables-----------------------
xpTable = [100,150,200,250,300,350,400,450,500,550,600]
hpTable = [100,110,120,130,140,150,160,170,180,190,200]
mpTable = [10,20,30,40,50,60,70,80,90,100]

class System:
	def NewSave(name):
		rawPlayerData = {
			"name":name,
			"race":"Humano",
			"hp":100,
			"mp":10,
			"maxHp":100,
			"maxMp":10,
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
			"deff":0,
			"weapon1":0,
			"subWeapon1":0,
			"subWeapon2":0,
			"xp":1000,
			"debug":0
			}
		saveName = 'Saves/'+name+'.JDere'
		jsonPlayerData = json.dumps(rawPlayerData, indent=1)
		openFile = open(saveName,'w')
		openFile.write(jsonPlayerData)
		openFile.close()

	def LoadData(name):
		saveName = 'Saves/'+name+'.JDere'
		global rawData
		with open(saveName, 'r+') as rawData:
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

	def levelUp():
		if pld['xp'] >= xpTable[pld['lvl']]:
			os.system('cls')
			lvl = pld["lvl"] +1
			oldHP = Player.Get.maxHp()
			newHP = hpTable[lvl]
			oldMP = Player.Get.maxMp()
			newMP = mpTable[lvl]
			#Update values----
			VarPoints = Player.Get.upPoints() +1
			Player.Update.upPoints(VarPoints)

			VarXp = Player.Get.xp() -xpTable[Player.Get.lvl()]
			Player.Update.xp(VarXp)

			VarLvl = Player.Get.lvl() +1
			Player.Update.lvl(VarLvl)

			Player.Update.maxHp(newHP)
			Player.Update.maxMp(newMP)

			Player.Restore.hp('full')
			Player.Restore.mp('full')
			
			#Update values----
			upMessage = '\nAumentando o seu nível você obteve uma melhora de Hp de {oldHp} para {newHp}\ne tambem uma melhora de Mp de {oldMp} para {newMp}\n tambem recebeu 1 ponto de modificador que pode ser usado com /mod'.format(oldHp=oldHP,newHp=newHP,oldMp=oldMP,newMp=newMP)
			return print(upMessage)
		else:
			return print('\nParece que você ainda não atende aos requeimentos necessários para subir de\nnível, volte denovo quando tiver XP suficiente pra isso')

	class Check:
		def stats():
			if pld['xp'] >= xpTable[pld['lvl']]:
				return print('Parece que você está pronto para subir de nível\nUse /lvlUp para passar para o próximo nível')

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
		def weapon1():
			return pld["weapon1"]
		def subWeapon1():
			return["subWeapon1"]
		def subWeapon2():
			return pld["subWeapon2"]
		def xp():
			return pld["xp"]

	class Restore:
		def hp(ammount):
			addHealth=0
			hpMax = Player.Get.maxHp()

			if ammount == 'full':
				addHealth = Player.Get.maxHp()
			else:
				addHealth = Player.Get.hp() + ammount

			if addHealth < hpMax:
				addHealth = Player.Get.maxHp()

			Player.Update.hp(addHealth)

		def mp(ammount):
			addMana=0
			mpMax = Player.Get.maxMp()

			if ammount == 'full':
				addMana = Player.Get.maxMp()

			else:
				addMana = Player.Get.mp() + ammount

			if addMana < mpMax:
				addMana = Player.Get.maxMp()

			Player.Update.mp(addMana)

	class Update:
		global _UPDATE_

		def _UPDATE_(up,value):
			saveName = 'Saves/'+nameVar+'.JDere'
			with open(saveName, 'r+') as rawData:
				data = json.load(rawData)
				rawData.seek(0)
				data[up] = value
				json.dump(data, rawData, indent=1)
				rawData.truncate()
				rawData.close()

		def local(upLocal):
			_UPDATE_('local',upLocal)

		def hp(hpUp):
			_UPDATE_('hp',hpUp)

		def mp(mpUp):
			_UPDATE_('mp',mpUp)

		def maxHp(maxHpUp):
			_UPDATE_('maxHp',maxHpUp)

		def maxMp(maxMpUp):
			_UPDATE_('maxMp',maxMpUp)

		def power(powerUp):
			_UPDATE_('power',powerUp)

		def senses(sensesUp):
			_UPDATE_('senses',sensesUp)

		def agility(agilityUp):
			_UPDATE_('agility',agilityUp)

		def magic(magicUp):
			_UPDATE_('magic',magicUp)

		def lvl(lvlUp):
			_UPDATE_('lvl',lvlUp)

		def upPoints(upPointsUp):
			_UPDATE_('upPoints',upPointsUp)

		def localList(localListUp):
			_UPDATE_('localList',localListUp)

		def history(historyUp):
			_UPDATE_('history',historyUp)

		def inv1(inv1Up):
			_UPDATE_('inv1',inv1Up)

		def inv2(inv2Up):
			_UPDATE_('inv2',inv2Up)

		def inv3(inv3Up):
			_UPDATE_('inv3',inv3Up)

		def inv4(inv4Up):
			_UPDATE_('inv4',inv4Up)

		def inv5(inv5Up):
			_UPDATE_('inv5',inv5Up)

		def deff(deffUp):
			_UPDATE_('deff',deffUp)

		def weapon1(weapon1Up):
			_UPDATE_('weapon1',weapon1Up)

		def subWeapon1(subWeapon1Up):
			_UPDATE_('subWeapon1',subWeapon1Up)

		def subWeapon2(subWeapon2Up):
			_UPDATE_('subWeapon2',subWeapon2Up)

		def xp(xpUp):
			_UPDATE_('xp',xpUp)