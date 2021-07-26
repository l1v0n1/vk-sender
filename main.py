import tkinter as tk
from tkinter import messagebox
import requests
import json
import time

class LoginApp(tk.Tk):
	def __init__(self):
		super().__init__()
		self.geometry('400x115')

		self.token = tk.Entry(self)
		self.text = tk.Entry(self)

		self.token.insert(tk.END, 'Токен')
		self.text.insert(tk.END, 'Текст для рассылки')

		self.token_btn = tk.Button(self, text="Рассылка", command=self.sender)
		self.clear_btn = tk.Button(self, text="Очистить", command=self.clear_form)
		self.stop_btn = tk.Button(self, text='Выйти', command=self.stop)

		self.token.pack()
		self.text.pack()
		self.token_btn.pack(fill=tk.BOTH)
		self.clear_btn.pack(fill=tk.BOTH)
		self.stop_btn.pack(fill=tk.BOTH)

	def sender(self):
		if self.token.get() == '':
			messagebox.showerror('Ошибка', 'Вы не ввели токен!\nВставьте в первое поле ввода токен от группы ВК с которой будет идти рассылка.')
		elif self.text.get() == '':
			messagebox.showerror('Ошибка', 'Вы не ввели текст для рассылки\nВставьте во второе поле ввода текст, который будет отправляться.')
		elif 'Токен' in self.token.get():
			messagebox.showerror('Ошибка', 'Удалите слово токен из первого поля и вставьте токен от группы ВК')
		else:
			start = time.time()
			try:
				r = requests.get(f'https://api.vk.com/method/messages.getConversations?access_token={self.token.get()}&v=5.130&count=200')
				conversations = r.json()
				rng = conversations['response']['count']

				for i in range(rng):
					if conversations['response']['items'][i]['conversation']['peer']['type'] == 'user' and conversations['response']['items'][i]['conversation']['can_write']['allowed']:
						peerid = conversations['response']['items'][i]['conversation']['peer']['id']
						req = requests.post('https://api.vk.com/method/messages.send', data={'access_token': self.token.get(), 'peer_id': int(peerid), 'random_id': 0, 'message': self.text.get(), 'v':"5.130"}).json()

				messagebox.showinfo('Удачно!', 'Рассылка завершена за {} сек'.format(round(time.time() - start, 1)))
			except Exception as error:
				messagebox.showerror('Ошибка', 'Возникла ошибка, возможно вы неверно ввели токен...\nОшибка: {}'.format(error))

	def clear_form(self):
		self.token.delete(0, tk.END)
		self.text.delete(0, tk.END)
		self.token.focus_set()

	def stop(self):
	    self.destroy()

if __name__ == "__main__":
	app = LoginApp()
	app.title('Рассылка Вконтакте')
	app.mainloop()
