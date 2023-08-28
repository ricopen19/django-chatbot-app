from django import forms


class MyForm(forms.Form):
    input_data = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'size': 100}),
        required=False,
        label="入力",
    )


class UploadForm(forms.Form):
    file = forms.FileField(label="", required=False)
