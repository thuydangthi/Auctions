import datetime
from auctions.models import Watchlist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from auctions.serializers import WatchlistSerializer
from auctions.permissions import IsOwnerOrReadOnly
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend


class WatchListList(generics.ListCreateAPIView):
    queryset = Watchlist.objects.filter(deleted_date__isnull=True)
    serializer_class = WatchlistSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {'auction': ['exact'], 'follower': [
        'exact'], 'created_date': ['date']}

    def create(self, request, *args, **kwargs):
        serializer = WatchlistSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(follower=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WatchListDetails(APIView):
    """
    Retrieve and delete a WatchList instance.
    """
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self, pk):
        data = get_object_or_404(Watchlist, id=pk, deleted_date__isnull=True)
        self.check_object_permissions(self.request, data)
        return data

    def get(self, request, pk, format=None):
        query_data = self.get_object(pk)
        serializer = WatchlistSerializer(query_data)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        query_data = self.get_object(pk)
        query_data.deleted_date = datetime.datetime.now()
        query_data.save()
        return Response({"detail": "Unfollow successful auction!"}, status=status.HTTP_204_NO_CONTENT)
