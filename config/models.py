# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 SNMP, Inc.

from mongoengine import Document
from mongoengine import EmbeddedDocument

from mongoengine import BooleanField
from mongoengine import EmbeddedDocumentField
from mongoengine import IntField
from mongoengine import ListField
from mongoengine import StringField


class Application(EmbeddedDocument):
    title = StringField(required=True)
    module = StringField(required=True)
    version = StringField(required=True)
    revision = IntField(required=True)
    stage = StringField(required=True)
    use_api_key = StringField(required=True)


class Logger(EmbeddedDocument):
    level = StringField(required=True)
    path = StringField(required=True)
    filename = StringField(required=True)


class ElasticSearchLogger(EmbeddedDocument):
    standard = EmbeddedDocumentField(Logger, required=True)
    trace = EmbeddedDocumentField(Logger, required=True)


class Logging(EmbeddedDocument):
    access = EmbeddedDocumentField(Logger, required=True)
    application = EmbeddedDocumentField(Logger, required=True)
    general = EmbeddedDocumentField(Logger, required=True)
    mysql = EmbeddedDocumentField(Logger, required=True)


class HostName(EmbeddedDocument):
    host = StringField(required=True)


class SSL(EmbeddedDocument):
    cert_filename = StringField()
    key_filename = StringField()


class HTTPServer(EmbeddedDocument):
    hosts = ListField(EmbeddedDocumentField(HostName), required=True)
    base_port = IntField(required=True)
    arns = ListField(EmbeddedDocumentField(HostName), required=True)
    ssl = EmbeddedDocumentField(SSL, required=True)


class MySQL(EmbeddedDocument):
    host = StringField(required=True)
    port = IntField(required=True)
    db_name = StringField(required=True)
    user = StringField(required=True)
    password = StringField(required=True)


class ElasticSearch(EmbeddedDocument):
    host = StringField(required=True)
    port = IntField(required=True)
    index = StringField(required=True)


class Database(EmbeddedDocument):
    mysql = EmbeddedDocumentField(MySQL, required=True)
    elasticsearch = EmbeddedDocumentField(ElasticSearch, required=True)


class Signature(EmbeddedDocument):
    get = StringField()
    post = StringField()
    put = StringField()
    delete = StringField()


class APIKey(EmbeddedDocument):
    secret = StringField(required=True)
    app = EmbeddedDocumentField(Signature, required=True)
    user = EmbeddedDocumentField(Signature, required=True)
    key = EmbeddedDocumentField(Signature, required=True)
    push = StringField()


class SQS(EmbeddedDocument):
    access_key = StringField(required=True)
    secret_key = StringField(required=True)
    region = StringField(required=True)
    path = StringField(required=True)
    name = StringField(required=True)
    arn = StringField(required=True)


class KeywordDB(EmbeddedDocument):
    user = StringField(required=True)
    password = StringField(required=True)
    workbook = StringField(required=True)


class AppConfig(Document):
    application = EmbeddedDocumentField(Application, required=True)
    debug = BooleanField(required=True)
    logging = EmbeddedDocumentField(Logging, required=True)
    server = EmbeddedDocumentField(HTTPServer, required=True)
    database = EmbeddedDocumentField(Database, required=True)
    apikey = EmbeddedDocumentField(APIKey, required=True)
    queue = EmbeddedDocumentField(SQS, required=True)
#    keyword_db = EmbeddedDocumentField(KeywordDB, required=True)
