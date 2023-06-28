import mysql.connector


def getConfig():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="123456",
        database="wechat_config",
        auth_plugin='mysql_native_password'
    )
    myCursor = mydb.cursor()
    myCursor.execute("SELECT * FROM developconfig")
    myConfig = myCursor.fetchall()
    configList = []
    for config in myConfig:
        # token 0
        configList.append(config[1])
        # appid 1
        configList.append(config[2])
        # appsecret 2
        configList.append(config[3])
        # encodekey 3
        configList.append(config[4])

    return configList
