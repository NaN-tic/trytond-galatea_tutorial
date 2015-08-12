# This file is part galatea_tutorial module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from mimetypes import guess_type
from datetime import datetime
import os
import hashlib
from trytond.model import ModelSQL, ModelView, fields
from trytond.pool import Pool
from trytond.transaction import Transaction
from trytond.cache import Cache
from trytond.config import config
from trytond.modules.galatea.tools import slugify, IMAGE_TYPES, thumbly

__all__ = ['GalateaTutorial', 'GalateaTutorialWebSite', 'GalateaTutorialComment']


class GalateaTutorial(ModelSQL, ModelView):
    "Galatea Tutorial"
    __name__ = 'galatea.tutorial'
    name = fields.Char('Name', required=True, translate=True,
        on_change=['name', 'slug'])
    slug = fields.Char('slug', required=True, translate=True,
        help='Cannonical uri.')
    slug_langs = fields.Function(fields.Dict(None, 'Slug Langs'), 'get_slug_langs')
    description = fields.Text('Description', required=True, translate=True,
        help='You could write wiki markup to create html content. Formats text following '
        'the MediaWiki (http://meta.wikimedia.org/wiki/Help:Editing) syntax.')
    long_description = fields.Text('Long Description', translate=True,
        help='You could write wiki markup to create html content. Formats text following '
        'the MediaWiki (http://meta.wikimedia.org/wiki/Help:Editing) syntax.')
    metadescription = fields.Char('Meta Description', translate=True, 
        help='Almost all search engines recommend it to be shorter ' \
        'than 155 characters of plain text')
    metakeywords = fields.Char('Meta Keywords',  translate=True,
        help='Separated by comma')
    metatitle = fields.Char('Meta Title',  translate=True)
    active = fields.Boolean('Active',
        help='Dissable to not show content tutorial.')
    visibility = fields.Selection([
            ('public','Public'),
            ('register','Register'),
            ('manager','Manager'),
            ], 'Visibility', required=True)
    tutorial_create_date = fields.DateTime('Create Date', readonly=True)
    tutorial_write_date = fields.DateTime('Write Date', readonly=True)
    user = fields.Many2One('galatea.user', 'User', required=True)
    websites = fields.Many2Many('galatea.tutorial-galatea.website', 
        'tutorial', 'website', 'Websites',
        help='Tutorial will be available in those websites')
    gallery = fields.Boolean('Gallery', help='Active gallery attachments.')
    comment = fields.Boolean('Comment', help='Active comments.')
    comments = fields.One2Many('galatea.tutorial.comment', 'tutorial', 'Comments')
    total_comments = fields.Function(fields.Integer("Total Comments"),
        'get_totalcomments')
    attachments = fields.One2Many('ir.attachment', 'resource', 'Attachments')
    thumb = fields.Function(fields.Binary('Thumb', filename='thumb_filename'),
        'get_thumb', setter='set_thumb')
    thumb_filename = fields.Char('File Name',
        help='Thumbnail File Name')
    thumb_path = fields.Function(fields.Char('Thumb Path'), 'get_thumb_path')
    _slug_langs_cache = Cache('galatea_tutorial.slug_langs')

    @staticmethod
    def default_active():
        return True

    @staticmethod
    def default_visibility():
        return 'public'

    @staticmethod
    def default_websites():
        Website = Pool().get('galatea.website')
        return [p.id for p in Website.search([('registration','=',True)])]

    @staticmethod
    def default_comment():
        return True

    @classmethod
    def default_user(cls):
        Website = Pool().get('galatea.website')
        websites = Website.search([('active', '=', True)], limit=1)
        if not websites:
            return None
        website, = websites
        if website.tutorial_anonymous_user:
            return website.tutorial_anonymous_user.id
        return None

    @staticmethod
    def default_tutorial_create_date():
        return datetime.now()

    @classmethod
    def __setup__(cls):
        super(GalateaTutorial, cls).__setup__()
        cls._order.insert(0, ('tutorial_create_date', 'DESC'))
        cls._order.insert(1, ('name', 'ASC'))
        cls._error_messages.update({
            'delete_tutorials': ('You can not delete '
                'tutorials because you will get error 404 NOT Found. '
                'Dissable active field.'),
            'not_file_mime': ('Not know file mime "%(file_name)s"'),
            'not_file_mime_image': ('"%(file_name)s" file mime is not an image ' \
                '(jpg, png or gif)'),
            'image_size': ('Thumb "%(file_name)s" size is larger than "%(size)s"Kb'),
            })

    def on_change_name(self):
        res = {}
        if self.name and not self.slug:
            res['slug'] = slugify(self.name)
        return res

    @classmethod
    def write(cls, *args):
        now = datetime.now()

        actions = iter(args)
        args = []
        for photos, values in zip(actions, actions):
            values = values.copy()
            values['tutorial_write_date'] = now
            args.extend((photos, values))
        return super(GalateaTutorial, cls).write(*args)

    @classmethod
    def copy(cls, tutorials, default=None):
        new_tutorials = []
        for tutorial in tutorials:
            default['slug'] = '%s-copy' % tutorial.slug
            new_tutorial, = super(GalateaTutorial, cls).copy([tutorial], default=default)
            tutorials.append(new_tutorial)
        return new_tutorials

    @classmethod
    def delete(cls, tutorials):
        cls.raise_user_error('delete_tutorials')

    def get_slug_langs(self, name):
        'Return dict slugs for each active languages'
        pool = Pool()
        Lang = pool.get('ir.lang')
        Tutorial = pool.get('galatea.tutorial')

        tutorial_id = self.id
        langs = Lang.search([
            ('active', '=', True),
            ('translatable', '=', True),
            ])

        slugs = {}
        for lang in langs:
            with Transaction().set_context(language=lang.code):
                tutorial, = Tutorial.read([tutorial_id], ['slug'])
                slugs[lang.code] = tutorial['slug']

        return slugs

    def get_totalcomments(self, name):
        return len(self.comments)

    def get_thumb(self, name):
        db_name = Transaction().cursor.dbname
        filename = self.thumb_filename
        if not filename:
            return None
        filename = os.path.join(config.get('database', 'path'), db_name,
            'galatea', 'tutorial', filename[0:2], filename[2:4], filename)

        value = None
        try:
            with open(filename, 'rb') as file_p:
                value = fields.Binary.cast(file_p.read())
        except IOError:
            pass
        return value

    def get_thumb_path(self, name):
        filename = self.thumb_filename
        if not filename:
            return None
        return '%s/%s/%s' % (filename[:2], filename[2:4], filename)

    @classmethod
    def set_thumb(cls, tutorials, name, value):
        if value is None:
            return

        Config = Pool().get('galatea.configuration')
        galatea_config = Config(1)
        size = galatea_config.tutorial_thumb_size or 300
        crop = galatea_config.tutorial_thumb_crop
        db_name = Transaction().cursor.dbname
        galatea_dir = os.path.join(
            config.get('database', 'path'), db_name, 'galatea', 'tutorial')

        for tutorial in tutorials:
            file_name = tutorial['thumb_filename']

            file_mime, _ = guess_type(file_name)
            if not file_mime:
                cls.raise_user_error('not_file_mime', {
                        'file_name': file_name,
                        })
            if file_mime not in IMAGE_TYPES:
                cls.raise_user_error('not_file_mime_image', {
                        'file_name': file_name,
                        })

            _, ext = file_mime.split('/')
            digest = '%s.%s' % (hashlib.md5(value).hexdigest(), ext)
            subdir1 = digest[0:2]
            subdir2 = digest[2:4]
            directory = os.path.join(galatea_dir, subdir1, subdir2)
            filename = os.path.join(directory, digest)

            thumb = thumbly(directory, filename, value, size, crop)
            if not thumb:
                cls.raise_user_error('not_file_mime_image', {
                        'file_name': file_name,
                        })
            cls.write([tutorial], {
                'thumb_filename': digest,
                })


