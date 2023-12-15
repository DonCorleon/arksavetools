from arksavetools.config import *

class ArkSaveUtils:
    enable_debug_logging = False

    @staticmethod
    def debug_log(message, *args):
        if ArkSaveUtils.enable_debug_logging:
            logger.info(message, *args)
