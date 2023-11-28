class Error(Exception):
    """Base class for other exceptions"""

    pass


class NoStrategyProvidedError(Error):
    pass


class UnknownStrategyError(Error):
    pass


class NoModeProvidedError(Error):
    pass


class NoMaxLossProvidedError(Error):
    pass


class NoPositionValueProvidedError(Error):
    pass


class InvalidConfigValueError(Error):
    pass
