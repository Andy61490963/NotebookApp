from rest_framework import serializers
from .models import Notebook, Note

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'is_trashed']

class NotebookSerializer(serializers.ModelSerializer):
    notes = serializers.SerializerMethodField()

    class Meta:
        model = Notebook
        fields = ['id', 'name', 'notes']

    def get_notes(self, obj):
        notes_not_trashed = obj.notes.filter(is_trashed=False)
        serializer = NoteSerializer(notes_not_trashed, many=True)
        return serializer.data
