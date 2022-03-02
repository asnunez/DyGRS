import Software.services_provider


def main() -> None:
    services_provider = Software.services_provider.create_app()

    services_provider.run("localhost", 80, debug=True)


if __name__ == '__main__':
    main()
