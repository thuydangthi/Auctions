from auctions.models.category_relationship import CategoryRelationship
from auctions.models import Category, CategoryRelationship
from rest_framework import serializers
from .category_relationship import CategoryChildSerializer, CategoryParentSerializer
from rest_framework.validators import UniqueTogetherValidator


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer class of Category api
    """
    category_child = CategoryChildSerializer(many=True, required=False, validators=[
        UniqueTogetherValidator(queryset=CategoryRelationship.objects.all(), fields=['child'])])
    category_parent = CategoryParentSerializer(many=True, required=False)

    class Meta:
        model = Category
        fields = '__all__'

    def create(self, validated_data):
        children = validated_data.pop('category_child')
        parent = validated_data.pop('category_parent')
        category = Category.objects.create(**validated_data)
        for child in children:
            CategoryRelationship.objects.create(parent=category, **child)
        for par in parent:
            CategoryRelationship.objects.create(child=category, **par)
        return category

    def validate(self, data):
        parent = data.get('category_parent', None)

        if parent and len(parent) > 1:
            raise serializers.ValidationError({
                'category_parent': ['A category can only be a subcategory of another category.'],
            })
        return data
