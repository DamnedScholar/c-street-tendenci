import json
import logging; logger = logging.getLogger('Cartomancer 🗺 ')

from celery import shared_task

from django.core.exceptions import ValidationError
from django.utils.text import slugify

from wagtail.core.models import Page

from lib.drone_hangar.google import directory

from .plugins import google_sheet
from .models import EntityPage, EntitiesIndexPage, AirBnBPage, APIResult

def fake_get_directory():
    data = []

    with open('lib/drone_hangar/static/google/directory.json') as f:
        data = json.loads(f.read())

    keys = [slugify(v) for v in data[0]]

    return dict(zip(keys, data))

@shared_task
def invoke(result):
    data = result.data
    # data = fake_get_directory()

    cats = set([])
    cat_objs = {}
    dump = {}
    loaded_ids = []

    if EntityPage.objects.count():
        [e.delete() for e in EntityPage.objects.all()]
    if EntitiesIndexPage.objects.count():
        [e.delete() for e in EntitiesIndexPage.objects.all()]

    try:
        root = Page.get_first_root_node()
        directory_root = EntitiesIndexPage(
            title="C-Street Directory",
            slug="directory"
            )
        root.add_child(instance=directory_root)
    except ValidationError:
        directory_root = EntitiesIndexPage.objects.get(slug="directory")

    for slug, row in data.items():
        logger.warn(repr(row))

        if not row.get('category', ''):
            continue
        
        if not row.get('name', ''):
            continue

        cat_slug = slugify(row['category'])
        if cat_slug not in cats:
            logger.warn(f"Making a new category for {cat_slug}.")
            cats.add(cat_slug)
            dump[cat_slug] = []

            cat_obj = EntitiesIndexPage(
                title=row['category'],
                slug=cat_slug
                )

            cat_objs.update({
                cat_slug: cat_obj
            })

            directory_root.add_child(instance=cat_obj)

            logger.warn(f'We made a new category object named {cat_slug}.')

        page_data = {
            'title': row['name'],
            'draft_title': '',
            'slug': slug,
            'data': row
        }

        with open('lib/cartomancer/testing/directory-dump.txt', 'a+') as f:
            f.write(f"{repr(page_data)}\n\n")

        try: dump[cat_slug].append(EntityPage(**page_data))
        except ValidationError:
            logger.warn(f"Aborted adding page. Data dump:")
            logger.warn(repr(row))

    logger.warn(f"We have data for {len(cats)} categories.")
    logger.warn(repr(dump))
    for cat in cats:
        [ cat_objs[cat].add_child(instance=entity) for entity in dump[cat] ]

        logger.warn(f"Cat {cat}: {len(dump[cat])} pages created")

    logger.warn("Everything seems to have gone alright.")
    return True

@shared_task
def conjure(source):
    data = google_sheet.call_api()

    from .models import APISource
    gsheet = APISource.objects.first()

    result = {
        "source": gsheet,
        "data": data,
        "model": "cartomancer.EntityPage"
    }

    record = APIResult(**result)

    record.save()
