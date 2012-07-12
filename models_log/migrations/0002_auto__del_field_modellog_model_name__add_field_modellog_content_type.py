# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'ModelLog.model_name'
        db.delete_column('models_log_modellog', 'model_name')

        # Adding field 'ModelLog.content_type'
        db.add_column('models_log_modellog', 'content_type',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['contenttypes.ContentType']),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'ModelLog.model_name'
        raise RuntimeError("Cannot reverse this migration. 'ModelLog.model_name' and its values cannot be restored.")
        # Deleting field 'ModelLog.content_type'
        db.delete_column('models_log_modellog', 'content_type_id')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'models_log.modellog': {
            'Meta': {'object_name': 'ModelLog'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'changed_pk': ('django.db.models.fields.IntegerField', [], {}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['models_log']