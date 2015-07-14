# -*- coding: utf8 -*-
# This file is part of PyBossa.
#
# Copyright (C) 2013 SF Isle of Man Limited
#
# PyBossa is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyBossa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with PyBossa.  If not, see <http://www.gnu.org/licenses/>.

import datetime
import json
import uuid
import requests

from sqlalchemy import Text
from sqlalchemy.orm import relationship, backref, class_mapper
from sqlalchemy.ext.mutable import Mutable
from sqlalchemy.types import TypeDecorator
from sqlalchemy import event
from sqlalchemy.engine import reflection
from sqlalchemy.schema import (
    MetaData,
    Table,
    DropTable,
    ForeignKeyConstraint,
    DropConstraint,
    )

import logging
from time import time


try:
    import cPickle as pickle
except ImportError:  # pragma: no cover
    import pickle


from pybossa.core import sentinel

log = logging.getLogger(__name__)



class DomainObject(object):

    def dictize(self):
        out = {}
        for col in self.__table__.c:
            out[col.name] = getattr(self, col.name)
        return out

    @classmethod
    def undictize(cls, dict_):
        raise NotImplementedError()

    def __str__(self):  # pragma: no cover
        return self.__unicode__().encode('utf8')

    def __unicode__(self): # pragma: no cover
        repr = u'<%s' % self.__class__.__name__
        table = class_mapper(self.__class__).mapped_table
        for col in table.c:
            try:
                repr += u' %s=%s' % (col.name, getattr(self, col.name))
            except Exception, inst:
                repr += u' %s=%s' % (col.name, inst)

        repr += '>'
        return repr


class JSONType(Mutable, TypeDecorator):
    '''Additional Database Type for handling JSON values.
    '''
    impl = Text

    def __init__(self):
        super(JSONType, self).__init__()

    def process_bind_param(self, value, dialect):
        return json.dumps(value)

    def process_result_value(self, value, dialiect):
        return json.loads(value)

    def copy_value(self, value):
        return json.loads(json.dumps(value))


class JSONEncodedDict(TypeDecorator):
    "Represents a dict structure as a json-encoded string."

    impl = Text

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value

    def copy_value(self, value):
        return json.loads(json.dumps(value))


class MutableDict(Mutable, dict):
    @classmethod
    def coerce(cls, key, value):
        "Convert plain dictionaries to MutableDict."

        if not isinstance(value, MutableDict):
            if isinstance(value, dict):
                return MutableDict(value)

            # this call will raise ValueError
            return Mutable.coerce(key, value)
        else:
            return value

    def __setitem__(self, key, value):
        "Detect dictionary set events and emit change events."

        dict.__setitem__(self, key, value)
        self.changed()

    def __delitem__(self, key):
        "Detect dictionary del events and emit change events."

        dict.__delitem__(self, key)
        self.changed()

    def __getstate__(self):
        d = self.__dict__.copy()
        return dict(self)

    def __setstate__(self, state):
        self.update(state)

MutableDict.associate_with(JSONEncodedDict)

def make_timestamp():
    now = datetime.datetime.utcnow()
    return now.isoformat()


def make_uuid():
    return str(uuid.uuid4())


def update_redis(obj):
    """Add domain object to update feed in Redis."""
    p = sentinel.master.pipeline()
    tmp = pickle.dumps(obj)
    p.zadd('pybossa_feed', time(), tmp)
    p.execute()


def update_project_timestamp(mapper, conn, target):
    """Update method to be used by the relationship objects."""
    sql_query = ("update project set updated='%s' where id=%s" %
                 (make_timestamp(), target.project_id))
    conn.execute(sql_query)


def webhook(url, payload=None):
    """Post to a webhook."""
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    if url:
        return requests.post(url, data=json.dumps(payload), headers=headers)
    else:
        return False
