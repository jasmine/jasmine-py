from django.views.generic.base import TemplateView


class JasmineRunner(TemplateView):
    config = None

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        self.config.reload()

        js_files = self.config.script_urls()

        css_files = self.config.stylesheet_urls()

        context.update({
            'css_files': css_files,
            'js_files': js_files,
        })

        return self.render_to_response(context)
