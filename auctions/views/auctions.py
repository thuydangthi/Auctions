from auctions.models import Auctions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from auctions.serializers import *
from auctions.permissions import IsOwnerOrReadOnly
import datetime
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend


class AuctionsList(generics.ListCreateAPIView):
    """
    List all auction, or create a new auction.
    """
    queryset = Auctions.objects.filter(deleted_at__isnull=True)
    serializer_class = AuctionOverviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {'seller': ['exact'],
                        'is_active': ['exact'],
                        'start_time': ['date', 'lte', 'gte', 'lt', 'gt'],
                        'end_time': ['date', 'lte', 'gte', 'lt', 'gt'],
                        'categories': ['exact']}

    def create(self, request, *args, **kwargs):
        serializer = AuctionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(seller=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuctionsDetail(APIView):
    """
    Retrieve, update or delete a auction instance.
    """
    serializer_class = AuctionSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Auctions.objects.filter(deleted_at__isnull=True)

    def get_object(self, pk):
        data = get_object_or_404(Auctions, id=pk)
        self.check_object_permissions(self.request, data)
        return data

    def get(self, request, pk, format=None):
        auction = self.get_object(pk)
        serializer = AuctionSerializer(auction)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        auction = self.get_object(pk)
        serializer = AuctionSerializer(
            auction, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        auction = get_object_or_404(Auctions, id=pk)
        auction.deleted_at = datetime.datetime.now()
        auction.save()
        return Response({"detail": "Delete auction successfully!"}, status=status.HTTP_204_NO_CONTENT)
