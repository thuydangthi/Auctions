from django.urls import path
from . import views


urlpatterns = [
    # user: gel all, create, delete, update, get one
    path('users/', views.UserRegisterList.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),

    # auctions: get all, create, delete, update, get one, filter
    path('auctions/', views.AuctionsList.as_view(), name='auctions-list'),
    path('auctions/<int:pk>/', views.AuctionsDetail.as_view(),
         name='auction-detail'),

    # bid: get all, get all filter by auction, get all
    path('bids/', views.BidsList.as_view(), name='bids-list'),
    path('bids/<int:pk>/', views.BidsDetail.as_view(), name='bid-detail'),

    # watch list: get all, get all filter by auction, get all
    path('watch-list/', views.WatchListList.as_view(), name='watch-list'),
    path('watch-list/<int:pk>/',
         views.WatchListDetails.as_view(), name='watch-detail'),

    # category list: get all, get all filter by auction, get all
    path('category-list/', views.CategoryList.as_view(), name='category-list'),
    path('category-list/<int:pk>/',
         views.CategoryDetail.as_view(), name='category-detail'),

    # category relationship list: get all, get all filter by auction, get all
    path('category-relationship-list/',
         views.CategoryRelationshipList.as_view(), name='category-relationship-list'),
    path('category-relationship-list/<int:pk>/',
         views.CategoryRelationshipDetail.as_view(), name='category-detail'),

    # image list: get all, get all filter by auction, get all
    path('auction-image-list/',
         views.AuctionImageList.as_view(), name='category-relationship-list'),
    path('auction-image-list/<int:pk>/',
         views.AuctionImageDetail.as_view(), name='category-detail'),
]
