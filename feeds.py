#!/usr/bin/env python
# -*- coding: utf-8 -*-

feeds = [


    ['https://www.bielertagblatt.ch/taxonomy/term/18/feed', 'Bieler Tagblatt'],
    ['https://www.schweizerbauer.ch/rss/politik-wirtschaft-p-57.xml', 'Schweizer Bauer'],
    ['https://www.luzernerzeitung.ch/schweiz.rss', 'Luzerner Zeitung'],
    ['https://www.infosperber.ch/inc/rss.cfm', 'Infosperber'],
    ['https://api.20min.ch/rss/view/63', '20 Minuten'],
    ['https://www.woz.ch/t/schweiz/feed', 'Die Wochenzeitung'],

    # SCHWEIZ
    ['https://api.20min.ch/rss/view/63', '20 Minuten'],
    ['http://www.blick.ch/news/schweiz/rss.xml', 'Blick'],
    ['http://www.nzz.ch/schweiz.rss', 'Neue Zürcher Zeitung'],
    ['http://www.tagesanzeiger.ch/schweiz/rss.html', 'Tages Anzeiger'],
    ['http://www.srf.ch/news/bnf/rss/1890', 'SRF'],
    ['http://www.derbund.ch/schweiz/rss.html', 'Der Bund'],
    #['http://www.bernerzeitung.ch/schweiz/rss.html', 'Berner Zeitung'],
    ['http://bazonline.ch/schweiz/rss.html', 'Basler Zeitung'],
    ['http://www.tagblatt.ch/schweiz.rss', 'St. Galler Tagblatt'],

    # BERN
    ['http://www.derbund.ch/bern/rss.html', 'Der Bund'],
    #['http://www.bernerzeitung.ch/region/bern/rss.html', 'Berner Zeitung'],

    # BASEL
    ['http://bazonline.ch/basel/rss.html', 'Basler Zeitung'],

    # ZÜRICH
    ['http://www.nzz.ch/zuerich.rss', 'Neue Zürcher Zeitung'],
    ['http://www.tagesanzeiger.ch/zuerich/rss.html', 'Tages Anzeiger'],

    # ST. GALLEN
    ['https://www.tagblatt.ch/ostschweiz/stgallen.rss', 'St. Galler Tagblatt'],

    # ZENTRALSCHWEIZ
    #['http://www.luzernerzeitung.ch/storage/rss/rss/zentralschweiz.xml', 'Neue Luzerner Zeitung'],


    # 20min international
    # 'http://www.20min.ch/rss/rss.tmpl?type=rubrik&get=3',

    # 20min wirtschaft und boerse
    # 'http://www.20min.ch/rss/rss.tmpl?type=channel&get=8',

    # 20min news
    # 'http://www.20min.ch/rss/rss.tmpl?type=channel&get=4',

    # 20min frontpage
    # 'http://www.20min.ch/rss/rss.tmpl?type=channel&get=1',

    # nzz international
    # 'http://www.nzz.ch/aktuell/international.rss',

    # nzz wirtschaft
    # 'http://www.nzz.ch/aktuell/wirtschaft/uebersicht.rss',

    # nzz wissenschaft
    # 'http://www.nzz.ch/wissen/uebersicht.rss',

    # tagesanzeiger front
    # 'http://www.tagesanzeiger.ch/rss.html',

    # tagesanzeiger ausland
    # 'http://www.tagesanzeiger.ch/ausland/rss.html',

    #  tagesanzeiger wirtschaft
    # 'http://www.tagesanzeiger.ch/wirtschaft/rss.html',

    # weltwoche online-exlusiv
    # 'http://weltwoche.ch/rss/online-exklusiv.html',

    # srf international
    # 'http://www.srf.ch/news/bnf/rss/1922',

    # srf wirtschaft
    # 'http://www.srf.ch/news/bnf/rss/1926',

    # arf panorama
    # 'http://www.srf.ch/news/bnf/rss/1930',

    # srf technik
    # 'http://www.srf.ch/wissen/bnf/rss/8354',

    # srf digital
    # 'http://www.srf.ch/wissen/bnf/rss/8314',

    # srf mensch
    # 'http://www.srf.ch/wissen/bnf/rss/8326',

    # srf natur
    # 'http://www.srf.ch/wissen/bnf/rss/8338',

    # Der Bund Front
    # 'http://www.derbund.ch/rss.html',

    # Der Bund Ausland
    # 'http://www.derbund.ch/ausland/rss.html',

    # Der Bund Wirschaft
    # 'http://www.derbund.ch/wirtschaft/rss.html',

    # Der Bund Digital
    # 'http://www.derbund.ch/digital/rss.html',

    # Basler Zeitung
    # 'http://bazonline.ch/rss.html',

    # Basler Zeitung Ausland
    # 'http://bazonline.ch/ausland/rss.html',

    # Basler Zeitung Schweiz
    # 'http://bazonline.ch/wirtschaft/rss.html',

    # Basler Zeitung Digital
    # 'http://bazonline.ch/digital/rss.html',

    # Blick News
    # 'http://www.blick.ch/news/rss.xml',

    # Blick Ausland
    # 'http://www.blick.ch/news/ausland/rss.xml',

    # Blick Wirtschaft
    # 'http://www.blick.ch/news/wirtschaft/rss.xml',

    # Blick Wissen
    # 'http://www.blick.ch/news/wissenschaftundtechnik/rss.xml',

    # St. Galler Tagblatt International
    # 'http://www.tagblatt.ch/storage/rss/rss/' +
    # 'nachrichten-politik-international.xml',

    # St. Galler Tagblatt Wirtschaft
    # 'http://www.tagblatt.ch/storage/rss/rss/nachrichten-wirtschaft.xml',
]

def get_feed_name(feed_url):
    for feed in feeds:
        if feed[0] == feed_url:
            return feed[1]
    return None
