from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Keyword, Flag, ContentItem
from .serializers import KeywordSerializer, FlagSerializer
from .services import scan_content_item

class KeywordListCreateView(generics.ListCreateAPIView):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer

class FlagListView(generics.ListAPIView):
    queryset = Flag.objects.all().order_by('-created_at')
    serializer_class = FlagSerializer

class FlagUpdateView(generics.UpdateAPIView):
    queryset = Flag.objects.all()
    serializer_class = FlagSerializer
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class ScanContentView(APIView):
    def post(self, request):
        data = request.data
        if isinstance(data, dict):
            data = [data]
            
        all_flags = []
        for item_data in data:
            flags = scan_content_item(item_data)
            all_flags.extend(flags)
            
        return Response({
            "message": f"Scan completed. processed {len(data)} items.",
            "flags_created_or_updated": len(all_flags)
        }, status=status.HTTP_200_OK)
