import logging
logging.basicConfig(level=logging.INFO, filename='Test.log', filemode='w', format='%(asctime)s %(name)s - %(levelname)s - %(message)s')

var1 = 5

logging.info("LogTest")
logging.info("Var1 value: %s", str(var1))