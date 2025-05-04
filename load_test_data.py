#!/usr/bin/env python
# load_test_data.py

import os
import django
import random
from django.db import transaction

# Django settings modulini o'rnatish
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'corruptino.settings')
django.setup()

# Modellarni import qilish
from django.contrib.auth import get_user_model
from accounts.models import EmployerProfile, CandidateProfile
from jobs.models import JobCategory, JobVacancy, TestQuestion, TestOption

User = get_user_model()

# Testlar uchun ma'lumotlar
JOB_CATEGORIES = [
    {"name": "Davlat boshqaruvi", "description": "Davlat idoralari va boshqaruv organlari uchun vakansiyalar"},
    {"name": "Ta'lim", "description": "Maktab, kollej, universitet va boshqa ta'lim muassasalari uchun vakansiyalar"},
    {"name": "Sog'liqni saqlash", "description": "Tibbiyot va sog'liqni saqlash sohasidagi vakansiyalar"},
    {"name": "IT va dasturlash", "description": "Axborot texnologiyalari sohasidagi mutaxassislar uchun vakansiyalar"},
    {"name": "Moliya va buxgalteriya", "description": "Moliya, buxgalteriya va soliq sohasidagi vakansiyalar"},
]

EMPLOYERS = [
    {
        "email": "employer1@example.com",
        "password": "testpass123",
        "first_name": "Akbar",
        "last_name": "Rahimov",
        "company_name": "Davlat soliq qo'mitasi",
        "company_address": "Toshkent sh, Chilonzor tumani, Bunyodkor ko'chasi, 23-uy",
        "position": "HR Direktor"
    },
    {
        "email": "employer2@example.com",
        "password": "testpass123",
        "first_name": "Farida",
        "last_name": "Karimova",
        "company_name": "Toshkent davlat iqtisodiyot universiteti",
        "company_address": "Toshkent sh, Olmazor tumani, Universitet ko'chasi, 7-uy",
        "position": "Kadrlar bo'limi boshlig'i"
    },
    {
        "email": "employer3@example.com",
        "password": "testpass123",
        "first_name": "Davron",
        "last_name": "Qodirov",
        "company_name": "Respublika ixtisoslashtirilgan pediatriya markazi",
        "company_address": "Toshkent sh, Yunusobod tumani, Bog'ishamol ko'chasi, 223a-uy",
        "position": "HR Menejeri"
    },
]

CANDIDATES = [
    {
        "email": "candidate1@example.com",
        "password": "testpass123",
        "first_name": "Kamola",
        "last_name": "Sharipova",
        "patronymic": "Bahodirovna",
        "education": "higher",
        "specialization": "Moliya va kredit",
        "residential_address": "Toshkent sh, Yashnobod tumani, Parkent ko'chasi, 45-uy",
        "passport_number": "AA1234567"
    },
    {
        "email": "candidate2@example.com",
        "password": "testpass123",
        "first_name": "Jasur",
        "last_name": "Olimov",
        "patronymic": "Faxriddinovich",
        "education": "higher",
        "specialization": "Kompyuter muhandisligi",
        "residential_address": "Toshkent sh, Mirzo Ulug'bek tumani, Durmon yo'li ko'chasi, 56-uy",
        "passport_number": "AB7654321"
    },
    {
        "email": "candidate3@example.com",
        "password": "testpass123",
        "first_name": "Zilola",
        "last_name": "Mahmudova",
        "patronymic": "Anvarovna",
        "education": "secondary_higher",
        "specialization": "Pediatriya",
        "residential_address": "Toshkent sh, Shayxontohur tumani, A.Navoiy ko'chasi, 34-uy",
        "passport_number": "AC9876543"
    },
    {
        "email": "candidate4@example.com",
        "password": "testpass123",
        "first_name": "Sanjar",
        "last_name": "Yusupov",
        "patronymic": "Alimovich",
        "education": "higher",
        "specialization": "Davlat boshqaruvi",
        "residential_address": "Toshkent sh, Yunusobod tumani, Amir Temur ko'chasi, 107-uy",
        "passport_number": "AB1122334"
    },
    {
        "email": "candidate5@example.com",
        "password": "testpass123",
        "first_name": "Nodira",
        "last_name": "Azizova",
        "patronymic": "Maxmudovna",
        "education": "secondary_special",
        "specialization": "Buxgalteriya hisobi",
        "residential_address": "Toshkent sh, Sergeli tumani, Yangi Sergeli ko'chasi, 15-uy",
        "passport_number": "AC5566778"
    },
]

