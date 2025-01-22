# products/services/product_service.py
from typing import List, Optional
from django.db.models import QuerySet
from ..models import Product, Category

class ProductService:
    @staticmethod
    def get_product_list(
        category_id: Optional[int] = None,
        search_query: Optional[str] = None,
        sort_by: Optional[str] = None
    ) -> QuerySet:
        """상품 목록을 조회합니다."""
        queryset = Product.objects.select_related('category').all()

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        if sort_by:
            if sort_by == 'price_asc':
                queryset = queryset.order_by('price')
            elif sort_by == 'price_desc':
                queryset = queryset.order_by('-price')
            elif sort_by == 'newest':
                queryset = queryset.order_by('-created_at')

        return queryset

    @staticmethod
    def get_product_detail(product_id: int) -> Product:
        """상품 상세 정보를 조회합니다."""
        from django.shortcuts import get_object_or_404

        return get_object_or_404(Product, id=product_id)

    @staticmethod
    def create_product(data: dict) -> Product:
        """새로운 상품을 생성합니다."""
        return Product.objects.create(**data)

    @staticmethod
    def update_product(product_id: int, data: dict) -> Product:
        """상품 정보를 수정합니다."""
        product = ProductService.get_product_detail(product_id)
        for key, value in data.items():
            setattr(product, key, value)
        product.save()
        return product

    @staticmethod
    def delete_product(product_id: int) -> None:
        """상품을 삭제합니다."""
        product = ProductService.get_product_detail(product_id)
        product.delete()
