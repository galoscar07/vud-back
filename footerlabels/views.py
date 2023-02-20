from rest_framework import generics

from footerlabels.models import Footerlabels
from footerlabels.serializers import FooterlabelsSerializer


class FooterLabelList(generics.ListCreateAPIView):
    queryset = Footerlabels.objects.all()
    serializer_class = FooterlabelsSerializer


class FooterLabelDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Footerlabels.objects.all()
    serializer_class = FooterlabelsSerializer



# Older way to do it
# class FooterLabelList(APIView):
#     """
#     List all footer labels, or create a new footer label.
#     """
#     def get(self, request, format=None):
#         snippets = Footerlabels.objects.all()
#         serializer = FooterlabelsSerializer(snippets, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = FooterlabelsSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class FooterLabelDetail(APIView):
#     """
#     Retrieve, update or delete a footer label instance.
#     """
#     def get_object(self, pk):
#         try:
#             return Footerlabels.objects.get(pk=pk)
#         except Footerlabels.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = FooterlabelsSerializer(snippet)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = FooterlabelsSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)