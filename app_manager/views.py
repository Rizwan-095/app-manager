from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .decorators import validate_data, validate_query_record, validate_subscription
from .models import App, Subscription, Plan
from .serializers import AppSerializer, AppUpdateSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@validate_data
def create_app(request):
    user, data = request.user, request.data
    app = App.objects.create(
        name=data['name'],
        description=data['description'],
        owner=user
    )
    app.save()
    plan = Plan.objects.create()
    plan.save()
    subscription = Subscription.objects.create(
        app=app,
        plan=plan
    )
    subscription.save()
    return Response({'message': 'App created.'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_apps(request):
    apps = App.objects.filter(owner=request.user)
    serializer = AppSerializer(apps, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@validate_query_record
def get_single_app(request, app_id):
    app = App.objects.get(owner=request.user, id=app_id)
    serializer = AppSerializer(app, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@validate_query_record
def delete_app(request, app_id):
    app = App.objects.get(owner=request.user, id=app_id).delete()
    return Response({'message': 'app is deleted.'})


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@validate_query_record
def update_app(request, app_id):
    app = App.objects.get(owner=request.user, id=app_id)
    serializer = AppUpdateSerializer(app, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'App updated.'})
    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@validate_query_record
@validate_subscription
def upgrade_subscription(request, app_id):
    data = request.data
    app = App.objects.get(owner=request.user, id=app_id)
    new_plan = Plan.objects.create(
        name=data['plan'],
        price=data['price']
    )
    new_plan.save()
    new_subscription = Subscription.objects.create(
        app=app,
        plan=new_plan
    )
    new_subscription.save()
    return Response({'message': 'subscription is upgraded.'})
