from django.views.generic import ListView, DetailView
from django.db.models import Q

from .models import SblItem


class Home(ListView):
    model = SblItem
    paginate_by = 10
    template_name = "spamhaus_sbl_parser/index.html"

    def get_queryset(self):
        items = SblItem.objects.all()
        q = self.request.GET.get('q', None)
        if q:
            q = q.strip()
            items = items.filter(
                Q(date__icontains=q) | Q(network__icontains=q) | Q(ref_name__icontains=q) | Q(domen__icontains=q) | Q(
                    ptext__icontains=q) | Q(ref_detail_text__icontains=q))
        return items

    def get_context_data(self, **kwards):
        context = super(Home, self).get_context_data(**kwards)
        q = self.request.GET.get('q', None)
        if q:
            context['q_string'] = q
        return context


class DetailSblItem(DetailView):
    model = SblItem
    template_name = "spamhaus_sbl_parser/detail.html"
