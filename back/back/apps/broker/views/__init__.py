from datetime import datetime
from io import BytesIO
from zipfile import ZipFile

from django.db.models.functions import Trunc
from django.db.models import Count

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny

from ..models.message import AdminReview, AgentType, Conversation, Message, UserFeedback
from ..serializers import (
    AdminReviewSerializer,
    ConversationMessagesSerializer,
    UserFeedbackSerializer, ConversationSerializer, StatsSerializer,
)
from ..serializers.messages import MessageSerializer
import django_filters

from ...language_model.models import RAGConfig, Intent


class ConversationFilterSet(django_filters.FilterSet):
    rag = django_filters.CharFilter(method='filter_rag')
    reviewed = django_filters.CharFilter(method='filter_reviewed')

    class Meta:
        model = Conversation
        fields = {
           'created_date': ['lte', 'gte'],
        }

    def filter_rag(self, queryset, name, value):
        rag = RAGConfig.objects.filter(pk=value).first()
        return queryset.filter(message__stack__0__payload__rag_config_name=rag.name).distinct()

    def filter_reviewed(self, queryset, name, value):
        val = True
        if value == "completed":
            val = False
        if val:
            return queryset.filter(message__adminreview__isnull=val).exclude(message__adminreview__isnull=not val).distinct()
        return queryset.filter(message__adminreview__isnull=val).distinct()


