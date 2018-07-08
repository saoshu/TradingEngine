import logging

class OMSLogger(object):
	# def __new__(cls, *args, **kw):
	# 	if _instance is None:
	# 		_instance = super(OMSLogger, cls).__new__(cls, *args, **kw)
	# 	return _instance
			
	@staticmethod
	def init_log_system(log_level=logging.DEBUG):
		FORMAT = "%(asctime)-15s %(message)s"
		logging.basicConfig(level=log_level, format=FORMAT)

	@staticmethod
	def debug(message):		
		logging.debug(message)

	@staticmethod
	def info(message):
		logging.info(message)

	@staticmethod
	def warning(message):
		logging.warning(message)

	@staticmethod
	def error(message):
		logging.error(message)

if __name__ == "__main__":
	OMSLogger.init_log_system()
	OMSLogger.debug("test log")
	# OMSLogger.instance.log_debug("test log 2")
	# OMSLogger.instance.log_info("test info")
	