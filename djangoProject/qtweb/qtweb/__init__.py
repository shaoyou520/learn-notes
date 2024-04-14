import pymysql
import logging
logging.getLogger().setLevel(logging.INFO)

pymysql.version_info = (1, 4, 13, "final", 0)
pymysql.install_as_MySQLdb()