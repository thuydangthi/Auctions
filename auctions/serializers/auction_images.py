from auctions.models import AuctionsImages
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


class AuctionsImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = AuctionsImages
        fields = ['image', 'id']
        extra_kwargs = {'id': {'read_only': True}}


class AuctionsImagesFullInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = AuctionsImages
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(queryset=AuctionsImages.objects.all(), fields=['auction', 'image'])]
