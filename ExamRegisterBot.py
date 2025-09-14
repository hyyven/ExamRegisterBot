import requests
import re
from time import sleep
from bs4 import BeautifulSoup as bs
from sys import exit

timer = 5
#Insert your cookie!
cookie = ""


def RegisterToExam():
	"""
	This is a function which allow user to subscribe to exam.
	"""

	cookie_dict = {'_intra_42_session_production': cookie}
	try:
		req = requests.get("https://profile.intra.42.fr", cookies=cookie_dict)
	except Exception as e:
		print(f"[-] Check your connection! {e}")
		return
	soup = bs(req.content.decode('utf-8'), 'html.parser')
	exams = [str(x) for x in soup.find_all('div') if x.get('data-event-kind') == 'exam']

	#hmmm there should be an easy way to get the csrf_token
	#maybe just a regex to get the csrf-token is better....

	csrf_token = soup.find(attrs={'name':'csrf-token'})
	csrf_token = csrf_token['content']

	if not exams:
		print("No EXAM!")
		return
	for exam in exams:
		if '<span class>="event full"' in exam:
			continue
		else:
			if '<span class="event-registered">registered</span>' in exam:
				print("You are already registered to Exam!")
				exit()
			event_id = re.search('/exams/[0-9]*', exam)
			if event_id:
				post_url = "https://profile.intra.42.fr" + event_id[0] + "/exams_users"
				post_data = {'_method': 'post', 'authenticity_token': csrf_token}
				try:
					req_exam = requests.post(post_url, data=post_data, cookies=cookie_dict)
				except Exception as e:
					print("[-] Error:", str(e))
					exit(-1)
				print("[+] Exams user was successfully created.")
				exit()	
			else:
				print("[*] Contact the author of this program or modify and send a pull request")

	print("Every exams are full! Try this program later!")
	exit()

if __name__ == "__main__":
	while True:
		RegisterToExam()
		sleep(timer)
