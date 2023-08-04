from django import forms

from stockapp.models import Product


class UploadProductFileForm(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", UploadProductFileForm())
        # kwargs.setdefault("verbose_name", "上传")
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        if isinstance(data, (list, tuple)):
            result = [self.clean_single_file(d, initial) for d in data]
        else:
            result = self.clean_single_file(data, initial)
        return result

    def clean_single_file(self, data, initial):
        # data.size in bytes less than 50M
        if data.size > 50000000:
            raise forms.ValidationError("File is too large.")
        if not (data.name.endswith('csv') or data.name.endswith('xls')
                or data.name.endswith('xlsx')):
            raise forms.ValidationError(str.format("文件类型不支持: {}", data.name))
        return super().clean(data, initial)


class FileFieldForm(forms.Form):
    file_field = MultipleFileField(max_length=64, allow_empty_file=False, label="上传文件")
    file_field.widget.attrs.update({"class": "form-control"})


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
