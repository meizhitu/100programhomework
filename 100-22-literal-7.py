__author__ = 'rui'
#coding=utf-8
import pygtk

pygtk.require("2.0")
import gtk
from Demo import DemoWindow
from datetime import datetime
import dateutil.tz
from lxml import etree
from feedformatter import Feed


class AtomEntry:
    def __init__(self):
        # ATOM
        # 必选
        self.atom_id = None
        self.atom_title = None
        self.atom_updated = datetime.now(dateutil.tz.tzutc())
        # 推荐
        self.atom_author = None  #[]
        self.atom_content = None
        self.atom_link = None  #[]
        self.atom_summary = None
        # 可选
        self.atom_category = None
        self.atom_contributor = None
        self.atom_published = None
        self.atom_source = None
        self.atom_rights = None

    def build_atom_entry(self, feed):
        entry = etree.SubElement(feed, 'entry')
        if not (self.atom_id and self.atom_title and self.atom_updated):
            raise ValueError('Required fields not set')
        id = etree.SubElement(entry, 'id')
        id.text = self.atom_id
        title = etree.SubElement(entry, 'title')
        title.text = self.atom_title
        updated = etree.SubElement(entry, 'updated')
        updated.text = self.atom_updated.isoformat()
        # An entry must contain an alternate link if there is no content element.
        if not self.atom_content:
            if not True in [l.get('rel') == 'alternate'
                            for l in self.atom_link or []]:
                raise ValueError('Entry must contain an alternate link or '
                                 + 'a content element.')
                # author 结点

        for a in self.atom_author or []:
            # Atom requires a name. Skip elements without.
            if not a.get('name'):
                continue
            author = etree.SubElement(entry, 'author')
            name = etree.SubElement(author, 'name')
            name.text = a.get('name')
            if a.get('email'):
                email = etree.SubElement(author, 'email')
                email.text = a.get('email')
            if a.get('uri'):
                email = etree.SubElement(author, 'url')
                email.text = a.get('uri')

        if self.atom_content:
            content = etree.SubElement(entry, 'content')
            atomtype = self.atom_content.get('type')
            if self.atom_content.get('src'):
                content.attrib['src'] = self.atom_content['src']
            elif self.atom_content.get('content'):
                # Surround xhtml with a div tag, parse it and embed it
                if atomtype == 'xhtml':
                    content.append(etree.fromstring('''<div
                                                            xmlns="http://www.w3.org/1999/xhtml">%s</div>''' %
                                                    self.atom_content.get('content')))
                # Emed the text in escaped form
                elif not atomtype or atomtype.startswith('text') or atomtype == 'html':
                    content.text = self.atom_content.get('content')
                # Parse XML and embed it
                elif atomtype.endswith('/xml') or atomtype.endswith('+xml'):
                    content.append(etree.fromstring(self.atom_content['content']))
                # Everything else should be included base64 encoded
                else:
                    raise ValueError('base64 encoded content is not supported at the moment.'
                                     + 'If you are interested , please file a bug report.')
                    # Add type description of the content
            if atomtype:
                content.attrib['type'] = atomtype

        for l in self.atom_link or []:
            link = etree.SubElement(entry, 'link', href=l['href'])
            if l.get('rel'):
                link.attrib['rel'] = l['rel']
            if l.get('type'):
                link.attrib['type'] = l['type']
            if l.get('hreflang'):
                link.attrib['hreflang'] = l['hreflang']
            if l.get('title'):
                link.attrib['title'] = l['title']
            if l.get('length'):
                link.attrib['length'] = l['length']

        if self.atom_summary:
            summary = etree.SubElement(entry, 'summary')
            summary.text = self.atom_summary
            #类别
        for c in self.atom_category or []:
            cat = etree.SubElement(feed, 'category', term=c['term'])
            if c.get('schema'):
                cat.attrib['schema'] = c['schema']
            if c.get('label'):
                cat.attrib['label'] = c['label']

                # Add contributor elements
        for c in self.atom_contributor or []:
        # Atom requires a name. Skip elements without.
            if not c.get('name'):
                continue
            contrib = etree.SubElement(feed, 'contributor')
            name = etree.SubElement(contrib, 'name')
            name.text = c.get('name')
            if c.get('email'):
                email = etree.SubElement(contrib, 'email')
                email.text = c.get('email')
            if c.get('uri'):
                email = etree.SubElement(contrib, 'url')
                email.text = c.get('uri')

        if self.atom_published:
            published = etree.SubElement(entry, 'published')
            published.text = self.atom_published.isoformat()

        if self.atom_rights:
            rights = etree.SubElement(feed, 'rights')
            rights.text = self.atom_rights
        return entry


