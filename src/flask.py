from flask import Flask, request
import time
import random

app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def index():
	asd = random.randint(1,70)

	if request.method == 'GET':
		return 'Lo que no es puede llegar a ser... como te ven te tratan, y si te ven mal... ¡te maltratan! y si te ven bien te Con-tratan'
	if request.method == 'POST':
		time.sleep(50)
		return 'La gente vive con miedo. Miedo a la vida, miedo a quedarse sin trabajo, miedo a perder la salud, miedo a la muerte, y hay que vivir más libremente el minuto a minuto'

if __name__ == '__main__':
	app.run(host="0.0.0.0",port=8080)