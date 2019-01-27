from Classes.color import Color


class Output:
    MSG_ERROR = 'error'
    MSG_OK = 'ok'

    @staticmethod
    def print(msg_type, value):
        if msg_type == Output.MSG_ERROR:
            color = Color.FAIL
            status = Output.MSG_ERROR
        else:
            color = Color.OKGREEN
            status = Output.MSG_ERROR

        print(
            color + '[' + status.upper() + ']' + Color.ENDC
            + ' ' + value
        )
