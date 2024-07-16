from rest_framework import serializers

from link_generator.models import Link


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = '__all__'
