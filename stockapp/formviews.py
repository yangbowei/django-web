from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic.edit import FormView
from .forms import FileFieldForm
from . import processor


class FileFieldFormView(FormView):
    form_class = FileFieldForm
    template_name = "add_products.html"  # Replace with your template.
    success_url = 'product/batch-add/'  # Replace with your URL or reverse().

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            # return self.form_valid(form)
            files = form.cleaned_data["file_field"]
            for file in files:
                success, result_msg = processor.process_excel_file(file.name, file.size, file.file)
                if success:
                    m = str.format('成功导入{}条数据，文件："{}"', result_msg, file.name)
                    messages.success(request, m)
                else:
                    m = str.format('导入失败，原因：{}。文件："{}"', result_msg, file.name)
                    messages.error(request, m)
            return redirect(request.META['HTTP_REFERER'])
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # files = form.cleaned_data["file_field"]
        # for file in files:
        return super().form_valid()
