from db_logic import DatabaseProcessor


def close_database():
    DatabaseProcessor().db.close()


def parse_command_with_kwargs(args):
    kwargs = {}
    for i in range(0, len(args) - 1, 2):
        key = args[i][2:]
        value = args[i + 1]

        try:
            value = eval(value)

        except (NameError, SyntaxError):
            pass

        kwargs[key] = value

    return kwargs


def to_column_string(iter_object):
    return '\n'.join(list(map(lambda x: x.name, iter_object)))

