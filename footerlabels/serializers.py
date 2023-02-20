from rest_framework import serializers
from footerlabels.models import Footerlabels


class FooterlabelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Footerlabels
        fields = ['id', 'label', 'link']









# Older way to do it
# class FooterlabelsSerializer(serializers.Serializer):
    # id = serializers.IntegerField(read_only=True)
    # label = serializers.CharField(required=True, allow_blank=False, max_length=100)
    # link = serializers.CharField(required=True, allow_blank=False, max_length=100)
    #
    # def create(self, validated_data):
    #     """
    #     Create and return a new `Footerlabels` instance, given the validated data.
    #     """
    #     return Footerlabels.objects.create(**validated_data)
    #
    # def update(self, instance, validated_data):
    #     """
    #     Update and return an existing `Footerlabels` instance, given the validated data.
    #     """
    #     instance.label = validated_data.get('label', instance.label)
    #     instance.link = validated_data.get('label', instance.label)


