import datetime
import json
from client.exceptions import LogicException, ClientException
from flask import current_app
from client import logger
import requests


class Logic:
    """Handles communication with logic tier and auth"""

    access_token = None
    response = None
    version = 'v1'

    def __init__(self, logic=None):
        self.logic = logic

    def call(self, method, obj, data, func=None):
        """Assemble URI and make request"""
        uri = '{logic}/api/{v}/{obj}'.format(
            logic=self.logic or current_app.config['LOGIC_URI'],
            v=self.version,
            obj=obj.__class__.__name__.lower())
        if hasattr(obj, 'id'):
            uri += '/%s' % obj.id
        if func:
            uri += '/%s' % func
        return self.request(method, uri, data, self.access_token)

    def request(self, method, uri, data, access_token=None):
        """Makes request with specified method, data, and optional access token"""
        data = data or {}
        if access_token:
            data['access_token'] = access_token
        self.response = getattr(requests, method)(uri, params=data)
        json = self.response.json()
        logger.info(self.response.url)
        logger.debug(json)
        if json['status'] != 200:
            raise LogicException('%s\n- - "%s %s" %d -' % (
                json['message'], method.upper(), self.response.url, json['status']))
        return json['data']

    # TODO: do we need these? call() is invoked directly
    def post(self, obj, **data):
        """Post request"""
        return self.call('post', obj, data)

    def get(self, obj, **data):
        """Get request"""
        return self.call('get', obj, data)

    def put(self, obj, **data):
        """Put request"""
        return self.call('put', obj, data)

    def delete(self, obj, **data):
        """Delete request"""
        return self.call('delete', obj, data)


logic = Logic()


class Entity:
    """Universal entity, abstracts communication with logic tier"""

    _response = None
    _response_data = None

    def __init__(self, **kwargs):
        self.load(**kwargs)

    # API functionality

    @property
    def _data(self):
        """Compiles data for this object"""
        return {
            k: v for k, v in vars(self).items()
            if not k.startswith('_') and not callable(v)}

    # TODO: clean this up
    def call(self, method, data=None, **kwargs):
        """calls the logic tier"""
        response = logic.call(method, self, data or self._data, **kwargs)
        to_date = datetime.datetime.fromtimestamp
        _values = {
            '$oid': lambda v: v['$oid'],
            # '$date': lambda v: to_date(v['$date']),  #TODO: fix to_date
            '$date': lambda v: v['$date']
        }
        _keys, identity = {'_id': 'id'}, lambda x: x
        _get_key = lambda v: list(v.keys())[0]
        _process = lambda v: _values.get(_get_key(v), identity)(v) \
            if isinstance(v, dict) else v
        _process_dict = lambda response: {
            _keys.get(k, k): _process(v) for k, v in response.items()}
        if isinstance(response, list):
            data = []
            for item in response:
                item = _process_dict(item) if isinstance(item, dict) else item
                data.append(item)
        elif isinstance(response, dict):
            data = _process_dict(response)
            self.load(**data)
        else:
            data = response
        self._response = response
        self._response_data = data
        logger.info(data)
        return data

    def post(self):
        """Create object"""
        self.call('post')
        return self

    def get(self):
        """Get object"""
        self.call('get')
        return self

    def fetch(self):
        """Fetch all objects that match the query"""
        return self.call('get', func='fetch')

    def put(self):
        """Saves the object"""
        self.call('put')
        return self

    def save(self):
        """Alias for put"""
        return self.put()

    def delete(self):
        """Delete the object"""
        return self.call('delete')

    def get_or_create(self):
        """Get or create an object"""
        self.call('get', func='get_or_create')
        return self

    # Utilities

    def load(self, force=False, **kwargs):
        """Loads all kwargs into object as attributes"""
        for k, v in kwargs.items():
            attr = getattr(self, k, None)
            if callable(attr) and not force:
                raise ClientException(
                    'Cannot override method "%s", use force=True' % k)
            setattr(self, k, v)
        return self

    def to_json(self):
        """Return jsonified object"""
        return json.dumps(self._data)
