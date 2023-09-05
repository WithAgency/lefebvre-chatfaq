import csv

from rest_framework import serializers

from .models import Dataset, Item, LLMConfig, Utterance


class DatasetSerializer(serializers.ModelSerializer):
    MANDATORY_COLUMNS = ["intent", "answer", "url"]

    class Meta:
        model = Dataset
        fields = "__all__"

    # extra step when validating: the file must contain the following columns: intent, answer, url
    def validate(self, data):
        if "original_file" in data:
            f = data["original_file"]
            decoded_file = f.read().decode("utf-8").splitlines()
            reader = csv.DictReader(decoded_file)
            if not all(elem in reader.fieldnames for elem in self.MANDATORY_COLUMNS):
                raise serializers.ValidationError(
                    "The file must contain the following columns: "
                    + ", ".join(self.MANDATORY_COLUMNS)
                )
            f.seek(0)
        return data


class DatasetFromUrlSerializer(DatasetSerializer):
    url = serializers.URLField()

    class Meta:
        model = Dataset
        fields = ["name", "lang", "url"]


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"


class UtteranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utterance
        fields = "__all__"


class LLMConfigSerializer(serializers.ModelSerializer):
    status = serializers.CharField(read_only=True)

    class Meta:
        model = LLMConfig
        fields = "__all__"
