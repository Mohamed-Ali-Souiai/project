from pprint import pprint

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from review.models import Review, Ticket
from authentication.models import User, UserFollows


def get_user_follows(user):
    """Returns list of users followed by current user"""
    follows = UserFollows.objects.filter(user=user)
    followed_users = []
    for follow in follows:
        followed_users.append(follow.followed_user)
    followed_users.append(user)
    return followed_users


def get_user_viewable_reviews(user):
    """
    All viewable reviews for user feed:
    Reviews by followed users + current user
    Reviews to current user tickets if review author is not followed

    @param user: currently logged-in User instance
    @return: filtered reviews queryset with no duplicate results
    """
    followed_users = get_user_follows(user)

    reviews = []
    all_reviews = Review.objects.filter(user__in=followed_users)  # .distinct()
    for review in all_reviews:
        reviews.append(review.id)

    user_tickets = Ticket.objects.filter(user=user)
    for ticket in user_tickets:
        review_responses = Review.objects.filter(ticket=ticket)
        for review in review_responses:
            reviews.append(review.id)

    reviews = Review.objects.filter(id__in=reviews).distinct()
    print(reviews)

    return reviews


def get_user_viewable_tickets(user):
    followed_users = get_user_follows(user)
    tickets = []
    for user in followed_users:
        tickets_by_user = Ticket.objects.filter(user=user)
        for ticket in tickets_by_user:
            tickets.append(ticket)
    return tickets


def get_replied_tickets(tickets):
    """
    Get tickets with review response
    Get corresponding review to link to for detail view

    @param tickets: user tickets queryset
    @return: list of tickets with response, list of review responses to corresponding tickets
    """
    replied_tickets = []
    replied_reviews = []

    for ticket in tickets:
        try:
            replied = Review.objects.get(ticket=ticket)
            if replied:
                replied_tickets.append(replied.ticket)
                replied_reviews.append(replied)

        except Review.DoesNotExist:
            pass

    return replied_tickets, replied_reviews



