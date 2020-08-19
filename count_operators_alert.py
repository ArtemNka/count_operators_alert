# encoding: utf-8
import requests
import plyer
import schedule
import time
from pynput import keyboard


data = {
	"cookie": "grafana_session=1293ff884085e36d0d80f0220fc8b499",#Session cookie
	'url': 'https://grafana.cdek.ru/api/tsdb/query',
	'body': {
			  "from": "1597457059909",
			  "to": "1597460659909",
			  "queries": [
			    {
			      "refId": "A",
			      "intervalMs": 60000,
			      "maxDataPoints": 219,
			      "datasourceId": 38,
			      "rawSql": '''SELECT TOP 1 CountOperator FROM [dbo].[A_Cube_CC_CallQueue] WHERE IdTask = 'F7533346-603B-4976-A2A0-363086DB960B' AND DateTimeStart = (SELECT MAX(DateTimeStart) FROM [dbo].[A_Cube_CC_CallQueue] WHERE IdTask = 'F7533346-603B-4976-A2A0-363086DB960B')''',
			      "format": "table"
			    }
			  ]
			} ,
	'timer': 3600
}


def on_press(key):
	
	if key == keyboard.Key.f3:
	
		data['timer'] = 1
		run_code()
		return False 

def query(url, body, cookie):
	headers = {
		'Cookie': cookie
	}

	try: 

		result = requests.post(url, json=body, headers=headers, timeout=10)
		
		result = result.json()
		
		data["num_of_operators"] = result["results"]['A']['tables'][0]['rows'][0][0] 

		return data["num_of_operators"]

	except:
		return "Ошибка"

	
	
def run_code():
	print("Подключаемся")
	data["num_of_operators"] = query(data["url"], data["body"], data["cookie"])
	print(f"Количество операторов: {data['num_of_operators']}")
	if data["num_of_operators"] < 2:


		plyer.notification.notify ( message= str(data["num_of_operators"]),
    	title='Мало операторов', timeout=3600)

		# ...or, in a non-blocking fashion:
		listener = keyboard.Listener(
		    on_press=on_press)

		listener.start()
		data['timer'] = 3600
		while data['timer'] >= 0:
		    print (f"До активации осталось: {data['timer']}")
		    time.sleep(1)
		    data['timer'] = data['timer'] - 1

###############################
##### Запуск скрипта
###############################
run_code()
schedule.every(4).seconds.do(run_code)

while True:  

	schedule.run_pending() 

