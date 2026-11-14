from rest_framework import serializers

MAX_IMAGE_MB = 5


class SkinRequestSerializer(serializers.Serializer):
    image = serializers.ImageField()

    def validate_image(self, file):
        if file.size > MAX_IMAGE_MB * 1024 * 1024:
            raise serializers.ValidationError(f"Image must be under {MAX_IMAGE_MB} MB.")
        return file


class BodyRequestSerializer(serializers.Serializer):
    # All measurements in cm
    shoulder = serializers.FloatField(min_value=20, max_value=200)
    bust = serializers.FloatField(min_value=20, max_value=250)
    waist = serializers.FloatField(min_value=20, max_value=250)
    hips = serializers.FloatField(min_value=20, max_value=250)