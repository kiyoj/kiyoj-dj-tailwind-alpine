from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import  CreateView, UpdateView, DeleteView
from .models import Post, Category, Comment, Reply, Bbstitle, Bbscomment
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from django.views.decorators.http import require_POST
from django.db.models import Max, Min, Count, Q
from django.http import Http404
from .forms import (
    CommentForm, PostForm, BbscommentForm
)


from django.conf import settings
from django.core.mail import send_mail, EmailMessage

def paginator_list(request, queryset, count):
    paginator = Paginator(queryset, count)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    try:
        temp = page_obj.paginator.page(page)
    except(EmptyPage, InvalidPage):
        temp = page_obj.paginator.page(1)
    index = temp.number - 1
    max_index = len(page_obj.paginator.page_range)
    start_index = index - 2 if index >= 3 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    page_range = list(page_obj.paginator.page_range)[start_index:end_index]

    context = {
        'object_list': page_obj.object_list,
        'page_obj': page_obj,
        'page_range': page_range,
    }
    return context


class PostList(ListView):
    model = Post
    template_name = 'blog/post_index.html'
    paginate_by = 5

    def get_queryset(self):
        qs = Post.objects.order_by('-created_at').filter(is_public=True)
        search = self.request.GET.get("search", None)
        if search:
        	qs = qs.filter( Q(title__icontains=search) | Q(text__icontains=search)	)

        category = self.request.GET.get('category', None)

        if category:
        	qs = qs.filter(category=category)

        return qs


