def is_integer(value):
    """ This little function is intended to be used in the
        OrderItemListView class to check if the order query
        parameter is an integer.
    """
    try:
        int(value)
        return True
    except ValueError:
        return False