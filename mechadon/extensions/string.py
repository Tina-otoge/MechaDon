def listify(l, marker='• ', seperator='\n'):
    return seperator.join([marker + str(x) for x in l])
