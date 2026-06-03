from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView,CreateView,DeleteView,UpdateView
from django.db.models import Avg
from .models import Book, Review


class ListBookView(LoginRequiredMixin, ListView):
    template_name = 'book/book_list.html'
    model = Book


class DetailBookView(LoginRequiredMixin, DetailView):
    model = Book


class CreateBookView(LoginRequiredMixin, CreateView):
    template_name = 'book/book_create.html'
    model = Book
    fields = ('title', 'text', 'category', 'thumbnail')
    success_url = reverse_lazy('list-book')


class DeleteBookView(LoginRequiredMixin, DeleteView):
    template_name = 'book/book_confirm_delete.html'
    model = Book
    success_url = reverse_lazy('list-book')

    def form_valid(self, form):
        form.instance.user = self.request.user


        return super().form_valid(form)


class UpdateBookView(LoginRequiredMixin, UpdateView):
    template_name = 'book/book_update.html'
    model = Book
    fields = ('title', 'text', 'category', 'thumbnail')



    def get_object(self, queryset = None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user:
            raise PermissionDenied
        return obj
    
    def get_success_url(self):
        return reverse('detail-book', kwargs={'pk': self.object.id})


class CreateReviewView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ('title', 'text', 'rate')
    template_name = 'book/review_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = Book.objects.get(pk=self.kwargs['book_id'])
        print(context)
        print(context['form'].errors)  # ←これ追加
        return context
    
    def form_valid(self, form):
        form.instance.user = self.request.user


        return super().form_valid(form)
    #??↓
    def form_valid(self, form):
        print("🔥通った🔥")
        print(form.errors)
        form.instance.book = Book.objects.get(pk=self.kwargs['book_id'])
        form.instance.user = self.request.user

        return super().form_valid(form)
    

    #   ↓レビュー対象の本を設定したり、レビュー後どこにいくか
    def get_success_url(self):
        return reverse_lazy('detail-book', kwargs={'pk': self.kwargs['book_id']})
    
# インデントいらない
def index_view(request):
    object_list = Book.objects.order_by('-id')
    ranking_list= Book.objects.annotate(avg_rating=Avg('review__rate)')).order_by('-avg_rating')

    return render(request, 'book/index.html',{'object_list' : object_list, 'ranking_list' : ranking_list})

