from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy, reverse
from .models import Article, Comment
from .forms import CommentForm

# Create your views here.
class CommentGet(LoginRequiredMixin, DetailView): #Creando la vista para ver comentarios (El usuario deberá loguearse)
    model = Article
    template_name = "article_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context
    

class CommentPost(SingleObjectMixin, FormView): #Creando la vista para publicar comentarios (El usuario deberá loguearse)
    model = Article
    form_class = CommentForm
    template_name = "article_details.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object ()
        return super().post(request, *args, **kwargs)
    
    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.article = self.object
        comment.author = self.request.user  # Asigna el autor al usuario que ha iniciado sesión
        comment.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("article_list")  # Cambiar a la lista de artículos
    

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'comment_delete.html'
    success_url = reverse_lazy('article_list')  # Redirigir a la lista de artículos después de eliminar el comentario

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user  # Solo permite que el autor elimine el comentario

    def handle_no_permission(self):
        return render(self.request, '403.html', status=403)  # Maneja el error si no tiene permiso


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm  # Asegúrate de usar el formulario adecuado para los comentarios
    template_name = 'comment_edit.html'
    success_url = reverse_lazy('article_list')  # Redirige a la lista de artículos después de la edición

    def test_func(self):
        # Solo el autor del comentario puede editarlo
        comment = self.get_object()
        return comment.author == self.request.user

    def handle_no_permission(self):
        # En caso de no tener permiso, muestra una página de error 403
        return render(self.request, '403.html', status=403)
    

class ArticleListView(LoginRequiredMixin, ListView): #Creando la vista para ver la lista de artículos (El usuario deberá esta logueado)
    model = Article
    template_name = "article_list.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()  # Proporciona un formulario de comentarios
        return context

    
class ArticleDetailsView(LoginRequiredMixin, View): #Creando la vista para ver los detalles del artículo (El usuario deberá esta logueado)
    def get(self, request, *args, **kwargs):
        view = CommentGet.as_view() #Ver comentarios
        return view(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        view = CommentPost.as_view() #Y postear comentarios
        return view(request, *args, **kwargs)
    
    
    
class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): # Creando la vista para actualizar un artículo 
                                                                              # (El usuario deberá esta logueado)
                                                                              # (Si el texto no es del autor arrojara error 403 FORBIDDEN)
    model = Article
    fields = ( #Título y cuerpo
        "title",
        "body",
        "image_url",  # Campo para la URL de la imagen
    )
    template_name = "article_edit.html"

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user
    
    def handle_no_permission(self):
        return render(self.request, '403.html', status=403)
    
    
class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView): # Creando la vista para eliminar un artículo 
                                                                              # (El usuario deberá esta logueado)
                                                                              # (Si el texto no es del autor arrojara error 403 FORBIDDEN)
    model = Article
    template_name = "article_delete.html"
    success_url = reverse_lazy("article_list")

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user
    
    def handle_no_permission(self):
        return render(self.request, '403.html', status=403)
    
    
class ArticleCreateView(LoginRequiredMixin, CreateView): # Creando la vista para eliminar un artículo (El usuario deberá esta logueado)
    model = Article
    template_name = "article_new.html"
    fields = (
        "title",
        "body",
        "image_url",  # Campo para la URL de la imagen
    )

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)