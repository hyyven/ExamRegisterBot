import requests
import re
from time import sleep
from bs4 import BeautifulSoup as bs
from sys import exit

timer = 60
#Insert your cookie!
cookie = ""

def skip_specific_exam(exams):
	for exam in exams:
		if 'class="date-day">15' and 'class="date-month">September' in exam:
			exams.remove(exam)
			# print("Skipping September 15 exam")

def RegisterToExam():
	cookie_dict = {'_intra_42_session_production': cookie}
	try:
		req = requests.get("https://profile.intra.42.fr", cookies=cookie_dict)
		req.raise_for_status()
	except Exception as e:
		print(f"[-] check your connection {e}")
		return
	soup = bs(req.content.decode('utf-8'), 'html.parser')
	exams = [str(x) for x in soup.find_all('div') if x.get('data-event-kind') == 'exam']

	#hmmm there should be an easy way to get the csrf_token
	#maybe just a regex to get the csrf-token is better....

	csrf_token = soup.find(attrs={'name':'csrf-token'})
	if not csrf_token:
		print("[-] cookie is probably invalid")
		exit(1)
	csrf_token = csrf_token['content']

	# skip_specific_exam(exams)

	if not exams:
		# print("[*] no exam")
		return
	for exam in exams:
		# print(f"[*] checking exam: {exam}")
		# continue
		if '<span class>="event full"' in exam:
			continue
		else:
			if '<span class="event-registered">registered</span>' in exam:
				print("[+] already registered to an exam")
				exit(0)
			event_id = re.search('/exams/[0-9]*', exam)
			if event_id:
				post_url = "https://profile.intra.42.fr" + event_id[0] + "/exams_users"
				post_data = {'_method': 'post', 'authenticity_token': csrf_token}
				try:
					req_exam = requests.post(post_url, data=post_data, cookies=cookie_dict)
				except Exception as e:
					print("[-] error:", str(e))
					exit(1)
				print("[+] successfully registered to an exam")
				exit(0)
			else:
				print("[*] contact the author of this program or modify and send a pull request")
	print("every exams are full")

if __name__ == "__main__":
	try:
		while True:
			RegisterToExam()
			sleep(timer)
	except KeyboardInterrupt:
		print("[-] exiting...")
		exit(0)
