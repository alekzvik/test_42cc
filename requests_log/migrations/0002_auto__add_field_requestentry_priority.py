# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'RequestEntry.priority'
        db.add_column('requests_log_requestentry', 'priority',
                      self.gf('django.db.models.fields.SmallIntegerField')(default=1),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'RequestEntry.priority'
        db.delete_column('requests_log_requestentry', 'priority')


    models = {
        'requests_log.requestentry': {
            'Meta': {'ordering': "['-priority', 'timestamp']", 'object_name': 'RequestEntry'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'path': ('django.db.models.fields.TextField', [], {}),
            'priority': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'query': ('django.db.models.fields.TextField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['requests_log']