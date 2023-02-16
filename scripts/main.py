from picamera2 import Picamera2
import io
import zenoh
import argparse


class CameraNode:
    cam = Picamera2
    capture_config = dict

    def __init__(self) -> None:
        self.cam = Picamera2()
        capture_config = self.cam.create_preview_configuration(
            main={"size": (1280, 720)})
        self.cam.configure(capture_config)
        self.cam.set_controls({"AfMode": 2})
        self.session = zenoh.open()

    def run(self, key):
        self.cam.start()
        print("Starting publisher on key:", key)
        pub = self.session.declare_publisher(key)

        while True:
            data = io.BytesIO()
            self.cam.capture_file(data, format='jpeg')
            pub.put(data.getbuffer().tobytes())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Camera Node', description='Stream camera over zenoh')
    parser.add_argument('--key', '-k', dest='key', default='camera_node',
                        type=str, help='Key expression to write to.')
    args = parser.parse_args()

    node = CameraNode()

    node.run(args.key)
