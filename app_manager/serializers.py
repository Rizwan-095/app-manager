from rest_framework import serializers
from .models import App, Plan, Subscription


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer()

    class Meta:
        model = Subscription
        fields = '__all__'


class AppSerializer(serializers.ModelSerializer):
    # subscriptions = SubscriptionSerializer(
    #     many=True, source='subscription_set')
    subscriptions = serializers.SerializerMethodField()

    class Meta:
        model = App
        fields = '__all__'

    def get_subscriptions(self, obj):
        active_subscriptions = obj.subscription_set.filter(isActive=True)
        return SubscriptionSerializer(active_subscriptions, many=True).data


class AppUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = ('name', 'description')
