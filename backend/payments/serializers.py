from rest_framework import serializers

from payments.models import Bill


class BillSerializer(serializers.ModelSerializer):
    reserve = serializers.StringRelatedField()
    
    class Meta:
        model = Bill
        fields = '__all__'