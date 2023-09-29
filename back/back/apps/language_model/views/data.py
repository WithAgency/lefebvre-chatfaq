from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action

from back.apps.language_model.models.data import KnowledgeBase, KnowledgeItem, AutoGeneratedTitle
from back.apps.language_model.serializers.data import KnowledgeBaseSerializer, KnowledgeItemSerializer, \
    AutoGeneratedTitleSerializer


class KnowledgeBaseAPIViewSet(viewsets.ModelViewSet):
    queryset = KnowledgeBase.objects.all()
    serializer_class = KnowledgeBaseSerializer

    @action(detail=True)
    def download_csv(self, request, *args, **kwargs):
        """
        A view to download all the knowledge base's items as a csv file:
        """
        kb = KnowledgeBase.objects.get(pk=kwargs["pk"])
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename={}'.format(
            kb.name + ".csv"
        )
        response.write(kb.to_csv())
        return response


class KnowledgeItemAPIViewSet(viewsets.ModelViewSet):
    queryset = KnowledgeItem.objects.all()
    serializer_class = KnowledgeItemSerializer
    filterset_fields = ["knowledge_base__id"]


class AutoGeneratedTitleAPIViewSet(viewsets.ModelViewSet):
    queryset = AutoGeneratedTitle.objects.all()
    serializer_class = AutoGeneratedTitleSerializer
    filterset_fields = ["knowledge_item__id"]
