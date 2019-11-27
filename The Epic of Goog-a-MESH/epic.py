#!/usr/bin/env python3.6

import json
import random
import string

REGIONS = [
    {
        "name": "the world",
        "parent": None,
        "champion": "Goog-a-MESH",
        "tense": "is",
    },
    {
        "name": "the lands of the north",
        "parent": "the world",
        "champion": "App-ul-MESH",
        "tense": "was",
    },

    {
        "name": "the lands of the west",
        "parent": "the world",
        "champion": "Amz-un-MESH",
        "tense": "was",
    },
    {
        "name": "the lands of the east",
        "parent": "the world",
        "champion": "Mikro-MESH",
        "tense": "was",
    },
    {
        "name": "the lands of the south",
        "parent": "the world",
        "champion": "MESH-buyuk",
        "tense": "was",
    },
]


def find_region(region_name):
    return [v for v in REGIONS if v['name'] == region_name][0]


def contained_regions(region_name):
    return [v for v in REGIONS if v['parent'] == region_name]


def random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length)).capitalize()


def random_c1():
    return random.choice([
        'b', 'cr', 'cl', 'd', 'f', 'gh', 'gl', 'gr', 'hr', 'zh',
    ])

def random_c2():
    return random.choice([
        'c', 'd', 'f', 'gh', 'r', 't', 'v', 'z',
    ])

def random_v1():
    return random.choice([
        'a', 'ai', 'e', 'o', 'u', 'uu',
    ])


def random_name():
    return ''.join(
        [
            random_c1().capitalize(),
            random_v1(),
            random_c1(),
            random_v1(),
            random_c2()
        ]
    )


def random_monster_name():
    return random_string(8)


def random_champion_name():
    return random_name()


def random_region_name():
    return random_name()


def random_city_name():
    return ''.join(
        [
            random_c1().capitalize(),
            random_v1(),
            random_c1(),
            random_v1(),
            '-',
            random.choice(['ulu', 'uk', 'aruk', 'ayuk'])
        ]
    )


def vanquished():
    return random.choice(['vanquished', 'subdued', 'crushed', 'overcame', 'quelled', 'put down', 'smote',])


def join_and(segs):
    if len(segs) == 0:
        return 'something'
    if len(segs) == 1:
        return segs[0]
    return ', '.join(segs[:-1]) + ' and ' + segs[-1]


def indef(noun):
    return '{} {}'.format('an' if noun.upper().startswith(('A', 'E', 'I', 'O', 'U')) else 'a', noun)


ANIMALS = [
    'bear', 'goat', 'lion', 'tiger', 'eagle', 'horse', 'boar', 'serpent',
    'weasel', 'badger', 'ox', 'bull',
]


def base_monster():
    a = random.choice([
        'Irrationally', 'Indefatigably', 'Impressively', 'Extremely', 'Excessively', 'Superlatively',
        'Ominously', 'Consummately', 'Supremely', 'Terribly', 'Hideously', 'Monumentally',
        'Overwhelmingly', 'Horridly', 'Interminably', 'Astonishingly', 'Incredibly', 'Remarkably',
    ])
    b = random.choice([
        'Strong', 'Fearsome', 'Frightful', 'Intimidating', 'Scary', 'Powerful', 'Imposing',
        'Hideous', 'Deadly', 'Cruel', 'Savage', 'Noxious',
    ])
    c = random.choice(ANIMALS).capitalize()
    return '{}, the {} {} {}-thing of {}'.format(
        random_monster_name(), a, b, c, random_region_name()
    )

def monster():
    m = base_monster()
    animals = random.sample(ANIMALS, 2)
    m += ", with the head of {} and the tail of {}".format(indef(animals[0]), indef(animals[1]))

    parts = random.sample([
        "hide was",
        "teeth were",
        "eyes were",
        "feathers were",
        "horns were",
        "claws were",
        "jaws were",
        "scales were",
        "breath was",
        "tongue was",
    ], 2)
    elements = random.sample([
        "fire", "ice", "stone", "iron", "steel", "lightning", "thunder",
        "poison",
        "the searing sun", "the blistering wind", "the pummelling hail",
    ], 2)

    for n in range(0, 2):
        m += ", {}whose {} like {}".format(
            'and ' if n > 0 else '',
            parts[n], elements[n],
        )
    return m


