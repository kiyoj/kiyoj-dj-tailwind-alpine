from django.db.models import Count, Q

from blog.models import Link, Category, Post, Bbstitle, Bbscomment
import random

def common(request):
    context = {
        'side_links': Link.objects.all().order_by('created_at'),
        'side_category': Category.objects.all().order_by('created_at'),
        'random_text': str(random.randint(10000, 100000)),
        #'side_bbstitle': Bbstitle.objects.all().order_by('created_at'),
        #'side_newbbstitle': Newbbsmain.objects.all().order_by('-created_at'),
        #'side_items': Items.objects.all().order_by('-createAt'),
        #'item_comments': Blogcomments.objects.filter(comment_show_flg=True),
        #'fzug_mains': Bbsmain.objects.all().order_by('mid'),
        #'bbs_mains': Newbbsmain.objects.all().order_by('mid'),
        'side_bbstitles': Bbstitle.objects.annotate(
            num_posts=Count('bbscomment', filter=Q(bbscomment__is_public=True))),

    }
    return context