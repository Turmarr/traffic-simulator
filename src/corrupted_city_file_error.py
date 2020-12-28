class CorruptedCityFileError(Exception):

    def __init__(self, message):
        super(CorruptedCityFileError, self).__init__(message)