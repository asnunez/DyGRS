from src import create_app

if __name__ == '__main__':
    server = create_app()
    server.run("0.0.0.0", 8080, debug=True)
