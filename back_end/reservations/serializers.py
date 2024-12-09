from rest_framework import serializers

from reservations.models import Reserve


class ReserveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserve
        fields = '__all__'