class PostDetail(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        #if 'return_id' in self.request.session:
        self.request.session['return_id'] = obj.id
        self.request.session['category_id'] = obj.category.id
        if not obj.is_public and not self.request.user.is_authenticated:
            raise Http404
        return obj


class CommentFormView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/post_comment_form.html'


    def form_valid(self, form):
        comment = form.save(commit=False)
        post_pk = self.kwargs['pk']
        comment.post_id = post_pk
        comment.save()

        return redirect('blog:post_detail', pk=post_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_pk = self.kwargs['pk']
        context['post'] = get_object_or_404(Post, pk=post_pk)
        return context




@require_POST
def post_comment_off(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.is_public = False
    comment.save()
    return redirect('blog:post_detail', pk=comment.post.id)

@require_POST
def post_comment_on(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.is_public = True
    comment.save()
    return redirect('blog:post_detail', pk=comment.post.id)


def post_edit(request, pk=None):
    if pk:
        post = get_object_or_404(Post, pk=pk)
    else:
        post = Post()

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('blog:post_detail', pk=post.id)
    else:  #GETの時
        form = PostForm(instance=post)

    context = {
        'form': form,
        'pk': pk,
        'post_id': request.session['return_id'],

    }
    return render(request, 'blog/post_edit.html', context)


class PostUpdate(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post_pk = self.kwargs['pk']
        #post.category  = get_object_or_404(Category, pk=post_pk)
        post.save()
        return redirect('blog:post_detail', pk=post_pk)


class PostCreate(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        #post.category = self.request.session['category_id']
        post.save()
        #post_pk = self.kwargs['pk']
        #post.category  = get_object_or_404(Category, pk=post.pk)
        #post.save()

        return redirect('blog:post_detail', pk=post.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post()
        post.is_public = True
        #object = get_object_or_404(Post, pk=self.request.session['return_id'])
        post.category = get_object_or_404(Category, pk=self.request.session['category_id'])
        form = PostForm(instance=post)
        #form.fields['is_public'] = True
        context['form'] =form
        #context['object'] = object
        return context


class PostDelete(DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'


class BbsIndex(ListView):
    model = Bbscomment
    template_name = 'blog/bbs_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = Bbscomment.objects.filter(is_public=True).order_by('-created_at')
        search = self.request.GET.get("search", None)
        if search:
        	qs = qs.filter( Q(name__icontains=search) | Q(comment__icontains=search))

        tmpcontext = paginator_list(self.request, qs, 10)
        context['object_list'] = tmpcontext['object_list']
        context['page_obj'] = tmpcontext['page_obj']
        context['page_range'] = tmpcontext['page_range']
        return context


class BbsListView(ListView):
    model = Bbscomment
    template_name = 'blog/bbs_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bbs_pk = self.kwargs['pk']
        bbs_comments = Bbscomment.objects.filter(bbstitle=bbs_pk, is_public=True).order_by('-created_at')
        self.request.session['bbs_return_id'] = bbs_pk
        tmpcontext = paginator_list(self.request, bbs_comments, 5)
        context['object_list'] = tmpcontext['object_list']
        context['page_obj'] = tmpcontext['page_obj']
        context['page_range'] = tmpcontext['page_range']
        return context


###使ってない　あとでつかうかも？
class BbsDetail(DetailView):
    model = Bbscomment
    template_name = 'blog/bbs_detail.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        #if 'return_id' in self.request.session:
        self.request.session['bbs_return_id'] = obj.id
        if not obj.is_public and not self.request.user.is_authenticated:
            raise Http404
        return obj


class BbsCreate(CreateView):
    model = Bbscomment
    template_name = 'blog/bbs_form.html'
    form_class = BbscommentForm

    def form_valid(self, form):
        bbs = form.save(commit=False)
        bbs.save()
        bbs_id = self.request.session['bbs_return_id']
        #print(bbs_id)
        return redirect('blog:bbs_detail', pk=bbs_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        bbs = Bbscomment()
        bbs.bbstitle = get_object_or_404(Bbstitle, pk=self.request.session['bbs_return_id'])
        form = BbscommentForm(instance=bbs)
        context['form'] = form
        return context


class BbsUpdate(UpdateView):
    model = Bbscomment
    template_name = 'blog/bbs_form.html'

    form_class = BbscommentForm

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if not obj.is_public and not self.request.user.is_authenticated:
            raise Http404
        return obj

    def form_valid(self, form):

        bbs = form.save(commit=False)
        #bbs_pk = self.kwargs['pk']
        #bbs.bbstitle = get_object_or_404(Bbstitle, pk=bbs_pk)
        #bbs.cid = self.request.session['bbs_cid']
        bbs.save()
        bbs_id = self.request.session['bbs_return_id']
        #print(bbs_id)
        return redirect('blog:bbs_detail', pk=bbs_id)


## 最初に作ったけど今は使ってない blog/bbs_edit.htmlも使ってない
def bbs_list(request):

    allbbs = Bbscomment.objects.all().order_by('-created_at')
    context = paginator_list(request, allbbs, 10)

    return render(request, 'blog/bbs_index.html', context)


def bbs_edit(request, pk=None):
    if pk:
        bbs = get_object_or_404(Bbscomment, pk=pk)
    else:
        bbs = Bbscomment()
        bbs.bbstitle = get_object_or_404(Bbstitle, pk=request.session['bbs_return_id'])
        #bbs.cid = Count(Bbscomment.objects.filter(bbstitle=request.session['bbs_return_id']))+1
        bbs.cid = Bbscomment.objects.filter(bbstitle=request.session['bbs_return_id']).count() + 1
        #bbs.cid = Bbscomment.objects.filter(bbstitle=request.session['bbs_return_id']).aggregate(Max('cid')) + 1
        #print(bbs.cid)

    if request.method == 'POST':
        form = BbscommentForm(request.POST, instance=bbs)
        if form.is_valid():
            bbs = form.save(commit=False)
            #bbs.cid = Count(Bbscomment.objects.filter(bbstitle=bbs.pk)) + 1
            bbs.save()
            return redirect('blog:bbs_detail', pk=bbs.id)
    else:  #GETの時

        form = BbscommentForm(instance=bbs)

    context = {
        'form': form,
        'pk': pk,
        #'bbs': bbs,
        #'session_bbs_id': request.session['bbs_return_id'],

    }
    return render(request, 'blog/bbs_edit.html', context)


def bbs_add(request, pk):
    bbs = get_object_or_404(Bbscomment, pk=pk)
    #bbs_cid = Count(Bbscomment.objects.get(bbstitle=bbs.bbstitle))+1
    if request.method == 'POST':
        form = BbscommentForm(request.POST)
        if form.is_valid():
            bbs = form.save(commit=False)
            bbs.save()

            return redirect('blog:bbs_detail', pk=bbs.pk)
    else:  #GETの時
        form = BbscommentForm(instance=bbs)
        #form.fields['cid'] = bbs_cid
    return render(request, 'blog/bbs_edit.html', {'form': form})


def bbs_detail(request, pk):
    bbs_comments = Bbscomment.objects.filter(bbstitle=pk)
    #request.session['bbs_return_id'] = bbs_comment.id
    context = paginator_list(request, bbs_comments, 5)
    return render(request, 'blog/bbs_detail.html', context)


@require_POST
def bbs_comment_off(request, pk):
    comment = get_object_or_404(Bbscomment, pk=pk)
    comment.is_public = False
    comment.save()
    return redirect('blog:bbs_detail', pk=comment.id)

@require_POST
def bbs_comment_on(request, pk):
    comment = get_object_or_404(Bbscomment, pk=pk)
    comment.is_public = True
    comment.save()
    return redirect('blog:bbs_detail', pk=comment.id)
