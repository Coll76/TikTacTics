from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import PhishingLink, PhishingData
from .serializers import PhishingLinkSerializer, PhishingDataSerializer
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly

# View to create a phishing link - available to all authenticated users
class PhishingLinkCreateView(generics.CreateAPIView):
    serializer_class = PhishingLinkSerializer
    queryset = PhishingLink.objects.all()
    permission_classes = [IsAuthenticated]  # Ensure the user is logged in

# View to retrieve or delete a phishing link - restricted to owners only
class PhishingLinkDetailView(generics.RetrieveDestroyAPIView):
    queryset = PhishingLink.objects.all()
    serializer_class = PhishingLinkSerializer
    permission_classes = [IsOwnerOrReadOnly]  # Ensure only the owner can delete

# View to create phishing data - available to all authenticated users
class PhishingDataCreateView(generics.CreateAPIView):
    queryset = PhishingData.objects.all()
    serializer_class = PhishingDataSerializer
    permission_classes = [IsAuthenticated]  # Ensure the user is logged in

# View to list phishing data - available to admins and owners of the data
class PhishingDataListView(generics.ListAPIView):
    queryset = PhishingData.objects.all()
    serializer_class = PhishingDataSerializer
    permission_classes = [IsAdminOrReadOnly]  # Admins can view, modify if needed
