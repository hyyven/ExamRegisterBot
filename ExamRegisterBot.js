const request = require('request');
const cheerio = require('cheerio');
const querystring = require('querystring');

const timer = 5000;
//Insert your cookie here!
const cookie = '';


if (cookie === '')
{
	console.error("Please Insert your cookie!");
	process.exit();
}

function check_exam()
{
	request.get({
	url :"https://profile.intra.42.fr", 
	headers: {
		'Cookie' : cookie, 
	}},
	(err, res, body) => {
		if (err)
		{
			console.error("[-] Check your connection!");
			return ;
		}
		console.log("[+] Connected to the site!");

		let $ = cheerio.load(body);
		let exam_event = $('div[data-event-kind="exam"]').html();
		if (exam_event == null)
		{
			console.log("No EXAM!");
			return ;
		}
		let registered = exam_event.search('<span class="event-registered">registered</span>');
		if (registered !== -1)
		{
			console.log("You are already registered to Exam!");
			process.exit();
		}
		let meta_csrf = $('meta[name="csrf-token"]').attr('content');
		let event_id = exam_event.match(/exams\/[0-9]*/);
		var postData = querystring.stringify({
			_method: 'post',
			authenticity_token: meta_csrf
		})
		request.post({
				url: "https://profile.intra.42.fr/" + event_id[0] + "/exams_users", 
				form : postData,
	 			headers:
				{
					'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0,9,image/webp,image/apng,*/*;q=0.8',
					'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
					'Cache-Control': 'max-age=0',
					'Connection': 'keep-alive',
					'Content-Length': postData.length,
					'Content-Type': 'application/x-www-from-urlencoded',
					'Cookie' : cookie,
					'Host'   : 'profile.intra.42.fr',
					'Origin' : 'https://profile.intra.42.fr',
					'Referer': 'https://profile.intra.42.fr/',
					'Upgrade-Insecure-Requests' : '1',
					'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36',
				}}, (err, res, body) => {
					if (err)
					{
						console.error("[-] Error:", err);
						return ;
					}
					console.log("[+] Exams user was successfully created.");
					process.exit();
				})
	})
}

setInterval(check_exam, timer);
