class Logger:

    logging = False

    @staticmethod
    def __log__(s):
        if Logger.logging:
            print(s)