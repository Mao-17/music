from django import forms
from .models import MusicFile

class MusicFileForm(forms.ModelForm):
    class Meta:
        model = MusicFile
        fields = ['title', 'file', 'access', 'allowed_users']
        widgets = {
            'allowed_users': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_allowed_users(self):
        data = self.cleaned_data['allowed_users']
        emails = data.strip().split('\n')
        users = []
        for email in emails:
            try:
                user = User.objects.get(email=email)
                users.append(user)
            except User.DoesNotExist:
                pass
        return users
