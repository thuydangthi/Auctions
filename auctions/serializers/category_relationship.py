from auctions.models import CategoryRelationship
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


class CategoryRelationshipSerializer(serializers.ModelSerializer):
    """
    Serializer class of Category relationship api
    """

    class Meta:
        model = CategoryRelationship
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(queryset=CategoryRelationship.objects.all(), fields=['child', 'parent'])]

    def validate(self, data):
        child = data.get('child', None)
        parent = data.get('parent', None)
        if child and parent and CategoryRelationship.objects.filter(
                child=parent, parent=child).exists():
            raise serializers.ValidationError({
                'parent': ['The fields child, parent must make a unique set.'],
            })

        return data


class CategoryParentSerializer(serializers.ModelSerializer):
    """
    Serializer class of Category relationship api
    """

    class Meta:
        model = CategoryRelationship
        fields = ['parent']


class CategoryChildSerializer(serializers.ModelSerializer):
    """
    Serializer class of Category relationship api
    """

    class Meta:
        model = CategoryRelationship
        fields = ['child']
