from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.urls import reverse

from store_app.models import *
from store_app.fields import ORDER_STATUS_CHOICES, REFUND_STATUS_CHOICES

from .forms import *

import django_filters
from django_filters.views import FilterView


"""
    Clothing Collection
"""


class ClothingCollectionCreate(CreateView):
    model = ClothingCollection
    form_class = CollectionForm
    template_name = 'store_app/clothing_collection/clothing_collection_form.html'

    def get_success_url(self):
        return reverse('admin_app:collection-list')


class ClothingCollectionList(ListView):
    model = ClothingCollection
    paginate_by = 10
    template_name = 'store_app/clothing_collection/clothing_collection_list.html'

    def get_ordering(self):
        ordering = self.request.GET.get('ordering', '-year')
        return ordering


class ClothingCollectionUpdate(UpdateView):
    model = ClothingCollection
    form_class = CollectionForm
    template_name = 'store_app/clothing_collection/clothing_collection_form.html'

    def get_success_url(self):
        return reverse('admin_app:collection-list')


class ClothingCollectionDelete(DeleteView):
    model = ClothingCollection
    form_class = CollectionForm
    template_name = 'store_app/delete_obj_form.html'

    def get_success_url(self):
        return reverse('admin_app:collection-list')

    def post(self, request, *args, **kwargs):
        super(ClothingCollectionDelete, self).delete(request, *args, **kwargs)
        return HttpResponseRedirect(self.get_success_url())


"""
    Categories
"""


class CategoryCreate(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'store_app/category/category_form.html'

    def get_success_url(self):
        return reverse('admin_app:category-list')


class CategoryList(ListView):
    model = Category
    paginate_by = 10
    template_name = 'store_app/category/category_list.html'

    def get_ordering(self):
        ordering = self.request.GET.get('ordering', 'title')
        return ordering


class CategoryUpdate(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'store_app/category/category_form.html'

    def get_success_url(self):
        return reverse('admin_app:category-list')


class CategoryDelete(DeleteView):
    model = Category
    template_name = 'store_app/delete_obj_form.html'

    def get_success_url(self):
        return reverse('admin_app:category-list')

    def post(self, request, *args, **kwargs):
        super(CategoryDelete, self).delete(request, *args, **kwargs)
        return HttpResponseRedirect(self.get_success_url())


"""
    Global Config
"""


class GlobalConfigCreate(CreateView):
    model = GlobalModel
    form_class = GlobalConfigForm
    template_name = 'store_app/global_config/global_config_form.html'

    def get_success_url(self):
        return reverse('admin_app:global-config-list')

    def form_valid(self, form):
        is_active = form.cleaned_data['active']
        if is_active:
            try:
                previous_active = GlobalModel.objects.get(active=True)
                previous_active.active = False
                previous_active.save()
            except GlobalModel.DoesNotExist:
                pass
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())


class GlobalConfigList(ListView):
    model = GlobalModel
    paginate_by = 10
    template_name = 'store_app/global_config/global_config_list.html'

    def get_ordering(self):
        ordering = self.request.GET.get('ordering', '-last_updated')
        return ordering


class GlobalConfigUpdate(UpdateView):
    model = GlobalModel
    form_class = GlobalConfigForm
    template_name = 'store_app/global_config/global_config_form.html'

    def get_success_url(self):
        return reverse('admin_app:global-config-list')

    def form_valid(self, form):
        is_active = form.cleaned_data['active']
        if is_active:
            try:
                previous_active = GlobalModel.objects.get(active=True)
                previous_active.active = False
                previous_active.save()
            except GlobalModel.DoesNotExist:
                pass
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())


class GlobalConfigDelete(DeleteView):
    model = GlobalModel
    template_name = 'store_app/delete_obj_form.html'

    def get_success_url(self):
        return reverse('admin_app:global-config-list')

    def post(self, request, *args, **kwargs):
        super(GlobalConfigDelete, self).delete(request, *args, **kwargs)
        return HttpResponseRedirect(self.get_success_url())


"""
    Custom Colors
"""


class CustomColorCreate(CreateView):
    model = CustomColor
    form_class = CustomColorForm
    template_name = 'store_app/custom_color/custom_color_form.html'

    def get_success_url(self):
        return reverse('admin_app:custom-color-list')