VACANCIES = [
    {
        "title": "Moliya bo'limi mutaxassisi",
        "category": "Moliya va buxgalteriya",
        "requirements": "Oliy ma'lumot: moliya, iqtisod yoki buxgalteriya yo'nalishi bo'yicha. Kamida 2 yillik ish tajribasi.",
        "salary_min": 3000000,
        "salary_max": 5000000,
        "location": "Toshkent, Chilonzor tumani"
    },
    {
        "title": "Dasturchi",
        "category": "IT va dasturlash",
        "requirements": "Oliy ma'lumot: kompyuter fanlari, dasturlash yo'nalishi bo'yicha. Python, Django bilan ishlash tajribasi.",
        "salary_min": 5000000,
        "salary_max": 10000000,
        "location": "Toshkent, Mirzo Ulug'bek tumani"
    },
    {
        "title": "Pediatr",
        "category": "Sog'liqni saqlash",
        "requirements": "Oliy tibbiy ma'lumot, pediatriya mutaxassisligi bo'yicha ordinator. Kamida 3 yillik ish tajribasi.",
        "salary_min": 4000000,
        "salary_max": 7000000,
        "location": "Toshkent, Yunusobod tumani"
    },
    {
        "title": "Davlat xizmatchisi",
        "category": "Davlat boshqaruvi",
        "requirements": "Oliy ma'lumot: davlat boshqaruvi, huquqshunoslik yo'nalishi bo'yicha. Davlat xizmatida ish tajribasi.",
        "salary_min": 4500000,
        "salary_max": 8000000,
        "location": "Toshkent, Chilonzor tumani"
    },
    {
        "title": "Oliy matematika o'qituvchisi",
        "category": "Ta'lim",
        "requirements": "Oliy ma'lumot: matematika yoki matematika o'qitish metodikasi yo'nalishi bo'yicha. Pedagogik tajriba.",
        "salary_min": 3500000,
        "salary_max": 6000000,
        "location": "Toshkent, Olmazor tumani"
    },
]

# Professional test savollari (soha bo'yicha)
PROFESSIONAL_QUESTIONS = [
    {
        "question_text": "O'zbekistonda soliq to'lovchilarni hisobga olish tartibi qanday qonun bilan tartibga solinadi?",
        "category": "Davlat boshqaruvi",
        "options": [
            {"option_text": "O'zbekiston Respublikasi Soliq kodeksi", "points": 10},
            {"option_text": "O'zbekiston Respublikasi Fuqarolik kodeksi", "points": 0},
            {"option_text": "O'zbekiston Respublikasi Mehnat kodeksi", "points": 0},
            {"option_text": "O'zbekiston Respublikasi Ma'muriy javobgarlik to'g'risidagi kodeksi", "points": 0}
        ]
    },
    {
        "question_text": "Python dasturlash tilida ro'yxat (list) elementlari indeksi qaysi sondan boshlanadi?",
        "category": "IT va dasturlash",
        "options": [
            {"option_text": "0", "points": 10},
            {"option_text": "1", "points": 0},
            {"option_text": "-1", "points": 0},
            {"option_text": "Ixtiyoriy", "points": 0}
        ]
    },
    {
        "question_text": "Bolalarda tana harorati ko'tarilganda qanday dori ishlatiladi?",
        "category": "Sog'liqni saqlash",
        "options": [
            {"option_text": "Paratsetamol", "points": 10},
            {"option_text": "Amoksitsillin", "points": 0},
            {"option_text": "Diazepam", "points": 0},
            {"option_text": "Digoksin", "points": 0}
        ]
    },
    {
        "question_text": "Qaysi moliyaviy hisobot korxonaning moliyaviy holatini ko'rsatadi?",
        "category": "Moliya va buxgalteriya",
        "options": [
            {"option_text": "Balans hisoboti", "points": 10},
            {"option_text": "Pul oqimi to'g'risidagi hisobot", "points": 0},
            {"option_text": "Daromadlar to'g'risidagi hisobot", "points": 0},
            {"option_text": "Soliq deklaratsiyasi", "points": 0}
        ]
    },
    {
        "question_text": "O'rta maktabda matematika o'qitishning asosiy maqsadi nima?",
        "category": "Ta'lim",
        "options": [
            {"option_text": "O'quvchilarning mantiqiy fikrlash qobiliyatini rivojlantirish", "points": 10},
            {"option_text": "O'quvchilarni olimpiadalarga tayyorlash", "points": 0},
            {"option_text": "Barcha o'quvchilarni matematika sohasiga yo'naltirish", "points": 0},
            {"option_text": "Faqat formulalarni yodlash", "points": 0}
        ]
    },
]

