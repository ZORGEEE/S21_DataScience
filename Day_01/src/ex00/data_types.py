def data_types():
    var_int = 1
    var_str = "q"
    var_float = 1.5
    var_bool = True
    var_list = [1, 2, 3]
    var_dict = {"key": "word"}
    var_tuple = (1, 2, 3)
    var_set = {1, 2, 3}

    types = [
        type(var_int).__name__,
        type(var_str).__name__,
        type(var_float).__name__,
        type(var_bool).__name__,
        type(var_list).__name__,
        type(var_dict).__name__,
        type(var_tuple).__name__,
        type(var_set).__name__
        ]

    print(str(types).replace("'", ""))

if __name__ == '__main__':
    data_types()