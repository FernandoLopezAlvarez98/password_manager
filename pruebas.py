import datetime


ahora = datetime.datetime.now()
id = str(ahora.month)+str(ahora.day)+str(ahora.second)+str(ahora.microsecond)
print(id)