import Bot


class App:
    def __init__(self):
        pass

    def __call__(self, debug=False):
        bot = Bot
        bot.start_routing()
