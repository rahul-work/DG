import sys
import subprocess
import webbrowser


ENV = 'PROD' # 'DEV' or 'TEST' or 'PROD'


if ENV == 'DEV':
	frontend_url = 'http://localhost:3000'
elif ENV == 'PROD':
	frontend_url = 'http://localhost:8000/static/index.html'


if __name__ == '__main__':
	server = subprocess.Popen(['uvicorn', 'main:app', '--reload'])
	try:
		webbrowser.open(frontend_url)
	except KeyboardInterrupt:
		server.kill()
	sys.exit()