import sys, os
sys.path.insert(0, 'data')
from Engine import *

loaded = False

def loadedd():
	global loaded
	loaded = True

def new():
	header(loaded)
	name = input('Nome: ')
	if System.CheckSave(name) == 1:
		System.NewSave(name)
		
	if System.CheckSave(name) == 0:
		print('Já existe um save com esse nome\ndeseja subescrever? [y/n]')
		check = input('Opção:')
		if check in ['y','Y']:
			System.NewSave(name)
		else:
			console(0)

def header(loaded):
	os.system('cls')
	if loaded == False:
		print('Tsundere RPG version 0.0.0A')
	if loaded == True:
		print('Tsundere RPG version 0.0.0A')
		print(Player.Get.name(),'|HP:',Player.Get.hp(),'|MP:',Player.Get.mp(),'|A:',Player.Get.agility(),'|P:',Player.Get.power(),'|S:',Player.Get.senses(),'|M:',Player.Get.magic(),'|D:',Player.Get.deff())

def console(mode):
	cl = input('Ação: ')
	if '/new' in cl:
		new()

	if '/load' in cl:
		header(loaded)
		if System.FindSaves() == True:
			loadedd()
		header(loaded)
		console(loaded)

	if loaded == True:

		if '/lvlUp' in cl:
			header(loaded)
			System.levelUp()
			input('\nPrecione Enter para continuar')
			header(loaded)
			console(loaded)

		if '/stats' in cl:
			header(loaded)
			System.Check.stats()
			input('\nPrecione Enter para continuar')
			header(loaded)
			console(loaded)

		if '/xp' in cl:
			amount = input()
			Player.Update.xp(amount)

		if '/rec' in cl:
			Player.Restore.hp('full')

		if '/mod' in cl:
			header(loaded)
			print('Sistema ainda não implementado\n')
			input('Precione Enter para continuar')
			header(loaded)
			console(loaded)

		if 'get' in cl:
			System.BattleSystem.createEnemy(1)
			input('')
header(loaded)
console(loaded)
