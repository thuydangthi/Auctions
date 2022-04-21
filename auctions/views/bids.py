from auctions.models import Bids, Auctions
from rest_framework.response import Response
from rest_framework import status, generics
from auctions.serializers import *
from django_filters.rest_framework import DjangoFilterBackend


class BidsList(generics.ListCreateAPIView):
    queryset = Bids.objects.all()
    serializer_class = BidsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'auction': ['exact'],
        'auctioneer': ['exact']
    }

    def create(self, request, *args, **kwargs):
        serializer = BidsSerializer(data=request.data)
        if serializer.is_valid():
            if Auctions.objects.get(pk=request.data['auction']).seller == request.user:
                return Response({"detail": "You can't bit for your auction!"}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(auctioneer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BidsDetail(generics.RetrieveAPIView):
    queryset = Bids.objects.all()
    serializer_class = BidsSerializer
