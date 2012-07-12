# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ModelLog'
        db.create_table('models_log_modellog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('changed_pk', self.gf('django.db.models.fields.IntegerField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('models_log', ['ModelLog'])


    def backwards(self, orm):
        # Deleting model 'ModelLog'
        db.delete_table('models_log_modellog')


    models = {
        'models_log.modellog': {
            'Meta': {'object_name': 'ModelLog'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'changed_pk': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['models_log']