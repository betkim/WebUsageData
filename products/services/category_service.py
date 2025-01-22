# products/services/category_service.py
from typing import List, Optional
from django.db.models import QuerySet
from ..models import Category

class CategoryService:
    @staticmethod
    def get_category_list() -> QuerySet:
        """카테고리 목록을 조회합니다."""
        return Category.objects.all()

    @staticmethod
    def create_category(data: dict) -> Category:
        """새로운 카테고리를 생성합니다."""
        return Category.objects.create(**data)