from django.db import models
from django.utils import timezone
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

class Category(models.Model):
    name = models.CharField(verbose_name='カテゴリ', max_length=255)
    created_at = models.DateTimeField(verbose_name='作成日', default=timezone.now)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(verbose_name='タイトル', max_length=255)
    text = MarkdownxField(verbose_name='本文', help_text='マークダウン形式で書いてください（画像はドラッグ＆ドロップ）')
    category = models.ForeignKey(Category, verbose_name='カテゴリ', on_delete=models.PROTECT, null=False)
    is_public = models.BooleanField(verbose_name='公開可能か?', default=False)
    created_at = models.DateTimeField(verbose_name='作成日', default=timezone.now)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)

    def __str__(self):
        return self.title

    def convert_markdown_to_html(self):
      return markdownify(self.text)

class Link(models.Model):
    name = models.CharField(verbose_name='リンク名', max_length=255)
    url = models.CharField(verbose_name='url', max_length=255)
    created_at = models.DateTimeField(verbose_name='作成日', default=timezone.now)

    def __str__(self):
        return self.name


class Comment(models.Model):
    name = models.CharField(verbose_name='お名前', max_length=255, default='名無し')
    text = MarkdownxField(verbose_name='本文', help_text='マークダウン形式で書いてください（画像はドラッグ＆ドロップ）')
    email = models.EmailField(verbose_name='メールアドレス', blank=True)
    post = models.ForeignKey(Post, verbose_name='対象記事', on_delete=models.CASCADE)
    is_public = models.BooleanField(verbose_name='公開？',default=1)
    created_at = models.DateTimeField(verbose_name='作成日', default=timezone.now)

    def __str__(self):
        return self.text[:20]
    
    def convert_markdown_to_html(self):
      return markdownify(self.text)


class Reply(models.Model):
    name = models.CharField(verbose_name='名前', max_length=255, default='名無し')
    text = MarkdownxField(verbose_name='本文', help_text='マークダウン形式で書いてください（画像はドラッグ＆ドロップ）')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name='対象コメント')
    is_public = models.BooleanField(verbose_name='公開？', default=1)
    created_at = models.DateTimeField(verbose_name='作成日', default=timezone.now)

    def __str__(self):
        return self.text[:20]

    def convert_markdown_to_html(self):
      return markdownify(self.text)

class Bbstitle(models.Model):
    maintitle = models.CharField(verbose_name='メインタイトル',max_length=255)
    subtitle = models.CharField(verbose_name='サブタイトル',max_length=255)
    created_at = models.DateTimeField(verbose_name='作成日',default=timezone.now)

    def __str__(self):
        return self.maintitle


class Bbscomment(models.Model):
    bbstitle = models.ForeignKey(Bbstitle, on_delete=models.PROTECT, null=True)
    created_at = models.DateTimeField(verbose_name='作成日',default=timezone.now)
    name = models.CharField(verbose_name='名前',max_length=150)
    #pass1 = models.CharField(max_length=100, blank=True, null=True)
    comment = MarkdownxField(verbose_name='コメント', help_text='Markdown形式で書いてください')
    is_public = models.BooleanField(verbose_name='公開？',default=1)

    def __str__(self):
        return self.comment[:20]

    def convert_markdown_to_html(self):
      return markdownify(self.comment)

