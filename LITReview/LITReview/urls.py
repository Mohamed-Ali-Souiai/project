from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView)
import authentication.views
import review.views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(
        template_name='authentication/login.html',
        redirect_authenticated_user=True
    ), name='login_page'),
    path('change-password/', PasswordChangeView.as_view(
        template_name='authentication/password_change_form.html'),
         name='password_change'
         ),
    path('logout/', authentication.views.logout_user, name='logout'),
    path('signup/', authentication.views.SignupPage.as_view(), name='signup'),
    path('flux/', review.views.feed, name='flux'),
    path('LITReview/subscriptions', review.views.subscriptions, name='subscriptions'),
    path('subscriptions/unsub/<int:id>/', review.views.unsubscribe, name='unsub'),
    path('LITReview/create_ticket', review.views.CreateTicket.as_view(), name='create_ticket'),
    path('LITReview/create_review', review.views.CreateReview.as_view(), name='create_review'),
    path('review/response/<int:review_id>', review.views.review_detail, name='response_review'),  # à faire
    path('posts/', review.views.my_posts, name='posts'),
    path(
        'LITReview/<int:ticket_id>/<int:review_id>/edit_review',
        review.views.EditReview.as_view(), name='edit_review'
         ),
    path('LITReview/<int:ticket_id>/edit_ticket', review.views.EditTicket.as_view(), name='edit_ticket'),
    path('LITReview/<int:ticket_id>/create_ticket_review',
         review.views.CreateTicketReview.as_view(),
         name='create_ticket_review'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#    path('LITReview/post', review.views.view_post, name='view_post'),
#    path('LITReview/follow_users', review.views.FollowUsers.as_view(), name='follow-users'),

