from rest_framework.response import Response
from rest_framework import status
from .models import App, Subscription, Plan
from .validators import verify_plan


def validate_data(view_func):
    def wrapper(request):
        data = request.data
        user = request.user
        if not data['name']:
            return Response({"error": "app must contain a name."}, status=status.HTTP_400_BAD_REQUEST)
        if App.objects.filter(owner=user, name=data['name']).exists():
            return Response({"error": "app with this name already exists"}, status=status.HTTP_400_BAD_REQUEST)
        return view_func(request)
    return wrapper


def validate_query_record(view_func):
    def wrapper(request, app_id):
        try:
            app = App.objects.get(owner=request.user, id=app_id)
        except App.DoesNotExist:
            return Response({"error": "app with this id does not exist"}, status=status.HTTP_404_NOT_FOUND)
        return view_func(request, app_id)
    return wrapper


def validate_subscription(view_func):
    def wrapper(request, app_id):
        plans = ['free', 'standard', 'pro']
        data = request.data
        if data['plan'] not in plans:
            return Response({"error": "only free, standard and pro plans are available."}, status=status.HTTP_400_BAD_REQUEST)
        current_subscription = Subscription.objects.get(
            app__id=app_id, isActive=True)
        if current_subscription.plan.name == data['plan']:
            return Response({"error": "app already contains this plan. choose different plan."}, status=status.HTTP_400_BAD_REQUEST)
        if data['plan'] == 'free':
            return Response({"error": "cannot upgrade to free plan."}, status=status.HTTP_400_BAD_REQUEST)
        for i, item in enumerate(plans):
            if current_subscription.plan.name == item:
                current_plan_value = i
                break
        for i, item in enumerate(plans):
            if data['plan'] == item:
                requested_plan_value = i
                break
        if requested_plan_value < current_plan_value:
            return Response({"error": "cannot degrade current plan."}, status=status.HTTP_400_BAD_REQUEST)
        check_payment = verify_plan(data['plan'], data['price'])
        if check_payment['error'] == True:
            return Response({"error": check_payment['message']}, status=status.HTTP_400_BAD_REQUEST)
        current_subscription.isActive = False
        current_subscription.save()
        return view_func(request, app_id)
    return wrapper
