from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse

from .models import Product
from .serializers import ProductSerializer

def home(request):
    return JsonResponse({"message": "Welcome to Jewelry API"})


@api_view(['GET'])
def get_products(request):
    products = Product.objects.all()

    # 🔍 Price Filter
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    # 🔍 Metal Filter
    metal = request.GET.get('metal')
    if metal:
        products = products.filter(base_metal__iexact=metal)

    # 🔃 Sorting
    sort = request.GET.get('sort')

    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'latest':
        products = products.order_by('-id')
    elif sort == 'popularity':
        products = products.order_by('-rating')

    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_product(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=404)

    serializer = ProductSerializer(product)
    return Response(serializer.data)

from .models import Category
from .serializers import CategorySerializer


@api_view(['GET'])
def get_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_products_by_category(request, id):
    products = Product.objects.filter(category_id=id)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_product(request):
    serializer = ProductSerializer(data=request.data)

    if serializer.is_valid():   # 🔥 THIS ENABLES VALIDATION
        serializer.save()
        return Response({"message": "Product added successfully"})

    return Response(serializer.errors)
    
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer

@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def update_product(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=404)

    if request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Product updated successfully"})
        return Response(serializer.errors)

    elif request.method == 'DELETE':
        product.delete()
        return Response({"message": "Product deleted successfully"})
    

from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
def register_user(request):
    try:
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Username and password required"}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=400)

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return Response({"message": "User created successfully"})

    except Exception as e:
        return Response({"error": str(e)}, status=500)

from django.contrib.auth import authenticate

@api_view(['POST'])
def login_user(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Username and password required"}, status=400)

        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            })

        return Response({"error": "Invalid credentials"}, status=401)

    except Exception as e:
        return Response({"error": str(e)}, status=500)
    