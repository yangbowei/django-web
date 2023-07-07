from django import forms

from stockapp.models import Product


class UploadProductFileForm(forms.Form):
    file = forms.FileField(allow_empty_file=False,
                           max_length=64,
                           widget=forms.ClearableFileInput(attrs={"class": "form-control"}))


class QueryTextForm(forms.Form):
    query = forms.CharField(label="", help_text="", widget=forms.Textarea)


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['brand', 'model', 'quantity', 'period', 'source']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})
