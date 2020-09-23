import sys, os
sys.path.insert(0, 'data')
from Engine import *

global loaded
loaded = 0

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
	if loaded == 0:
		print('Tsundere RPG version 0.0.0A')
	if loaded == 1:
		print('Tsundere RPG version 0.0.0A\n')
		print(Player.Get.name(),'|HP:',Player.Get.hp(),'|MP:',Player.Get.mp(),'|A:',Player.Get.agility(),'|P:',Player.Get.power(),'|S:',Player.Get.senses(),'|M:',Player.Get.magic(),'|D:',Player.Get.deff())

def console(fight):
	cl = input('Ação: ')
	if 'new' in cl:
		new()
	if 'adm' in cl:
		Player.Update.local(1)

header(loaded)
console(0)
