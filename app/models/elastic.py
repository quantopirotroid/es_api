from easydict import EasyDict as edict
from app import es


class Data_validator():
    '''The class objects to find errors in json data.
       Arguments:
           data, type - dict'''
    def __init__(self):
        pass

    def common_check(self, data):
        if not data:
            return {'error': '400',
                    'reason': 'data is None'}
        if not isinstance(data, dict):
            return {'error': '400',
                    'reason': 'data must be a valid json'}
        if not data.get('index'):
            return {'error': '400',
                    'reason': 'index field is not set'}
        if not data.get('doc_type'):
            return {'error': '400',
                    'reason': 'doc_type field is not set'}

    def get_add_check(self, data):
        if not data.get('id'):
            return {'error': '400',
                    'reason': 'id field is not set'}

    def add_check(self, data):
        if not data.get('body'):
            return {'error': '400',
                    'reason': 'body field is not set'}

    def search_check(self, data):
        if not data.get('text'):
            return {'error': '400',
                    'reason': 'text field is not set'}


class ES_handler():
    def __init__(self):
        pass

    def add_data(self, check_error, data=None):
        common_error = check_error.common_check(data)
        if common_error:
            return common_error
        add_error = check_error.add_check(data)
        if add_error:
            return add_error
        error = check_error.get_add_check(data)
        if error:
            return error
        # exception expected?
        data = edict(data)
        # add try except
        resp = es.create(index=data.index,
                         doc_type=data.doc_type,
                         id=data.id,
                         body=data.body)
        return resp.get('created')

    def get_from_id(self, check_error, data=None):
        common_error = check_error.common_check(data)
        if common_error:
            return common_error
        error = check_error.get_add_check(data)
        if error:
            return error
        # exception expected?
        data = edict(data)
        # add try except
        resp = es.get(index=data.index,
                      doc_type=data.doc_type,
                      id=data.id)
        es_fields = ('_index', '_type', '_source', '_id')
        user_fields = ('index', 'doc_type', 'body', 'id')
        user_resp = {u: resp[e] for u, e in zip(user_fields, es_fields)}
        return user_resp

    def search(self, check_error, data=None):
        common_error = check_error.common_check(data)
        if common_error:
            return common_error
        error = check_error.search_check(data)
        if error:
            return error
        # exception expected?
        data = edict(data)
        body = {
            'query': {
                'query_string': {
                    'query': data.text
                }
            }
        }
        # add try except
        resp = es.search(index=data.index,
                         doc_type=data.doc_type,
                         body=body)
        es_fields = ('_index', '_type', '_source', '_id')
        user_fields = ('index', 'doc_type', 'body', 'id')
        hits = resp['hits']['hits']
        user_resp = {'hits': len(hits),
                     'found': [
                    {
                     u_field: doc[e_field]
                     for u_field, e_field in zip(user_fields, es_fields)
                    }
                     for doc in hits
            ]
        }
        return user_resp