# Psixologik test savollari
PSYCHOLOGICAL_QUESTIONS = [
    {
        "question_text": "Men o'zimni ko'proq qanday ta'riflardim?",
        "options": [
            {"option_text": "Ekstravert (tashqi dunyoga qaratilgan)", "points": 5},
            {"option_text": "Introvert (ichki dunyoga qaratilgan)", "points": 5}
        ]
    },
    {
        "question_text": "Qaror qabul qilishda men ko'proq nimaga asoslanaman?",
        "options": [
            {"option_text": "Mantiqqa", "points": 5},
            {"option_text": "Intuitsiyaga", "points": 5}
        ]
    },
    {
        "question_text": "Qiyin vaziyatlarda men odatda...",
        "options": [
            {"option_text": "Barcha imkoniyatlarni tahlil qilaman", "points": 5},
            {"option_text": "Tezkor qaror qabul qilaman", "points": 5}
        ]
    },
    {
        "question_text": "Menga ko'proq yoqadi...",
        "options": [
            {"option_text": "Bir vazifaga chuqur sho'ng'ish", "points": 5},
            {"option_text": "Bir vaqtning o'zida bir necha vazifalar ustida ishlash", "points": 5}
        ]
    },
    {
        "question_text": "Mening kuchli tomonim...",
        "options": [
            {"option_text": "Aniqlik va tartib", "points": 5},
            {"option_text": "Moslashuvchanlik va o'zgarishlarga tayyorlik", "points": 5}
        ]
    },
]

# Korrupsiyaga moyillik test savollari
CORRUPTION_QUESTIONS = [
    {
        "question_text": "Sizningcha, professional faoliyatda qanday holatda qoidalarni chetlab o'tish mumkin?",
        "options": [
            {"option_text": "Hech qanday holatda mumkin emas", "points": 10},
            {"option_text": "Agar bu kompaniya manfaatlariga xizmat qilsa", "points": 5},
            {"option_text": "Agar bu shaxsiy foyda keltirsa va hech kim bilmasa", "points": 0}
        ]
    },
    {
        "question_text": "Ishxonada qimmatlligini hisobga olgan holda qanday sovg'alarni qabul qilish mumkin?",
        "options": [
            {"option_text": "Hech qanday sovg'alarni qabul qilmaslik kerak", "points": 10},
            {"option_text": "Faqat ramziy sovg'alarni (qalamlar, bloknot, kalendar)", "points": 7},
            {"option_text": "Ma'lum miqdorgacha bo'lgan sovg'alarni", "points": 4},
            {"option_text": "Agar bu ish munosabatlariga ta'sir ko'rsatmasa, har qanday sovg'ani", "points": 0}
        ]
    },
    {
        "question_text": "Hamkasbingiz yoki boshlig'ingiz qoidalarni buzayotganini ko'rsangiz...",
        "options": [
            {"option_text": "Darhol yuqori rahbariyatga yoki nazorat organlariga xabar beraman", "points": 10},
            {"option_text": "Avval ular bilan gaplashib, vaziyatni tushuntirishga harakat qilaman", "points": 7},
            {"option_text": "Aralashmayman, bu mening ishim emas", "points": 4},
            {"option_text": "Faqat bu harakat jiddiy zarar keltirsa, xabar beraman", "points": 2}
        ]
    },
    {
        "question_text": "Shaxsiy foydaga ega bo'lish uchun kompaniya resurslaridan foydalanish (masalan, ofis jihozlari, xizmat mashinasi)...",
        "options": [
            {"option_text": "Har qanday holatda noto'g'ri", "points": 10},
            {"option_text": "Agar bu kompaniyaga zarar keltirmasa, mumkin", "points": 5},
            {"option_text": "Ba'zan mumkin, agar bu keng tarqalgan amaliyot bo'lsa", "points": 2},
            {"option_text": "Agar bu kichik narsalar bo'lsa, muammo emas", "points": 0}
        ]
    },
    {
        "question_text": "Agar siz qabul qilayotgan qaror oila a'zongiz yoki yaqin do'stingizga foyda keltirsa...",
        "options": [
            {"option_text": "O'zimni bu qarordan chetlatib, boshqa shaxsga topshiraman", "points": 10},
            {"option_text": "Vaziyatni boshliqqа ma'lum qilaman va ko'rsatmalarga amal qilaman", "points": 8},
            {"option_text": "Eng adolatli qarorni chiqarishga harakat qilaman, ammo buni hech kimga aytmayman",
             "points": 4},
            {"option_text": "Yaqinlarimning manfaatlarini himoya qilishga harakat qilaman", "points": 0}
        ]
    },
]