class ConversationAPIViewSet(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name']
    filterset_class = ConversationFilterSet

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ConversationMessagesSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action == 'retrieve' or self.action == 'destroy':
            return [AllowAny(), ]
        return super(ConversationAPIViewSet, self).get_permissions()

    @action(methods=("get",), detail=False, authentication_classes=[], permission_classes=[AllowAny])
    def from_sender(self, request, *args, **kwargs):
        if not request.query_params.get("sender"):
            return JsonResponse(
                {"error": "sender is required"},
                status=400,
            )
        results = [ConversationSerializer(c).data for c in Conversation.conversations_from_sender(request.query_params.get("sender"))]
        return JsonResponse(
            results,
            safe=False,
        )

    @action(methods=("post",), detail=True, authentication_classes=[], permission_classes=[AllowAny])
    def download(self, request, *args, **kwargs):
        """
        A view to download all the knowledge base's items as a csv file:
        """
        ids = kwargs["pk"].split(",")
        if len(ids) == 1:
            conv = Conversation.objects.get(pk=ids[0])
            content = conv.conversation_to_text()
            filename = f"{conv.created_date.strftime('%Y-%m-%d_%H-%M-%S')}.txt"
            content_type = "text/plain"
        else:
            zip_content = BytesIO()
            with ZipFile(zip_content, "w") as _zip:
                for _id in ids:
                    conv = Conversation.objects.get(pk=_id)
                    _content = conv.conversation_to_text()
                    _zip.writestr(
                        conv.get_first_msg().created_date.strftime("%Y-%m-%d_%H-%M-%S")
                        + ".txt",
                        _content,
                    )

            filename = f"{datetime.today().strftime('%Y-%m-%d_%H-%M-%S')}.zip"
            content_type = "application/x-zip-compressed"
            content = zip_content.getvalue()

        response = HttpResponse(content, content_type=content_type)
        response["Content-Disposition"] = "attachment; filename={0}".format(filename)
        response["Access-Control-Expose-Headers"] = "Content-Disposition"
        return response


class MessageView(LoginRequiredMixin, viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class UserFeedbackAPIViewSet(viewsets.ModelViewSet):
    serializer_class = UserFeedbackSerializer
    queryset = UserFeedback.objects.all()
    permission_classes = [AllowAny]
    filterset_fields = ["message"]


class AdminReviewAPIViewSet(viewsets.ModelViewSet):
    serializer_class = AdminReviewSerializer
    queryset = AdminReview.objects.all()
    filterset_fields = ["message"]


class SenderAPIView(CreateAPIView, UpdateAPIView):
    def get(self, request):
        return JsonResponse(
            list(
                Message.objects.filter(sender__type=AgentType.human.value)
                .values_list("sender__id", flat=True)
                .distinct()
            ),
            safe=False,
        )


class Stats(APIView):
    def get(self, request):
        serializer = StatsSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        if not RAGConfig.objects.filter(pk=data["rag"]).exists():
            return JsonResponse(
                {"error": "RAG config not found"},
                status=400,
            )
        rag = RAGConfig.objects.get(pk=data["rag"])
        min_date = data.get("min_date", None)
        max_date = data.get("max_date", None)
        granularity = data.get("granularity", None)

        # ----------- Conversations -----------
        conversations = Conversation.objects
        if min_date:
            conversations = conversations.filter(created_date__gte=min_date)
        if max_date:
            conversations = conversations.filter(created_date__lte=max_date)

        conversations_rag_filtered = conversations.filter(
            message__stack__0__payload__rag_config_id=rag.id
        ).distinct()
        # --- Total conversations
        total_conversations = conversations_rag_filtered.count()
        # --- Message count per conversation
        conversations_message_count = conversations_rag_filtered.annotate(
            messages_count=Count("message")
        ).values("messages_count", "name")
        # --- Conversations by date
        conversations_by_date = conversations_rag_filtered.annotate(
            date=Trunc("created_date", granularity)
        ).values("created_date").annotate(count=Count("id"))

        # --- Conversations per RAG Config
        conversations_per_rag = conversations.filter(
            message__stack__0__payload__rag_config_id__isnull=False
        ).annotate(
            rag_id=Count("message__stack__0__payload__rag_config_id")
        ).values("message__stack__0__payload__rag_config_id")

        # ----------- Messages -----------
        messages = Message.objects
        if min_date:
            messages = messages.filter(created_date__gte=min_date)
        if max_date:
            messages = messages.filter(created_date__lte=max_date)
        messages_rag_filtered = messages.filter(
            stack__0__payload__rag_config_id=rag.id
        ).distinct()
        # --- Messages per RAG Config
        messages_per_rag = Message.objects.filter(
            stack__0__payload__rag_config_id__isnull=False
        ).annotate(
            rag_id=Count("stack__0__payload__rag_config_id")
        ).values("stack__0__payload__rag_config_id").annotate(count=Count("stack__0__payload__rag_config_id"))
        messages_per_rag_with_prev = messages_per_rag.filter(prev__isnull=False)
        # --- Chit chat count
        chit_chats_count = messages_per_rag_with_prev.filter(
            messageknowledgeitem__isnull=True
        ).count()
        chit_chats_percentage = chit_chats_count / messages_per_rag_with_prev.count() * 100
        # --- Unanswerable queries count
        intents_suggested = Intent.objects.filter(suggested_intent=True).values("pk")
        unanswerable_queries_count = messages_per_rag_with_prev.filter(
            intent__in=intents_suggested
        ).count()
        unanswerable_queries_percentage = unanswerable_queries_count / messages_per_rag_with_prev.count() * 100
        # --- Answerable queries count
        answerable_queries_count = messages_per_rag_with_prev.count() - unanswerable_queries_count
        answerable_queries_percentage = answerable_queries_count / messages_per_rag_with_prev.count() * 100

        return JsonResponse(
            {
                "total_conversations": total_conversations,
                # "conversations_per_rag": list(conversations_per_rag.all()),
                "conversations_message_count": list(conversations_message_count.all()),
                "messages_per_rag": list(messages_per_rag.all()),
                "conversations_by_date": list(conversations_by_date.all()),
                "chit_chats_count": chit_chats_count,
                "chit_chats_percentage": chit_chats_percentage,
                "unanswerable_queries_count": unanswerable_queries_count,
                "unanswerable_queries_percentage": unanswerable_queries_percentage,
                "answerable_queries_count": answerable_queries_count,
                "answerable_queries_percentage": answerable_queries_percentage,
            },
            safe=False,
        )
