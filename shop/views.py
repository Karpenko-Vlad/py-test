from django.db import transaction
from rest_framework import permissions, status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from shop.models import AdminAccessPermission, Product, Card, Invoice, CardItem, InvoiceItem
from shop.serializers import ProductSerializer, InvoiceSerializer, CardSerializer
from shop.utils import generate_and_send_pdf_for_invoice


class ProductViewSet(ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView, GenericViewSet, GenericAPIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, AdminAccessPermission]

    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductSerializer


class CardViewSet(ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView, GenericViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, AdminAccessPermission]

    queryset = Card.objects.all().order_by('-id')
    serializer_class = CardSerializer


class InvoiceViewSet(ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView, GenericViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, AdminAccessPermission]

    queryset = Invoice.objects.all().order_by('-id')
    serializer_class = InvoiceSerializer


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def products(request):
    serializer = ProductSerializer(Product.objects.all().sorted_by('-id'), many=True)
    return Response(data=serializer.data)


@api_view(['POST', 'DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def product_add_to_card(request):
    if request.method == "POST":
        if 'product_id' and 'product_count' not in request.POST:
            return Response(request.POST, status.HTTP_204_NO_CONTENT)

        card = request.user.cards.first()
        if not card:
            card = Card.objects.create(user_id=request.user.id)

        item = CardItem.objects.filter(card_id=card.id,
                                       item_id=request.POST['product_id']).first()
        if not item:
            item = CardItem.objects.create(card_id=card.id,
                                           item_id=request.POST['product_id'],
                                           count=request.POST['product_count'])
            return Response(request.POST, status.HTTP_201_CREATED)
        else:
            item.count += int(request.POST['product_count'])
            item.save()

        return Response({'product_id': item.item.id, 'product_count': item.count}, status.HTTP_202_ACCEPTED)

    elif request.method == "DELETE":
        if 'product_id' not in request.POST:
            return Response(request.POST, status.HTTP_204_NO_CONTENT)

        card = request.user.cards.first()
        if not card:
            return Response(request.POST, status.HTTP_204_NO_CONTENT)

        item = CardItem.objects.filter(card_id=card.id,
                                       item_id=request.POST['product_id']).first()
        if not item:
            return Response(request.POST, status.HTTP_204_NO_CONTENT)
        item.delete()

        return Response(request.POST, status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@transaction.atomic
def card_buy(request):
    card = request.user.cards.first()
    if not card:
        return Response(request.POST, status.HTTP_204_NO_CONTENT)

    card_items = CardItem.objects.filter(card_id=card.id).all()
    if not card_items:
        return Response(request.POST, status.HTTP_204_NO_CONTENT)

    invoice = Invoice.objects.create(user_id=request.user.id,
                                     for_email=request.user.email)

    for card_item in card_items:
        InvoiceItem.objects.create(invoice_id=invoice.id,
                                   fixed_price=card_item.item.price,
                                   item_id=card_item.item.id,
                                   count=card_item.count)
        card_item.delete()

    if generate_and_send_pdf_for_invoice(request, invoice.id):
        return Response(request.POST, status.HTTP_200_OK)

    return Response(request.POST, status.HTTP_200_OK)
