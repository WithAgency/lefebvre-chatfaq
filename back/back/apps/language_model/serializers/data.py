import csv

from rest_framework import serializers

from back.apps.language_model.models.data import KnowledgeBase, KnowledgeItem, AutoGeneratedTitle, Intent, \
    KnowledgeItemImage, DataSource


class KnowledgeBaseSerializer(serializers.ModelSerializer):
    num_of_data_sources = serializers.SerializerMethodField()
    num_of_knowledge_items = serializers.SerializerMethodField()

    def get_num_of_data_sources(self, obj):
        return obj.datasource_set.count()

    def get_num_of_knowledge_items(self, obj):
        return obj.knowledgeitem_set.count()

    class Meta:
        model = KnowledgeBase
        fields = "__all__"


class DataSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSource
        fields = "__all__"

    # extra step when validating CSVs: the file must contain the following columns: title, content, url
    def validate(self, data):
        if data.get('original_csv') is not None:
            title_index, content_index, url_index = data.get("title_index_col"), data.get("content_index_col"), data.get("url_index_col")
            if title_index is None or content_index is None or url_index is None:
                errors = {}
                if title_index is None:
                    errors["title_index_col"] = ["You must specify the index of the title column in the CSV"]
                if content_index is None:
                    errors["content_index_col"] = ["You must specify the index of the content column in the CSV"]
                if url_index is None:
                    errors["url_index_col"] = ["You must specify the index of the url column in the CSV"]
                raise serializers.ValidationError(errors)

            f = data["original_csv"]
            decoded_file = f.read().decode("utf-8").splitlines()
            reader = csv.reader(decoded_file)
            next(reader) if data["csv_header"] else None
            mandatory_columns = [title_index, content_index, url_index]
            for _i, row in enumerate(reader):
                if len(row) < max(mandatory_columns):
                    raise serializers.ValidationError({
                        "original_csv": f"Row {_i + 1} does not contain all the required columns: {', '.join(str(i) for i in mandatory_columns)}"
                    })
                if not all(row[i].strip() if len(row) > i else None for i in mandatory_columns):
                    raise serializers.ValidationError({
                        "original_csv": f"Row {_i + 1} does not contain all the required columns: {', '.join(str(i) for i in mandatory_columns)}"
                    })
            f.seek(0)
        return data

    def to_internal_value(self, data):
        if "knowledge_base" in data:
            kb = KnowledgeBase.objects.filter(name=data["knowledge_base"]).first()
            if kb:
                data["knowledge_base"] = str(kb.pk)
        return super().to_internal_value(data)


class KnowledgeBaseFromUrlSerializer(KnowledgeBaseSerializer):
    url = serializers.URLField()

    class Meta:
        model = KnowledgeBase
        fields = ["name", "lang", "url"]


class KnowledgeItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnowledgeItem
        fields = "__all__"

    def to_internal_value(self, data):
        if "knowledge_base" in data:
            kb = KnowledgeBase.objects.filter(name=data["knowledge_base"]).first()
            if kb:
                data["knowledge_base"] = str(kb.pk)
        return super().to_internal_value(data)


class KnowledgeItemImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnowledgeItemImage
        fields = "__all__"

    def to_representation(self, instance):
        # add the file name to the representation
        ret = super().to_representation(instance)
        ret["image_file_name"] = instance.image_file.name
        return ret


class AutoGeneratedTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutoGeneratedTitle
        fields = "__all__"


class IntentSerializer(serializers.ModelSerializer):
    num_of_knowledge_items = serializers.SerializerMethodField()
    num_of_messages = serializers.SerializerMethodField()
    name_of_knowledge_base = serializers.SerializerMethodField()

    def get_num_of_knowledge_items(self, obj):
        return obj.knowledge_item.count()

    def get_num_of_messages(self, obj):
        return obj.message.count()

    def get_name_of_knowledge_base(self, obj):
        ki = obj.knowledge_item.first()
        if ki:
            return ki.knowledge_base.name

    class Meta:
        model = Intent
        fields = "__all__"

    def to_internal_value(self, data):
        if "knowledge_base" in data:
            kb = KnowledgeBase.objects.filter(name=data["knowledge_base"]).first()
            if kb:
                data["knowledge_base"] = str(kb.pk)
        return super().to_internal_value(data)