def renown(k):
    return random.sample([
        "do the bards not sing of how",
        "do the rhymes of the poets not tell us how",
        "is it not written on the tablets in the Temple of " + random_region_name() + " how",
        "is it not painted in the frescoes of the Hall of " + random_region_name() + " how",
        "is it not always on the lips of the schoolchildren how",
        "is it not whispered among fishwives in the marketplace how",
        "do the warriors not know by heart the tale of how",
    ], k)


def exploit(intro, rhetoric, region):
    return "{} {} {} {} {}?\n\n".format(
        intro, rhetoric, region['champion'], vanquished(), monster()
    )


def verse(region_name, chain):
    queue = []

    region = find_region(region_name)

    intro = random.choice(["Yea, and let", "And let"]) if chain else "Let"

    x = ''
    x += "{} it not be doubted that {} {} the mightiest of all in {}.\n\n".format(
        intro, region['champion'], region['tense'], region_name
    )

    subs = contained_regions(region_name)

    if len(subs) > 0:

        # Recursive case

        for i, sub in enumerate(subs):
            x += "{} is it not true that {} {} {}, the mightiest of all in {}?\n\n".format(
                "For" if i == 0 else "And", region['champion'], 'defeated', sub['champion'], sub['name']
            )

            queue.append(sub['name'])

        x += "And is it not true that there is no more to {} than {}?\n\n".format(
            region_name, join_and([sub['name'] for sub in subs])
        )

    else:

        # Base case
        rhetorics = renown(3)
        x += exploit("For", rhetorics[0], region)
        x += exploit("And", rhetorics[1], region)
        x += exploit("And", rhetorics[2], region)

    x += "Therefore let it not be doubted that {} {} the mightiest of all in {}.\n\n".format(
        region['champion'], region['tense'], region_name
    )
    last_one = region['champion']

    for (champion, tense, domain) in chain:
        x += "And therefore let it not be doubted that {}, vanquisher of {}, {} the mightiest of all in {}.\n\n".format(
            champion, last_one, tense, domain
        )
        last_one = champion

    # x += "- - - -\n\n"

    for name in queue:
        x += verse(name, [(region['champion'], region['tense'], region_name)] + chain)

    return x


def create_subregion(region_name, type_):
    if type_ == 'geo':
        adj = random.choice([
            "Grey", "Terrible", "Unending", "Sprawling",
            "Madness-inducing", "Vast", "Misty", "Dank", "Blasted",
            "Inhospitable", "Barren", "Bleak", "Desolate", "Hostile",
            "Stark", "Windswept", "Wicked",
        ])
        geo = random.choice([
            "Wastes", "Deserts", "Jungles", "Plains", "Valleys", "Mountains", "Forests", "Steppes", "Marshes", "Swamps",
        ])
        name = "the {} {} of {}".format(adj, geo, random_region_name())
    elif type_ == 'provinces':
        name = "the {} of {}".format(random.choice(["Province"]), random_region_name())
    elif type_ == 'cities':
        name = "the {} of {}".format(random.choice(["City", "Villages", "Settlements"]), random_city_name())
    elif type_ == 'houses':
        name = "the House of {}".format(random_city_name())
    else:
        raise NotImplementedError

    champion_adj = random.choice([
        "Repulsive", "Terrible", "Intimidating", "Berserk", "Mad", "Vengeful", "Oppressive", "Wrathful",
        "Magnificent", "Agile",
    ])
    return {
        "name": name,
        "parent": region_name,
        "champion": "{} the {}".format(random_champion_name(), champion_adj),
        "tense": "was",
    }


def create_subregions(region_names, num, type_):
    created_subregion_names = []
    for region_name in region_names:
        for i in range(num):
            subregion = create_subregion(region_name, type_)
            created_subregion_names.append(subregion['name'])
            REGIONS.append(subregion)
    return created_subregion_names


def main(args):
    random.seed(12345)

    region_names = [r['name'] for r in REGIONS if r['name'] != "the world"]

    subregion_names = create_subregions(region_names, 4, 'geo')
    subsubregion_names = create_subregions(subregion_names, 3, 'provinces')
    subsubsubregion_names = create_subregions(subsubregion_names, 3, 'cities')

    if '--dump' in args:
        print(json.dumps(REGIONS, indent=4))
        return

    print("# The Epic of Goog-a-MESH")
    print("")
    print("### Art in the Age of Quantum Supremacy Meets Proof in the Age of Oral Tradition")
    print("")
    print("- - - -\n\n")
    print("")

    r = verse("the world", [])
    print(r)


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
