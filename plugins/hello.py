from jetson.plugin import BloopyPlugin


class HelloPlugin(BloopyPlugin):
    name = "hello"

    def run(self) -> None:
        print("Hello from plugin!")