class GalateaTutorialWebSite(ModelSQL):
    'Galatea Tutorial - Website'
    __name__ = 'galatea.tutorial-galatea.website'
    _table = 'galatea_tutorial_galatea_website'
    tutorial = fields.Many2One('galatea.tutorial', 'Tutorial', ondelete='CASCADE',
            select=True, required=True)
    website = fields.Many2One('galatea.website', 'Website', ondelete='RESTRICT',
            select=True, required=True)


class GalateaTutorialComment(ModelSQL, ModelView):
    "Galatea Tutorial Comment"
    __name__ = 'galatea.tutorial.comment'
    tutorial = fields.Many2One('galatea.tutorial', 'Tutorial', required=True)
    user = fields.Many2One('galatea.user', 'User', required=True)
    description = fields.Text('Description', required=True,
        help='You could write wiki markup to create html content. Formats text following '
        'the MediaWiki (http://meta.wikimedia.org/wiki/Help:Editing) syntax.')
    active = fields.Boolean('Active',
        help='Dissable to not show content tutorial.')
    comment_create_date = fields.DateTime('Create Date', readonly=True)

    @classmethod
    def __setup__(cls):
        super(GalateaTutorialComment, cls).__setup__()
        cls._order.insert(0, ('create_date', 'DESC'))
        cls._order.insert(1, ('id', 'DESC'))

    @staticmethod
    def default_active():
        return True

    @classmethod
    def default_user(cls):
        Website = Pool().get('galatea.website')
        websites = Website.search([('active', '=', True)], limit=1)
        if not websites:
            return None
        website, = websites
        if website.tutorial_anonymous_user:
            return website.tutorial_anonymous_user.id
        return None

    @staticmethod
    def default_comment_create_date():
        return datetime.now()

    @classmethod
    def copy(cls, comments, default=None):
        default['comment_create_date'] = datetime.now()
        return super(GalateaTutorialComment, cls).copy(comments, default=default)
