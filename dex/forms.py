from django import forms

from pagedown.widgets import PagedownWidget

from django.forms.extras.widgets import SelectDateWidget

from .models import Org


class OrgForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrgForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.name is not None:
            self.fields['entity_name'].widget.attrs['readonly'] = True
        if instance.short_name is not None:
            self.fields['short_name'].widget.attrs['readonly'] = True
        if instance.website is not None:
            self.fields['website'].widget.attrs['readonly'] = True
        if instance.city is not None:
            self.fields['city_str'].widget.attrs['readonly'] = True
        if instance.zip_code is not None:
            self.fields['zip_code'].widget.attrs['readonly'] = True
        if instance.phone_number is not None:
            self.fields['phone_number'].widget.attrs['readonly'] = True
        if instance.email_address is not None:
            self.fields['email_address'].widget.attrs['readonly'] = True
        if instance.facebook is not None:
            self.fields['facebook'].widget.attrs['readonly'] = True
        if instance.twitter is not None:
            self.fields['twitter'].widget.attrs['readonly'] = True
        if instance.notes is not None:
            self.fields['notes'].widget.attrs['readonly'] = True

    name = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    class Meta:
        model = Org
        fields = [
            "name",
            "short_name",
            "website",
            "city_str",
            "zip_code",
            "phone_number",
            "email_address",
            "facebook",
            "twitter",
            "tags",
            "notes",
        ]


class NewOrgForm(forms.ModelForm):
    class Meta:
        model = Org
        fields = [
            "name",
            "short_name",
            "website",
            "city_str",
            "zip_code",
            "phone_number",
            "email_address",
            "facebook",
            "twitter",
            "tags",
            "notes",
        ]



class OrgAdminForm(forms.ModelForm):
    class Meta:
        model = Org
        exclude = ['slug', 'twt_followers', 'twt_following', 'twt_user_id', 'twt_user_desc', 'twt_verified', 'industry',]



# class CountryCheckList(forms.Form):
#     REGION = ('MAJOR', 'MENA', 'LA', 'SEA', 'EUR',)
#
#     country = forms.CharField(max_length=75)
#     region = models.CharField(max_length=25, choices=ACTOR)
