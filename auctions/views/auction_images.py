from auctions.models import AuctionsImages
from rest_framework import status, generics
from auctions.serializers import AuctionsImagesFullInfoSerializer
from auctions.permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend


class AuctionImageList(generics.ListCreateAPIView):
    queryset = AuctionsImages.objects.all()
    serializer_class = AuctionsImagesFullInfoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['auction', 'auction__seller']


class AuctionImageDetail(generics.RetrieveDestroyAPIView):
    queryset = AuctionsImages.objects.all()
    serializer_class = AuctionsImagesFullInfoSerializer
    permission_classes = [IsOwnerOrReadOnly]
