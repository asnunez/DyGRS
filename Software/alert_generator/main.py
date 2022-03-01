from threading import Thread


def process_video(id_camera) -> None:
    pass


def main() -> None:
    camaras = [
        "rstp://camera1/dfdsf.mp4",
        "rstp://camera2/dfdsf.mp4",
        "rstp://camera3/dfdsf.mp4",
        "rstp://camera4/dfdsf.mp4",
        "rstp://camera5/dfdsf.mp4"
    ]

    threads = [Thread(target=process_video, args=(c,)) for c in camaras]

    [t.start() for t in threads]

    [t.join() for t in threads]


if __name__ == '__main__':
    main()
