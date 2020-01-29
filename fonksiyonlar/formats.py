def eightdecimalstring(value):
    if isinstance(value,float):
        return "{0:.8f}".format(value)
    elif isinstance(value,str):
        return value
    else:
        print("Type error. Type is : {}".format(type(value)))
        return -1