from rest_framework import serializers

from payments.models import Bill


class BillSerializer(serializers.ModelSerializer):
    reserve = serializers.HyperlinkedRelatedField(view_name='reservations:reserve-detail', read_only=True)
    
    class Meta:
        model = Bill
        fields = '__all__'