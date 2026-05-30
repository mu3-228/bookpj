from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView,CreateView,DeleteView,UpdateView
from .models import Book, Review
from django.contrib.auth.mixins import LoginRequiredMixin



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
class UpdateBookView(LoginRequiredMixin, UpdateView):
    template_name = 'book/book_update.html'
    model = Book
    fields = ('title', 'text', 'category', 'thumbnail')
    success_url = reverse_lazy('list-book')
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
    #
    def form_valid(self, form):
        print("🔥通った🔥ひ")
        print(form.errors)
        form.instance.book = Book.objects.get(pk=self.kwargs['book_id'])
        form.instance.user = self.request.user
        return super().form_valid(form)
    #   ↓レビュー対象の本を設定したり、レビュー後どこにいくか
    def get_success_url(self):
        return reverse_lazy('detail-book', kwargs={'pk': self.kwargs['book_id']})
    
# インデントいらない
def index_view(request):
    object_list = Book.objects.order_by('category')
    return render(request, 'book/index.html',{'object_list' : object_list})

