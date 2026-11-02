from django import forms
from .models import Post, Comment, Bbscomment, Reply
from markdownx.widgets import MarkdownxWidget
import datetime
import random

class PostForm(forms.ModelForm):

    class Meta:
        model = Post

        fields = ('title', 'text', 'category', 'is_public','created_at')

        widgets = {
            'text': MarkdownxWidget(attrs={'placeholder':'コメント', 'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline', 'cols': 60, 'rows': 10}),

            #'is_public': forms.CheckboxInput(disabled=True,attrs={'class':'form-check-input'}),
        }
        labels ={
            'title':'タイトル',
            'text':'',
            'category': 'カテゴリー',
            'is_public': '公開可能',
            'created_at': '登録日',

        }


class CommentForm(forms.ModelForm):

    
    #captcha = SimpleCaptchaField(
    #    widget=forms.TextInput(attrs={'class': 'form-control'}),
    #)
    #self.spamtext = str(random.randint(10000, 100000))

    class Meta:
        model = Comment
        fields = ('name', 'email', 'text',)
        widgets = {
            'text': MarkdownxWidget(attrs={'placeholder': 'コメント', 'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline', 'cols': 60, 'rows': 10}),
        }
        labels ={
            'name': 'お名前',
            'email': 'メール',
            'text': '',
		}




class BbscommentForm(forms.ModelForm):

    #captcha = SimpleCaptchaField(
    #    widget=forms.TextInput(attrs={'class': 'form-control'}),
    #)


    class Meta:
        model = Bbscomment
        fields = ('name', 'comment',  'bbstitle', 'is_public' )
        widgets = {
            'comment': MarkdownxWidget(attrs={'placeholder': 'コメント', 'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline', 'cols': 60, 'rows': 10}),

        }
        labels ={
            'name': 'お名前',
            'comment': '',
            #'cid': '順番号',
            'bbstitle': '親タイトル',
            'is_public': '公開する',

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for field in self.fields.values():
        #    field.widget.attrs['class'] = 'form-control'
        #    field.widget.attrs['placeholder'] = field.label
        #self.fields['cid'].widget = forms.HiddenInput()


