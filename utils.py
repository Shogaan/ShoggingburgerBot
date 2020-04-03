from db_logic import DatabaseProcessor

def close_database():
    DatabaseProcessor().db.close()

def to_column_string(iter_object):
    return '\n'.join(list(map(lambda x: x.name, iter_object)))