class CustomColorList(ListView):
    model = CustomColor
    paginate_by = 10
    template_name = 'store_app/custom_color/custom_color_list.html'

    def get_ordering(self):
        ordering = self.request.GET.get('ordering', '-nickname')
        return ordering


class CustomColorUpdate(UpdateView):
    model = CustomColor
    form_class = CustomColorForm
    template_name = 'store_app/custom_color/custom_color_form.html'

    def get_success_url(self):
        return reverse('admin_app:custom-color-list')


class CustomColorDelete(DeleteView):
    model = CustomColor
    template_name = 'store_app/delete_obj_form.html'

    def get_success_url(self):
        return reverse('admin_app:custom-color-list')

    def post(self, request, *args, **kwargs):
        super(CustomColorDelete, self).delete(request, *args, **kwargs)
        return HttpResponseRedirect(self.get_success_url())


"""
    Clothing Products
"""


class ClothingProductCreate(CreateView):
    model = ClothingProduct
    form_class = ClothingProductForm
    template_name = 'store_app/clothing_product/clothing_product_form.html'

    def get_success_url(self):
        return reverse('admin_app:clothing-product-list')

    def get_context_data(self, **kwargs):
        context = super(ClothingProductCreate, self).get_context_data(**kwargs)
        context['picture_required'] = True
        return context

    def form_valid(self, form):
        self.object = form.save()
        if 'primary_image' in self.request.FILES:
            primary_image = self.request.FILES['primary_image']
            ClothingProductImage.objects.create(image=primary_image, type_of_image="PRIMARY", product=self.object)
        if 'secondary_image' in self.request.FILES:
            secondary_image = self.request.FILES['secondary_image']
            ClothingProductImage.objects.create(image=secondary_image, type_of_image="SECONDARY", product=self.object)
        if len(self.request.FILES.getlist('extra_images')) > 0:
            extra_images = self.request.FILES.getlist('extra_images')
            for extra_image in extra_images:
                ClothingProductImage.objects.create(image=extra_image, type_of_image="EXTRA", product=self.object)
        return HttpResponseRedirect(self.get_success_url())


class ClothingProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    code = django_filters.CharFilter(lookup_expr='icontains')
    collections = django_filters.ModelChoiceFilter(queryset=ClothingCollection.objects.all())
    categories = django_filters.ModelChoiceFilter(queryset=Category.objects.all())

    class Meta:
        model = ClothingProduct
        fields = ['name', 'code', 'collections', 'categories']


class ClothingProductSimpleFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    code = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = ClothingProduct
        fields = ['name', 'code']


class ClothingProductList(FilterView):
    model = ClothingProduct
    filterset_class = ClothingProductFilter
    context_object_name = 'clothing_products'
    paginate_by = 10
    template_name = 'store_app/clothing_product/clothing_product_list.html'

    def get_ordering(self):
        ordering = self.request.GET.get('ordering', '-name')
        return ordering


class ClothingProductUpdate(UpdateView):
    model = ClothingProduct
    form_class = ClothingProductForm
    template_name = 'store_app/clothing_product/clothing_product_form.html'

    def get_success_url(self):
        return reverse('admin_app:clothing-product-list')

    def get_context_data(self, **kwargs):
        context = super(ClothingProductUpdate, self).get_context_data(**kwargs)
        context['picture_required'] = False
        return context

    def form_valid(self, form):
        self.object = form.save()
        if 'primary_image' in self.request.FILES:
            primary_image = self.request.FILES['primary_image']
            try:
                old_primary_image = ClothingProductImage.objects.get(type_of_image="PRIMARY", product=self.object)
                old_primary_image.delete()
            except:
                pass
            ClothingProductImage.objects.create(image=primary_image, type_of_image="PRIMARY", product=self.object)
        if 'secondary_image' in self.request.FILES:
            secondary_image = self.request.FILES['secondary_image']
            try:
                old_secondary_image = ClothingProductImage.objects.get(type_of_image="SECONDARY", product=self.object)
                old_secondary_image.delete()
            except:
                pass
            ClothingProductImage.objects.create(image=secondary_image, type_of_image="SECONDARY", product=self.object)
        if len(self.request.FILES.getlist('extra_images')) > 0:
            extra_images = self.request.FILES.getlist('extra_images')
            try:
                old_extra_images = ClothingProductImage.objects.filter(type_of_image="EXTRA", product=self.object)
                for old_extra_image in old_extra_images:
                    old_extra_image.delete()
            except:
                pass
            for extra_image in extra_images:
                ClothingProductImage.objects.create(image=extra_image, type_of_image="EXTRA", product=self.object)
        return HttpResponseRedirect(self.get_success_url())


