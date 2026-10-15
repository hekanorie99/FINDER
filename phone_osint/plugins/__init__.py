from .phonenumbers_plugin import PhoneNumbersPlugin
from .hibp import HIBPPlugin
from .numverify import NumverifyPlugin
from .dorking import DorkingPlugin

# Порядок = порядок выполнения
ALL_PLUGINS = [
    PhoneNumbersPlugin,
    HIBPPlugin,
    NumverifyPlugin,
    DorkingPlugin,
]
