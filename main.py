import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

import django
django.setup()

import random

from datacenter.models import Commendation
from datacenter.models import Lesson
from datacenter.models import Schoolkid


commendations = [
    'Молодец!',
    'Отлично!',
    'Хорошо!',
    'Гораздо лучше, чем я ожидал!',
    'Ты меня приятно удивил!',
    'Великолепно!',
    'Прекрасно!',
    'Ты меня очень обрадовал!',
    'Именно этого я давно ждал от тебя!',
    'Сказано здорово – просто и ясно!',
    'Ты, как всегда, точен!',
    'Очень хороший ответ!',
    'Талантливо!',
    'Ты сегодня прыгнул выше головы!',
    'Я поражен!',
    'Уже существенно лучше!',
    'Потрясающе!',
    'Замечательно!',
    'Прекрасное начало!',
    'Так держать!',
    'Ты на верном пути!',
    'Здорово!',
    'Это как раз то, что нужно!',
    'Я тобой горжусь!',
    'С каждым разом у тебя получается всё лучше!',
    'Мы с тобой не зря поработали!',
    'Я вижу, как ты стараешься!',
    'Ты растешь над собой!',
    'Ты многое сделал, я это вижу!',
    'Теперь у тебя точно все получится!'
]

def fix_marks(name):
    schoolkid = Schoolkid.objects.get(full_name__contains=name)
    schoolkid.mark_set.filter(points__lte=3).update(points=5)
    return


def remove_chastisements(name):
    schoolkid = Schoolkid.objects.get(full_name__contains=name)
    schoolkid.chastisement_set.all().delete()
    return


def create_commendation(name, subject):
    schoolkid = Schoolkid.objects.get(full_name__contains=name)
    year_of_study = schoolkid.year_of_study
    group_letter = schoolkid.group_letter

    text = random.choice(commendations)

    lessons = Lesson.objects.filter(
        subject__title__contains=subject,
        group_letter=group_letter,
        year_of_study=year_of_study
    ).order_by('date')
    for lesson in lessons:
        if not lesson.subject.commendation_set.filter(
            schoolkid=schoolkid,
            created=lesson.date
        ):
            c = Commendation.objects.create(
                text=text,
                created=lesson.date,
                schoolkid=schoolkid,
                subject=lesson.subject,
                teacher=lesson.teacher
            )
            print(c.text)
            break


def main():
    create_commendation("Фролов Иван", "Музыка")


if __name__ == '__main__':
    main()
