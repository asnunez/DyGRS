from sw.http_server import app

if __name__ == '__main__':

    server = app.create_app()

    server.run("localhost", 5000, debug=True)