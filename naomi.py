### Bot Amino Naomi version 0.1 by Akihiko Ken 
import amino
import random
import re
import datetime

client = amino.Client()
client.login(email="secret", password="se4") #вводим пароль и почту от аккаунта бота
sub_client = amino.SubClient(comId='156542274', profile=client.profile) #вместо "id" введите айди сообщества, в котором будет работать чат
ban = 0
tim = 1
hm = [0]
av = []
nom = 0

def on_message(data):
	global ban
	global tim
	global nom
	chatId = data.message.chatId
	nickname = data.message.author.nickname
	content = data.message.content
	vrem = data.message.createdTime[17:19]
	id = data.message.messageId
	print(f"{nickname}: {content}: {chatId} : {ban}: {data.message.type}") # вывод в консоль сообщений и автора этих сообщений
	lis = ['Думаю, да', 'Думаю что нет']
	
	content = str(content).split(" ")
	if content[0][0] == "!" and content[0][1:].lower() == "инфа":
		sub_client.send_message(message="Привет! Меня зовут Наоми. Вот мои команды:", chatId=chatId)
	if content[0][0] == "?":
		sub_client.send_message(message=str(random.choice(lis)), chatId=chatId, replyTo=id)
	if content[0][0] == "!" and content[0][1:].lower() == "love":
		tex = re.split('[' + re.escape("@, ") + ']+', content)
		sub_client.send_message(message=(f"Вероятность любви между {tex[1]} и {tex[3]} равна {random.randint(0,100)}%"), chatId=chatId, replyTo=id)
	if content[0][0] == "!" and content[0][1:].lower() == "on":
		tim = -tim
	##if str(datetime.datetime.today())[11:13] == str(23) and tim == 1:
		##sub_client.send_message(message="Спокойной ночи, милашки.", chatId=chatId) ## Приветствие
	##if str(datetime.datetime.today())[11:13] == str("07") and tim == 1:
		##sub_client.send_message(message="Доброе утро, милашки.", chatId=chatId) # Приветствие

	##################################Защита чата##################################################
	if content[0][0] == "!":
		if content[0][1:].lower() == "save":
			nazvan = sub_client.get_chat_thread(chatId=data.message.chatId).title
			opisan = sub_client.get_chat_thread(chatId=data.message.chatId).content
			fonsss = sub_client.get_chat_thread(chatId=data.message.chatId).backgroundImage
			sub_client.send_message(message='Усё', chatId=data.message.chatId)
		if content[0][1:].lower() == "go":
			sub_client.edit_chat(chatId=data.message.chatId, title=str(nazvan), content=str(opisan))
			try:
				sub_client.edit_chat(chatId=data.message.chatId, backgroundImage=str(fonsss))
			except:
				sub_client.send_message(message='Восстановление прошло успешно!', chatId=data.message.chatId)
		if content[0][1:].lower() == "a" and sub_client.get_chat_thread(chatId).author.userId:
			sub_client.invite_to_chat(userId=str(client.get_from_code(str(content[1][:])).objectId), chatId=chatId)
			nom = 1

	if abs(int(vrem) - int(hm[0])) <= 2:
		if ban == 5 and av.count(nickname) > 2:
			hm[0] = vrem
			av.clear()
			ban = 0
			sub_client.send_message(message='Рейдер кикнут', chatId=data.message.chatId)
			sub_client.kick(userId=data.message.author.userId, chatId=data.message.chatId, allowRejoin = True)
		else:
			ban += 1
			hm[0] = vrem
			av.append(nickname)	
	else:
		hm[0] = vrem

	if data.message.content != None and data.message.type in [1, 50, 58, 57, 59, 100, 101, 102, 103, 104, 105, 106, 107, 109, 110, 113, 114, 115, 116, 124, 125, 126]:
		sub_client.send_message(message='Рейдеры пошлены нахуй!', chatId=data.message.chatId)
		sub_client.kick(userId=data.message.author.userId, chatId=data.message.chatId, allowRejoin = True)
	if data.message.content == None and nom == 1:
		sub_client.send_message(message='Добро пожаловать!', chatId=data.message.chatId)
		nom = 0

methods = []
for x in client.callbacks.chat_methods:
	methods.append(client.callbacks.event(client.callbacks.chat_methods[x].__name__)(on_message))