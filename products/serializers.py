from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    final_price = serializers.SerializerMethodField()
    _links = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'shop', 'price', 'sku', 'description', 'location',
            'discount', 'category', 'stock', 'is_available', 'picture', 'is_delete', 'final_price', '_links'
        ]
        read_only_fields = ('id', 'is_delete')

    def get__links(self, obj):
        request = self.context.get('request')
        base = request.build_absolute_uri('/')[:-1] if request else ''
        return [
            {
                'rel': 'self',
                'href': f"{base}/products",
                'action': 'POST',
                'types': ['application/json']
            },
            {
                'rel': 'self',
                'href': f"{base}/products/{obj.id}/",
                'action': 'GET',
                'types': ['application/json']
            },
            {
                'rel': 'self',
                'href': f"{base}/products/{obj.id}/",
                'action': 'PUT',
                'types': ['application/json']
            },
            {
                'rel': 'self',
                'href': f"{base}/products/{obj.id}/",
                'action': 'DELETE',
                'types': ['application/json']
            }
        ]

    # keep representation deterministic and include _links
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['_links'] = self.get__links(instance)
        return data

    def get_final_price(self, obj):
        return obj.final_price()
