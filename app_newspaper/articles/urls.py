from django.urls import path
from .views import (
    ArticleListView,
    ArticleDetailsView,
    ArticleUpdateView,
    ArticleDeleteView,
    ArticleCreateView,
    CommentPost,  # Asegúrate de importar la vista para comentarios
    CommentDeleteView,
    CommentUpdateView
)

urlpatterns = [ #Incluyendo las URL's de los artículos
    path("<int:pk>/", ArticleDetailsView.as_view(), name='article_details'),
    path("<int:pk>/edit/", ArticleUpdateView.as_view(), name='article_edit'),
    path("<int:pk>/delete/", ArticleDeleteView.as_view(), name='article_delete'),
    path("new/" , ArticleCreateView.as_view(), name="article_new"),
    path('', ArticleListView.as_view(), name='article_list'),
    path("<int:pk>/comment/", CommentPost.as_view(), name='article_comment'),  # Nueva URL para comentarios
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    path('comment/<int:pk>/edit/', CommentUpdateView.as_view(), name='comment_edit'),
]