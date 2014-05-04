"""Looks for classic microformats class names and augments them with
microformats2 names. Ported and adapted from php-mf2.
"""

# Classic Root Classname map
CLASSIC_ROOT_MAP = {
    'vcard': 'h-card',
    'hfeed': 'h-feed',
    'hentry': 'h-entry',
    'hrecipe': 'h-recipe',
    'hresume': 'h-resume',
    'hevent': 'h-event',
    'hreview': 'h-review'
}

CLASSIC_PROPERTY_MAP = {
    'vcard': {
        'fn': ['p-name'],
        'url': ['u-url'],
        'honorific-prefix': ['p-honorific-prefix'],
        'given-name': ['p-given-name'],
        'additional-name': ['p-additional-name'],
        'family-name': ['p-family-name'],
        'honorific-suffix': ['p-honorific-suffix'],
        'nickname': ['p-nickname'],
        'email': ['u-email'],
        'logo': ['u-logo'],
        'photo': ['u-photo'],
        'url': ['u-url'],
        'uid': ['u-uid'],
        'category': ['p-category'],
        'adr': ['p-adr', 'h-adr'],
        'extended-address': ['p-extended-address'],
        'street-address': ['p-street-address'],
        'locality': ['p-locality'],
        'region': ['p-region'],
        'postal-code': ['p-postal-code'],
        'country-name': ['p-country-name'],
        'label': ['p-label'],
        'geo': ['p-geo', 'h-geo'],
        'latitude': ['p-latitude'],
        'longitude': ['p-longitude'],
        'tel': ['p-tel'],
        'note': ['p-note'],
        'bday': ['dt-bday'],
        'key': ['u-key'],
        'org': ['p-org'],
        'organization-name': ['p-organization-name'],
        'organization-unit': ['p-organization-unit'],
    },
    'hentry': {
        'entry-title': ['p-name'],
        'entry-summary': ['p-summary'],
        'entry-content': ['e-content'],
        'published': ['dt-published'],
        'updated': ['dt-updated'],
        'author': ['p-author', 'h-card'],
        'category': ['p-category'],
        'geo': ['p-geo', 'h-geo'],
        'latitude': ['p-latitude'],
        'longitude': ['p-longitude'],
    },
    'hrecipe': {
        'fn': ['p-name'],
        'ingredient': ['p-ingredient'],
        'yield': ['p-yield'],
        'instructions': ['e-instructions'],
        'duration': ['dt-duration'],
        'nutrition': ['p-nutrition'],
        'photo': ['u-photo'],
        'summary': ['p-summary'],
        'author': ['p-author', 'h-card'],
    },
    'hresume': {
        'summary': ['p-summary'],
        'contact': ['h-card', 'p-contact'],
        'education': ['h-event', 'p-education'],
        'experience': ['h-event', 'p-experience'],
        'skill': ['p-skill'],
        'affiliation': ['p-affiliation', 'h-card'],
    },
    'hevent': {
        'dtstart': ['dt-start'],
        'dtend': ['dt-end'],
        'duration': ['dt-duration'],
        'description': ['p-description'],
        'summary': ['p-summary'],
        'description': ['p-description'],
        'url': ['u-url'],
        'category': ['p-category'],
        'location': ['h-card'],
        'geo': ['p-location h-geo'],
    },
    'hreview': {
        'summary': ['p-name'],
        'fn': ['p-item', 'h-item', 'p-name'],  # doesn’t work properly, see spec
        'photo': ['u-photo'],  # of the item being reviewed (p-item h-item u-photo)
        'url': ['u-url'],  # of the item being reviewed (p-item h-item u-url)
        'reviewer': ['p-reviewer', 'p-author', 'h-card'],
        'dtreviewed': ['dt-reviewed'],
        'rating': ['p-rating'],
        'best': ['p-best'],
        'worst': ['p-worst'],
        'description': ['p-description'],
    }
}


def apply_rules(doc):
    """add modern classnames for older mf classnames

    modifies BeautifulSoup document in-place
    """

    def update_child_properties(parent, properties):
        for child in parent.find_all(recursive=False):
            child_class = child.get('class')
            for old_prop, new_props in properties.items():
                if child_class and old_prop in child_class:
                    for new_prop in new_props:
                        if new_prop not in child_class:
                            child_class.append(new_prop)

            # recurse if it's not a nested root
            if not any(cls in CLASSIC_ROOT_MAP
                       for cls in child.get('class', [])):
                update_child_properties(child, properties)

    for old_root, new_root in CLASSIC_ROOT_MAP.items():
        for el in doc.find_all(lambda el: old_root in el.get('class', [])
                               and new_root not in el.get('class', [])):
            el['class'].append(new_root)

    for old_root, properties in CLASSIC_PROPERTY_MAP.items():
        for el in doc.find_all(class_=old_root):
            update_child_properties(el, properties)
