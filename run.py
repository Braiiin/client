# the main Flask application
from client import create_app

app = create_app()

if __name__ == "__main__":
	app.run(**app.config['INIT'])