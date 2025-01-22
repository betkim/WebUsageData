# products/views.py
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.shortcuts import render
from .models import Product
from .services.product_service import ProductService
from .services.logging_service import LoggingService
from .services.category_service import CategoryService


class ProductListView(ListView):
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        return ProductService.get_product_list(
            category_id=self.request.GET.get('category'),
            search_query=self.request.GET.get('search'),
            sort_by=self.request.GET.get('sort')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = CategoryService.get_category_list()
        return context

class ProductDetailView(DetailView):
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_object(self):
        obj = ProductService.get_product_detail(self.kwargs['pk'])
        # 조회 로그 기록
        LoggingService.log_product_view(
            user_id=self.request.user.id if self.request.user.is_authenticated else None,
            product_id=obj.id,
            metadata={'referrer': self.request.META.get('HTTP_REFERER')}
        )
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_stats'] = LoggingService.get_product_view_stats(self.kwargs['pk'])
        return context
