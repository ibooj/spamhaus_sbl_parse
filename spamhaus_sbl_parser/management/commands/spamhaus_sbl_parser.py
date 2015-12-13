import socket
import socks
import requests
import leaf
import subprocess

from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext_lazy as _

from spamhaus_sbl_parser.models import SblLog, SblItem


def reload_tor():
    reload_tor_process = subprocess.Popen('/etc/init.d/tor reload', shell=True)
    while reload_tor_process.poll() is None:
        pass


def sbl_parser_log(msg):
    o = SblLog(msg=msg)
    o.save()


class Command(BaseCommand):
    help = _('Загрузка списка хостов')
    h = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0'}
    s = requests.Session()
    sbl_items = []

    def get_sbl_item(self, i):
        sbl_item = {}

        status = i.xpath('tr/td[1]/img')[0].src.replace('/images/', '').replace('.gif', '')
        if status == 'spacer':
            status = i.xpath('tr/td[last()]/div/img')[0].src.replace('/images/', '').replace('.gif', '')
        sbl_item.update({'status': status})

        date = i.xpath('tr[2]/td[1]/span')[0].text
        sbl_item.update({'date': date})

        ref = i.xpath('tr/td[2]/span')[0].get('a')
        if ref:
            sbl_item.update({'ref_href': ref.href})
            page = self.s.get('http://spamhaus.org%s' % sbl_item['ref_href'], headers=self.h)
            document = leaf.parse(page.text)
            detail_text = document.xpath('body/div/table[2]/tr[2]/td[2]')[0]
            # detail_text_data = document.xpath('body/div/table[2]/tr[2]/td[2]/table/tr[3]/td')[0]
            # sbl_item.update({'date': detail_text_data.get('span').text.replace('|', '').strip()})
            sbl_item.update({'ref_detail_text': detail_text.inner_html()})
            ref_name = ref.get('b').text
        else:
            sbl_item.update({'ref_href': None})
            ref_name = i.xpath('tr/td[2]/span/b/font')[0].text
        sbl_item.update({'ref_name': ref_name})

        network = i.xpath('tr/td[3]/span')[0].text
        sbl_item.update({'network': network})

        domen = i.xpath('tr/td[4]/span')[0].get('a').text
        sbl_item.update({'domen': domen})

        ptext = i.xpath('tr[2]/td[2]/span')[0].text
        sbl_item.update({'ptext': ptext})

        self.sbl_items.append(sbl_item)

    def get_sbl_items(self):
        try:
            page = self.s.get('http://spamhaus.org/sbl/latest/', headers=self.h)
            document = leaf.parse(page.text)
            items = document.xpath('body/div/table[2]/tr[3]/td[2]/table')
            if not items:
                raise Exception('table items not found')
            for i in items:
                try:
                    self.get_sbl_item(i)
                except Exception as e:
                    sbl_parser_log(e)
                # break
        except Exception as e:
            sbl_parser_log(e)
            reload_tor()
            self.get_sbl_items()

        for item in self.sbl_items:
            obj = SblItem.objects.get_or_create(ref_name=item['ref_name'])[0]
            for key in item:
                setattr(obj, key, item[key])
            obj.save()

    def handle(self, *args, **options):
        try:
            socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)
            socket.socket = socks.socksocket
            self.get_sbl_items()

        except Exception as e:
            raise CommandError(_('Ошибка "%s" ' % e))
