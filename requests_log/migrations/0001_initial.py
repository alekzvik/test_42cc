# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RequestEntry'
        db.create_table('requests_log_requestentry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('path', self.gf('django.db.models.fields.TextField')()),
            ('method', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('query', self.gf('django.db.models.fields.TextField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('requests_log', ['RequestEntry'])


    def backwards(self, orm):
        # Deleting model 'RequestEntry'
        db.delete_table('requests_log_requestentry')


    models = {
        'requests_log.requestentry': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'RequestEntry'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'path': ('django.db.models.fields.TextField', [], {}),
            'query': ('django.db.models.fields.TextField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['requests_log']