class ClothingProductDelete(DeleteView):
    model = ClothingProduct
    template_name = 'store_app/delete_obj_form.html'

    def get_success_url(self):
        return reverse('admin_app:clothing-product-list')

    def post(self, request, *args, **kwargs):
        super(ClothingProductDelete, self).delete(request, *args, **kwargs)
        return HttpResponseRedirect(self.get_success_url())


class ClothingProductFilterCollection(FilterView):
    model = ClothingProduct
    paginate_by = 10
    filterset_class = ClothingProductSimpleFilter
    context_object_name = 'clothing_products'
    template_name = 'store_app/clothing_product/clothing_product_list.html'
    ordering = ['-name']

    def get_queryset(self, **kwargs):
        collection_pk = self.kwargs['pk']
        collection = ClothingCollection.objects.get(pk=collection_pk)
        return collection.get_products_set().order_by('name')

    def get_ordering(self):
        ordering = self.request.GET.get('ordering', '-name')
        return ordering


class ClothingProductFilterCategory(ListView):
    model = ClothingProduct
    paginate_by = 10
    template_name = 'store_app/clothing_product/clothing_product_list.html'

    def get_queryset(self, **kwargs):
        category_pk = self.kwargs['pk']
        category = Category.objects.get(pk=category_pk)
        return category.get_products_set()

    def get_ordering(self):
        ordering = self.request.GET.get('ordering', '-name')
        return ordering


"""
    Orders
"""

class OrderFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    phone = django_filters.CharFilter(lookup_expr='icontains')
    status = django_filters.ChoiceFilter(choices=ORDER_STATUS_CHOICES)

    class Meta:
        model = ClothingProduct
        fields = ['first_name', 'last_name', 'email', 'phone', 'status']


class OrderList(FilterView):
    model = Order
    filterset_class = OrderFilter
    context_object_name = 'orders'
    paginate_by = 10
    template_name = 'store_app/order/order_list.html'

    def get_queryset(self):
        return Order.objects.filter(ordered=True).order_by('-ordered_date')


class OrderCreate(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'store_app/order/order_form.html'

    def get_success_url(self):
        return reverse('admin_app:order-list')


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.ordered = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class OrderUpdate(UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'store_app/order/order_form.html'

    def get_success_url(self):
        return reverse('admin_app:order-list')


class OrderDelete(DeleteView):
    model = Order
    template_name = 'store_app/delete_obj_form.html'

    def get_success_url(self):
        return reverse('admin_app:order-list')

    def post(self, request, *args, **kwargs):
        super(OrderDelete, self).delete(request, *args, **kwargs)
        return HttpResponseRedirect(self.get_success_url())


class OrderDetail(DetailView):
    model = Order
    template_name = 'store_app/order/order_detail.html'
    queryset = Order.objects.all()


"""
    Payments
"""
class PaymentFilter(django_filters.FilterSet):
    email = django_filters.CharFilter(lookup_expr='icontains')
    refund = django_filters.ChoiceFilter(choices=REFUND_STATUS_CHOICES)

    class Meta:
        model = Payment
        fields = ['email', 'refund']


class PaymentList(FilterView):
    model = Payment
    filterset_class = PaymentFilter
    context_object_name = 'payments'
    paginate_by = 10
    template_name = 'store_app/payment/payment_list.html'

    def get_queryset(self):
        return Payment.objects.order_by('-timestamp')


class PaymentCreate(CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'store_app/payment/payment_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        self.object.ip_address = ip
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('admin_app:payment-list')


class PaymentUpdate(UpdateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'store_app/payment/payment_form.html'

    def get_success_url(self):
        return reverse('admin_app:payment-list')


class PaymentDelete(DeleteView):
    model = Payment
    template_name = 'store_app/delete_obj_form.html'

    def get_success_url(self):
        return reverse('admin_app:payment-list')

    def post(self, request, *args, **kwargs):
        super(PaymentDelete, self).delete(request, *args, **kwargs)
        return HttpResponseRedirect(self.get_success_url())