@transaction.atomic
def load_test_data():
    """
    Test ma'lumotlarini yuklash
    """
    print("Test ma'lumotlarini yuklash boshlandi...")

    # Admin foydalanuvchisi
    if not User.objects.filter(email='admin@corruptino.uz').exists():
        admin_user = User.objects.create_superuser(
            email='admin@corruptino.uz',
            password='adminpass123',
            first_name='Admin',
            last_name='CorruptiNO'
        )
        print(f"Admin yaratildi: {admin_user.email}")

    # Kategoriyalarni yuklash
    categories = {}
    for category_data in JOB_CATEGORIES:
        category, created = JobCategory.objects.get_or_create(
            name=category_data['name'],
            defaults={'description': category_data['description']}
        )
        categories[category_data['name']] = category
        if created:
            print(f"Kategoriya yaratildi: {category.name}")

    # Ish beruvchilarni yuklash
    employers = {}
    for employer_data in EMPLOYERS:
        if not User.objects.filter(email=employer_data['email']).exists():
            user = User.objects.create_user(
                email=employer_data['email'],
                password=employer_data['password'],
                first_name=employer_data['first_name'],
                last_name=employer_data['last_name'],
                user_type='employer',
                is_verified=True
            )

            employer = EmployerProfile.objects.create(
                user=user,
                company_name=employer_data['company_name'],
                company_address=employer_data['company_address'],
                position=employer_data['position']
            )

            employers[employer_data['email']] = employer
            print(f"Ish beruvchi yaratildi: {user.email}")

    # Nomzodlarni yuklash
    candidates = {}
    for candidate_data in CANDIDATES:
        if not User.objects.filter(email=candidate_data['email']).exists():
            # Fayl yo'lini o'zgartirish kerak
            # passport_file = open('path/to/sample_passport.pdf', 'rb')

            user = User.objects.create_user(
                email=candidate_data['email'],
                password=candidate_data['password'],
                first_name=candidate_data['first_name'],
                last_name=candidate_data['last_name'],
                user_type='candidate',
                is_verified=True
            )

            candidate = CandidateProfile.objects.create(
                user=user,
                patronymic=candidate_data['patronymic'],
                education=candidate_data['education'],
                specialization=candidate_data['specialization'],
                residential_address=candidate_data['residential_address'],
                passport_number=candidate_data['passport_number'],
                # passport_pdf=File(passport_file, name='sample_passport.pdf')
            )

            candidates[candidate_data['email']] = candidate
            print(f"Nomzod yaratildi: {user.email}")

    # Vakansiyalarni yuklash
    for vacancy_data in VACANCIES:
        # Tasodifiy ish beruvchini tanlash
        employer = random.choice(list(employers.values()))

        # Kategoriyani topish
        category = categories.get(vacancy_data['category'])

        if category:
            vacancy = JobVacancy.objects.create(
                employer=employer,
                title=vacancy_data['title'],
                category=category,
                requirements=vacancy_data['requirements'],
                salary_min=vacancy_data['salary_min'],
                salary_max=vacancy_data['salary_max'],
                location=vacancy_data['location'],
                is_active=True
            )
            print(f"Vakansiya yaratildi: {vacancy.title}")

    # Professional test savollarini yuklash
    for question_data in PROFESSIONAL_QUESTIONS:
        category = categories.get(question_data['category'])

        if category:
            question = TestQuestion.objects.create(
                question_text=question_data['question_text'],
                question_type='professional',
                category=category,
                is_active=True
            )

            for option_data in question_data['options']:
                TestOption.objects.create(
                    question=question,
                    option_text=option_data['option_text'],
                    points=option_data['points']
                )

            print(f"Professional test savoli yaratildi: {question.question_text[:30]}...")

    # Psixologik test savollarini yuklash
    for question_data in PSYCHOLOGICAL_QUESTIONS:
        question = TestQuestion.objects.create(
            question_text=question_data['question_text'],
            question_type='psychological',
            is_active=True
        )

        for option_data in question_data['options']:
            TestOption.objects.create(
                question=question,
                option_text=option_data['option_text'],
                points=option_data['points']
            )

        print(f"Psixologik test savoli yaratildi: {question.question_text[:30]}...")

    # Korrupsiyaga moyillik test savollarini yuklash
    for question_data in CORRUPTION_QUESTIONS:
        question = TestQuestion.objects.create(
            question_text=question_data['question_text'],
            question_type='corruption',
            is_active=True
        )

        for option_data in question_data['options']:
            TestOption.objects.create(
                question=question,
                option_text=option_data['option_text'],
                points=option_data['points']
            )

        print(f"Korrupsiyaga moyillik test savoli yaratildi: {question.question_text[:30]}...")

    print("Test ma'lumotlari muvaffaqiyatli yuklandi!")


if __name__ == '__main__':
    load_test_data()