class AtomFeed:
    def __init__(self):
        # ATOM
        self.feed_entries = []
        # http://www.atomenabled.org/developers/syndication/
        # required
        self.atom_id = None
        self.atom_title = None
        self.atom_updated = datetime.now(dateutil.tz.tzutc())
        # recommended
        self.atom_author = None  # [{name*, uri, email}]
        self.atom_link = None  # [{href*, rel, type, hreflang, title, length}]
        # optional
        self.atom_category = None  # {term*, schema, label}
        self.atom_contributor = None
        self.atom_icon = None
        self.atom_logo = None
        self.atom_rights = None
        self.atom_subtitle = None
        # other
        self.atom_feed_xml_lang = None

    def build_atom_entry(self):
        feed = etree.Element('feed', xmlns='http://www.w3.org/2005/Atom')
        if self.atom_feed_xml_lang:
            feed.attrib['{http://www.w3.org/XML/1998/namespace}lang'] = \
                self.atom_feed_xml_lang

        if not (self.atom_id and self.atom_title and self.atom_updated):
            missing = ', '.join(([] if self.atom_title else ['title']) +
                                ([] if self.atom_id else ['id']) +
                                ([] if self.atom_updated else ['updated']))
            raise ValueError('Required fields not set (%s)' % missing)

        atomid = etree.SubElement(feed, 'id')
        atomid.text = self.atom_id
        title = etree.SubElement(feed, 'title')
        title.text = self.atom_title
        updated = etree.SubElement(feed, 'updated')
        updated.text = self.atom_updated.isoformat()

        # Add author elements
        for a in self.atom_author or []:
            # Atom requires a name. Skip elements without.
            if not a.get('name'):
                continue
            author = etree.SubElement(feed, 'author')
            name = etree.SubElement(author, 'name')
            name.text = a.get('name')
            if a.get('email'):
                email = etree.SubElement(author, 'email')
                email.text = a.get('email')
            if a.get('uri'):
                email = etree.SubElement(author, 'url')
                email.text = a.get('uri')

        for l in self.atom_link or []:
            link = etree.SubElement(feed, 'link', href=l['href'])
            if l.get('rel'):
                link.attrib['rel'] = l['rel']
            if l.get('type'):
                link.attrib['type'] = l['type']
            if l.get('hreflang'):
                link.attrib['hreflang'] = l['hreflang']
            if l.get('title'):
                link.attrib['title'] = l['title']
            if l.get('length'):
                link.attrib['length'] = l['length']

        for c in self.atom_category or []:
            cat = etree.SubElement(feed, 'category', term=c['term'])
            if c.get('schema'):
                cat.attrib['schema'] = c['schema']
            if c.get('label'):
                cat.attrib['label'] = c['label']

        # Add author elements
        for c in self.atom_contributor or []:
            # Atom requires a name. Skip elements without.
            if not c.get('name'):
                continue
            contrib = etree.SubElement(feed, 'contributor')
            name = etree.SubElement(contrib, 'name')
            name.text = c.get('name')
            if c.get('email'):
                email = etree.SubElement(contrib, 'email')
                email.text = c.get('email')
            if c.get('uri'):
                email = etree.SubElement(contrib, 'url')
                email.text = c.get('uri')

        if self.atom_icon:
            icon = etree.SubElement(feed, 'icon')
            icon.text = self.atom_icon

        if self.atom_logo:
            logo = etree.SubElement(feed, 'logo')
            logo.text = self.atom_logo

        if self.atom_rights:
            rights = etree.SubElement(feed, 'rights')
            rights.text = self.atom_rights

        if self.atom_subtitle:
            subtitle = etree.SubElement(feed, 'subtitle')
            subtitle.text = self.atom_subtitle

        for entry in self.feed_entries:
            entry.build_atom_entry(feed)

        doc = etree.ElementTree(feed)

        return feed, doc


class RssFeedCreator(DemoWindow):
    def doGo(self, result):
        feed = Feed()
        feed.feed["title"] = "Test Feed"
        feed.feed["link"] = "http://code.google.com/p/feedformatter/"
        feed.feed["author"] = "Luke Maurits"
        feed.feed["description"] = "A simple test feed for feedformatter"

        item = {"title": "Test item", "link": "http://www.python.org", "description": "Python programming language",
                "guid": "1234567890"}

        feed.items.append(item)

        atomFeed = AtomFeed()
        atomFeed.atom_id = "http://code.google.com/p/feedformatter/"
        atomFeed.atom_title = "Test Feed"
        atomFeed.atom_author = [{'name': 'Luke Maurits'}]
        atomFeed.atom_link = [{'href': "http://code.google.com/p/feedformatter/", 'rel': 'self', 'type': 'text/html'}]
        atomFeed.atom_subtitle = "A simple test feed for feedformatter"
        atomEntry = AtomEntry()
        atomEntry.atom_id = "1234567890"
        atomEntry.atom_title = "Test item"
        atomEntry.atom_content = {'content': "Python programming language", 'type': 'html'}
        atomEntry.atom_link = [{'href': "http://www.python.org", 'rel': 'self', 'type': 'text/html'}]
        atomFeed.feed_entries.append(atomEntry)
        atom, doc = atomFeed.build_atom_entry()
        atomString = ('<?xml version="1.0" encoding="UTF-8" ?>\n' + etree.tostring(atom, pretty_print=True))
        print('%s\n%s' % (atomString, feed.format_atom_string(pretty=True)))
        return atomString


if __name__ == "__main__":
    creator = RssFeedCreator("RSS Feed生成", "")
    gtk.main()