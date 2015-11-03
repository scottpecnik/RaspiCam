class FakeCamera(object):

    def __init__(self):
        self.test = 'txt'
        pass

    def capture(self, output, fileformat=None):
        self._open_output(output)
        self._close_output(output)
        print(fileformat)

    def _open_output(self, output):
        # opened = isinstance(output, (bytes, str))
        pass
        # if opened:
        #     # Open files in binary mode with a decent buffer size
        #     output = io.open(output, 'wb', buffering=65536)
        #     output.write('test')

    def _close_output(self, output):
        output.close()

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def close(self):
        pass