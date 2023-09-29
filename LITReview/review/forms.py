from django import forms
from django.contrib.auth import get_user_model
import review.models

User = get_user_model()

CHOICES = ((1, '-1'), (2, '-2'), (3, '-3'), (4, '-4'), (5, '-5'))


class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(required=True, choices=CHOICES,
                               widget=forms.RadioSelect(attrs={'class': 'Radio'}))  # ,initial=1
    edit_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = review.models.Review
        fields = ['headline', 'body', 'rating']


class TicketForm(forms.ModelForm):
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = review.models.Ticket
        fields = ['title', 'description', 'image']


class UserFollowsForm(forms.Form):
    followed_user = forms.CharField(
        label=False,
        widget=forms.TextInput()
    )


"""username = forms.CharField(max_length=50, label=False, widget=forms.TextInput())

    def save(self, request):
        uf = review.models.UserFollows.objects.create(username=request.user)"""


class DeleteTicketForm(forms.Form):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class DeleteReviewForm(forms.Form):
    delete_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)


"""______________________________________________________"""

"""Ces champs utilisent le widget   HiddenInput   ,
et ne seront pas vus par l’utilisateur sur le front-end.
Le choix du type de champ et de la valeur initiale est quelque peu arbitraire,
vu que nous allons simplement vérifier la présence du champ dans la vue."""


