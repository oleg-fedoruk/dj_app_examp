from django.db import models


class Post(models.Model):
    """Модель статей/постов"""

    title = models.CharField(max_length=255, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Статья')
    views = models.IntegerField(default=0, verbose_name='Количество просмотров')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = 'Статьи'
        ordering = ['-date_created']


class Comment(models.Model):
    """Модель комментариев"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Статья', related_name='comments')
    text = models.TextField(verbose_name='Текст комментария')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'{self.text[:15]}...'

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = 'Комментарии'
        ordering = ['-date_created']
