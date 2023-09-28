from django.conf import settings
from itertools import chain
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.views.generic import View
from . import forms, models
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Value, CharField
from authentication.models import UserFollows, User

from .utils import get_user_viewable_reviews, get_user_viewable_tickets, get_replied_tickets, get_user_follows


@login_required
def my_posts(request, post_id=None):  # pk=None
    if post_id:
        user = get_object_or_404(settings.AUTH_USER_MODEL, id=post_id)
    else:
        user = request.user

    followed_users = get_user_follows(request.user)  # function utils

    reviews = models.Review.objects.filter(user=user)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    tickets = models.Ticket.objects.filter(user=user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    replied_tickets, replied_reviews = get_replied_tickets(tickets)

    posts_list = sorted(chain(reviews, tickets), key=lambda post: post.time_created, reverse=True)

    if posts_list:
        paginator = Paginator(posts_list, 5)
        page = request.GET.get('page')
        posts = paginator.get_page(page)
        total_posts = paginator.count
    else:
        posts = None
        total_posts = 0

    context = {
        'posts': posts,
        'title': f"{user.username}'s posts ({total_posts})",
        'r_tickets': replied_tickets,
        'r_reviews': replied_reviews,
        'followed_users': followed_users
    }

    return render(request, 'review/feed.html', context)


@login_required
def feed(request):
    followed_users = get_user_follows(request.user)

    reviews = get_user_viewable_reviews(request.user)
    print(reviews)
    print('_______________________________________')
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    tickets = get_user_viewable_tickets(request.user)
    print(tickets)
    #tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    replied_tickets, replied_reviews = get_replied_tickets(tickets)

    posts_list = sorted(chain(reviews, tickets), key=lambda post: post.time_created, reverse=True)

    if posts_list:
        paginator = Paginator(posts_list, 5)
        page = request.GET.get('page')
        posts = paginator.get_page(page)
    else:
        posts = None

    context = {
        'posts': posts,
        'r_tickets': replied_tickets,
        'r_reviews': replied_reviews,
        'title': 'Feed',
        'followed_users': followed_users
    }

    return render(request, 'review/feed.html', context)


class CreateTicket(View, LoginRequiredMixin):
    form_ticket_class = forms.TicketForm
    template_name = 'review/create_ticket.html'

    def get(self, request):
        ticket_form = self.form_ticket_class()
        context = {'ticket_form': ticket_form}
        return render(request, self.template_name, context=context)

    def post(self, request):
        ticket_form = self.form_ticket_class(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('flux')
        context = {'ticket_form': ticket_form}
        return render(request, self.template_name, context=context)


class CreateReview(View, LoginRequiredMixin):
    form_ticket_class = forms.TicketForm
    form_review_class = forms.ReviewForm
    template_name = 'review/create_review.html'

    def get(self, request):
        ticket_from = self.form_ticket_class()
        review_form = self.form_review_class()
        context = {'ticket_from': ticket_from,
                   'review_form': review_form}
        return render(request, self.template_name, context=context)

    def post(self, request):
        ticket_from = self.form_ticket_class(request.POST, request.FILES)
        review_form = self.form_review_class(request.POST)
        if all([review_form.is_valid(), ticket_from.is_valid()]):
            ticket = ticket_from.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect('flux')
        context = {'ticket_from': ticket_from,
                   'review_form': review_form}
        return render(request, self.template_name, context=context)


class CreateTicketReview(LoginRequiredMixin, View):
    login_url = "/login/"  # LoginRequiredMixin
    redirect_field_name = "feed"  # LoginRequiredMixin
    form_ticket_class = forms.TicketForm
    form_review_class = forms.ReviewForm
    template_name = 'review/create_ticket_review.html'

    def get(self, request, ticket_id):
        ticket = get_object_or_404(models.Ticket, id=ticket_id)
        ticket_form = self.form_ticket_class(instance=ticket)
        # ticket_from = self.form_ticket_class()
        review_form = self.form_review_class()
        context = {'ticket_form': ticket_form,
                   'review_form': review_form}
        return render(request, self.template_name, context=context)

    def post(self, request, ticket_id):
        ticket = get_object_or_404(models.Ticket, id=ticket_id)
        ticket_form = self.form_ticket_class(instance=ticket)
        # ticket_from = self.form_ticket_class(request.POST, request.FILES)
        review_form = self.form_review_class(request.POST)
        if review_form.is_valid():
            review_form.save()
            return redirect('flux')
        context = {'ticket_form': ticket_form,
                   'review_form': review_form}
        return render(request, self.template_name, context=context)


@login_required
def review_detail(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    followed_users = get_user_follows(request.user)
    context = {
        'post': review,
        'title': 'Review detail',
        'followed_users': followed_users
    }

    return render(request, 'review/post_detail.html', context)


class EditTicket(View, LoginRequiredMixin):
    form_edit_class = forms.TicketForm
    form_delete_class = forms.DeleteTicketForm
    template_name = 'blog/edit_ticket.html'

    def get(self, request, ticket_id):
        ticket = get_object_or_404(models.Ticket, id=ticket_id)
        edit_form = self.form_edit_class(instance=ticket)
        delete_form = self.form_delete_class()
        context = {
            'edit_form': edit_form,
            'delete_form': delete_form,
        }
        return render(request, self.template_name, context=context)

    def post(self, request, ticket_id):
        ticket = get_object_or_404(models.Blog, id=ticket_id)
        edit_form = self.form_edit_class(instance=ticket)
        delete_form = self.form_delete_class()

        if 'edit_blog' in request.POST:
            edit_form = self.form_edit_class(request.POST, instance=ticket)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('flux')
        if 'delete_blog' in request.POST:
            delete_form = self.form_delete_class(request.POST)
            if delete_form.is_valid():
                ticket.delete()
                return redirect('flux')
        context = {
            'edit_form': edit_form,
            'delete_form': delete_form,
        }
        return render(request, self.template_name, context=context)


class EditReview(View, LoginRequiredMixin):
    form_ticket_class = forms.TicketForm
    form_review_class = forms.ReviewForm
    template_name = 'blog/edit_review.html'

    def get(self, request, ticket_id, review_id):
        ticket = get_object_or_404(models.Ticket, id=ticket_id)
        review = get_object_or_404(models.Review, id=review_id)
        edit_ticket_form = self.form_ticket_class(instance=ticket)
        edit_review_form = self.form_review_class(instance=review)
        # delete_form = self.form_delete_class()
        context = {
            'edit_review_form': edit_review_form,
            'edit_ticket_form': edit_ticket_form,
        }
        return render(request, self.template_name, context=context)

    def post(self, request, ticket_id, review_id):
        ticket = get_object_or_404(models.Ticket, id=ticket_id)
        review = get_object_or_404(models.Review, id=review_id)
        edit_ticket_form = self.form_ticket_class(instance=ticket)
        edit_review_form = self.form_review_class(instance=review)
        # edit_form = self.form_edit_class(instance=review)
        # delete_form = self.form_delete_class()

        if 'edit_blog' in request.POST:
            edit_ticket_form = self.form_ticket_class(request.POST, instance=ticket)
            edit_review_form = self.form_review_class(request.POST, instance=review)
            if edit_review_form.is_valid():
                edit_review_form.save()
                return redirect('flux')
        context = {
            'edit_ticket_form': edit_ticket_form,
            'edit_review_form': edit_review_form,
        }
        return render(request, self.template_name, context=context)


@login_required()
def subscriptions(request):
    # subscription = models.UserFollows.objects.filter(Q(user__in=request.user.follows.all()))
    subscription = UserFollows.objects.filter(user=request.user)  # .order_by('followed_user')
    subscriber = UserFollows.objects.filter(followed_user=request.user)  # .order_by('user')
    follow_user_form = forms.UserFollowsForm()
    if request.method == "POST":
        follow_user_form = forms.UserFollowsForm(request.POST)  # username=request.POST['followed_user'])
        if follow_user_form.is_valid():
            username = follow_user_form.cleaned_data['followed_user']
            if username != f'{request.user}':
                user = User.objects.get(id=request.user.id)
                followed_user = User.objects.filter(username=username)[0]
                if followed_user is not None:
                    add_follower = UserFollows(user=user, followed_user=followed_user)
                    add_follower.save()
                else:
                    return redirect('subscriptions')
    context = {
        'follow_user_form': follow_user_form,
        'subscriber': subscriber,
        'subscription': subscription
    }
    return render(
        request,
        'review/subscriptions.html',
        context=context
    )


@login_required
def unsubscribe(request, link_id):
    link = UserFollows.objects.get(id=link_id)
    link.delete()
    return redirect('subscriptions')




