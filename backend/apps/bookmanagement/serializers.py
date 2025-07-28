from rest_framework import serializers

from apps.bookmanagement.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"
