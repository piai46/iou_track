from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import User
from .serializers import UserSerializer

class UserListView(APIView):

    def get(self, request):
        data = request.data
        if data:
            users = User.objects.filter(name__in=data['users']).order_by('name')
            users_serializers = UserSerializer(users, many=True)
            return Response({"users": users_serializers.data}, status=status.HTTP_200_OK)
        else:
            users = [user for user in User.objects.all()]
            users_serializers = UserSerializer(users, many=True)
            return Response({"users": users_serializers.data}, status=status.HTTP_200_OK)
        

class CreateUserView(APIView):

    def post(self, request):
        user = UserSerializer(data={"name":request.data["user"]})
        if user.is_valid():
            user.save()
            return Response(user.data, status=status.HTTP_201_CREATED)
        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CreateIOUView(APIView):

    def post(self, request):
        data = request.data
        if data:
            try:
                lender = User.objects.get(name=data['lender'])
                lender.owe_by[data['borrower']] = float(data['amount'])
                lender.balance += float(data['amount'])
                borrower = User.objects.get(name=data['borrower'])
                borrower.owes[data['lender']] = float(data['amount'])
                borrower.balance -= float(data['amount'])
                lender.save()
                borrower.save()
                users_serializers = UserSerializer([lender, borrower], many=True)
                return Response({"users": users_serializers.data}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)
