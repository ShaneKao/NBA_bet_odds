__author__ = 'shane'
# -*- coding: utf-8 -*-
from pyquery import PyQuery as pyq
import urllib, urllib2
import re
import cPickle as pickle

class proxy_list(object):
    def __init__(self):
        self.__host = 'http://proxylist.hidemyass.com'
        self.__REFERER = 'http://proxylist.hidemyass.com'
        self.__headers = {'Accept': 'text/html, application/xhtml+xml, */*',
                         'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
                         'Connection': 'Keep-Alive',
                         # 'Host': __host,
                         'Referer': self.__REFERER}

    def get_proxy_list(self, page_range=15):
        __all_proxy_list =[]
        for __page in range(page_range):
            __url = 'http://proxylist.hidemyass.com/%s#listable' % __page
            __request = urllib2.Request(__url, headers=self.__headers)
            __response = urllib2.urlopen(__request)
            __the_page = __response.read()
            doc = pyq(__the_page)

            for __list_idx in doc('#listable tbody>tr')[:]:
                __tmp = doc(__list_idx).outerHtml()
                p = pyq(__tmp)
                for __j in p('style').text().split('\n'):
                   if __j.find('display:none')>0:
                      p.remove(__j.split('{')[0])

                p.remove('style')

                for __j in p('span,div'):
                   if p(__j).attr('style')=='display:none':
                      p(__j).remove()

                __proxy = {'last_update' : p('td').eq(0).text(),
                           'ip_address' : p('td').eq(1).text().replace(' ',''),
                           'port' : p('td').eq(2).text(),
                           'country' : p('td').eq(3).text(),
                           'countryIsoCode' : p('td').eq(3).attr('rel'),
                           'type': p('td').eq(6).text(),
                           'anon' : p('td').eq(7).text(),
                           'speed': ''.join( re.findall(u'\d', p('td').eq(4)('.indicator').attr('style').split(';')[0]) ),
                           'connection_time': ''.join( re.findall(u'\d', p('td').eq(4)('.indicator').attr('style').split(';')[0]) )
                           }
                print __proxy
                __all_proxy_list.append(__proxy)

        pickle.dump(__all_proxy_list, open('free_proxy_list', 'wb'))
        __all_proxy_list = pickle.load(open('free_proxy_list' , 'r'))
        return __all_proxy_list

        all_count_cnt = {}
        for __i in __all_proxy_list:
            if all_count_cnt.has_key(__i['country']):
                all_count_cnt[__i['country']] = all_count_cnt[__i['country']]+1
            else:
                all_count_cnt[__i['country']] = 1

        print all_count_cnt

        all_count_cnt = {}
        for __i in __all_proxy_list:
            if all_count_cnt.has_key(__i['countryIsoCode']):
                all_count_cnt[__i['countryIsoCode']] = all_count_cnt[__i['countryIsoCode']]+1
            else:
                all_count_cnt[__i['countryIsoCode']] = 1

        print all_count_cnt

if __name__ == "__main__":
    px = proxy_list()
    proxy_list = px.get_proxy_list()
    print proxy_list


if __name__ == "__main__xx":
    __host = 'http://proxylist.hidemyass.com'
    __REFERER = 'http://proxylist.hidemyass.com'
    __headers = {'Accept': 'text/html, application/xhtml+xml, */*',
                     'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
                     'Connection': 'Keep-Alive',
                     'Referer': __REFERER}
                 # 'Host': __host,}

    __page = 2
    __url = 'http://proxylist.hidemyass.com/%s#listable' % __page
    __request = urllib2.Request(__url, headers=__headers)
    __response = urllib2.urlopen(__request)
    __the_page = __response.read()
    doc = pyq(__the_page)



