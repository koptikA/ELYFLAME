# ElyFlame Academy: маркетинговый ресерч для брифа и PRD сайта

Дата: 2026-09-24. Метод: WebSearch и WebFetch, собственные сайты школ и платформ, документация Google Search Central, schema.org и Meta, данные US Census (ACS) через API Census Reporter.
Обозначения: **[не проверено]** — вторичный источник или данные нельзя подтвердить первоисточником; **[не найдено]** — искали, но данных нет; **[не открылся]** — сайт не загрузился.

---

## 1. Краткие выводы

1. **Рядом прямые конкуренты, и сайты у них слабые.** В радиусе примерно 15 миль работают Rhythmix (тоже Buffalo Grove), AP Rhythmic Academy & Stretching Studio (Wheeling, в соседнем городе), North Shore Rhythmics (Glenview и Deerfield) и Vitrychenko Academy (Morton Grove и Arlington Heights). Ни один сайт не закрывает весь путь «выбрать класс по возрасту → увидеть цену → записаться на пробное → оплатить». Цены публикуют только Chicago Rhythmics и Queen RG.
2. **Позиционирование AP Rhythmic Academy почти совпадает с ElyFlame.** Название «Rhythmic Academy & Stretching Studio», дети с 3 лет, уровни до 6+, бесплатное пробное. Академия стоит в Wheeling, примерно в одном городе от ElyFlame. Отстраиваться придётся от неё в первую очередь: брендом, прозрачностью цен и удобной записью.
3. **Бесплатное пробное — норма рынка** (Rhythmix, AP, Vitrychenko, Queen RG). Платное пробное тоже встречается: Chicago Rhythmics берёт $15 через Zelle или PayPal, San Diego Rhythms — $25, Avanti (Австралия) — $25, North London RGA — £20. Цена $10 ниже этих ориентиров. Подавать её стоит как бронь места («$10 — резерв места, засчитывается в первый месяц»), а не как барьер. Засчитывать $10 или нет, решает клиент.
4. **Главные вопросы родителей** видны по FAQ-страницам. С какого возраста? Нужен ли опыт? Что надеть на пробное? Сколько стоит? Сколько детей на тренера? Можно ли смотреть занятие? Как попасть в соревновательную группу? Что с пропусками и возвратами? В отзывах родители хвалят тренеров по имени, растущую уверенность ребёнка, чистоту зала и быстрые ответы.
5. **Русская и восточноевропейская аудитория подтверждается.** По ACS 2020–2024 на русском, польском и других славянских языках дома говорят 13,4% жителей Buffalo Grove, 17,7% в Wheeling, 20,2% в Prospect Heights, 11,8% в Mount Prospect. У всех конкурентов тренеры — выходцы из Украины, Беларуси, Болгарии и России. Rhythmix размещается в русскоязычном справочнике Russian Flyers. Вывод: при запуске достаточно русской посадочной страницы или раздела, а не полной копии сайта. Подробнее в разделе 5.
6. **Регистрация.** Для старта с одной локацией и небольшим числом учеников подходит лёгкий вариант A: своя форма записи на пробное плюс оплата $10 через Stripe Payment Link. Вариант B — Jackrabbit (от $49/мес) или iClassPro (от $139/мес) для полного цикла: waiver, автоплатежи, родительский портал. Его стоит подключать, когда появятся регулярные абонементы. Сайт лучше проектировать так, чтобы кнопка «Register» вела на внешний портал и замена платформы не требовала редизайна.
7. **Instagram-ленту нельзя безопасно встроить на чисто статический сайт.** Basic Display API отключён 4 декабря 2024. Новый Instagram API требует Business- или Creator-аккаунт и токен, который живёт 60 дней. Держать токен в клиентском JS нельзя. Реалистичные варианты: вручную встроить 3–6 постов через официальный Embed, либо поставить маленькую serverless-функцию для обновления токена, либо сторонний виджет.
8. **Нынешний elyflame.com — нетронутая установка WordPress** с темой Twenty Twenty-Five и постом «Hello world!» от 09/28/2025. Имя автора поста — личный email владелицы. Страница бесполезна для конверсии, раскрывает email и работает на WordPress, хотя целевой стек — статический HTML, CSS и JS. Её нужно заменить целиком.
9. **Самый дешёвый рычаг в локальном SEO — Google Business Profile, отзывы и schema.org.** Подходит `SportsClub` (подтип `SportsActivityLocation`) с `address`, `geo`, `openingHoursSpecification` и `telephone`. Звёзды из собственных отзывов в выдачу не попадут: это запрещают правила Google о self-serving reviews. FAQ rich results для обычных сайтов с 2023 года не показываются, поэтому FAQ нужен людям, а не ради сниппета.
10. **Доверие строится на именах тренеров и их регалиях.** Конкуренты выставляют Master of Sport, олимпийцев и сборные. У ElyFlame публично подтверждается одно: Yelizaveta Yuvkhimenko из Illinois есть в национальном списке судей USA Gymnastics по художественной гимнастике. Биографию тренеров, результаты учениц и фото нужно получить у клиента, иначе блок доверия будет пустым.

---

## 2. Конкуренты

### 2.1 Сводная таблица

| # | Школа | Где | Программы и возраст | Цены | Пробное | Запись | Тренеры и результаты | Сайт: плюсы и минусы |
|---|---|---|---|---|---|---|---|---|
| 1 | **Rhythmix Inc.** https://www.rhythmixinc.com/ | Buffalo Grove. По вторичному источнику, 1700 Weiland Rd [не проверено] | Recreational с 3 лет: Beginner 3–6, Beginner 7+, Intermediate, Advanced, Pre-Team. Competitive L3–9 по рекомендации тренера | не найдено | Бесплатное: «the first class is always free» | Своя форма /register (поля уровня для двух детей); формы и правила лежат в Google Drive | Irina Polyachenko (35+ лет, первый тренер олимпийских чемпионок Tamara Yerofeyeva и Olga Andreyeva), Valery Roytman (бывшая участница сборной США). 4,9★ на Google, 30 отзывов (через Trustindex) | + Цепляющие отзывы, ясный pathway. − Нет цен и расписания, адрес не показан явно, WordPress/Brizy, CTA «Register now» без слов о пробном |
| 2 | **AP Rhythmic Academy & Stretching Studio** https://aprhythmicacademy.com/ | 970 Seton Court, Wheeling, IL 60090 | С 3 лет: Pre-school, Level 1 Xcel … Level 6+. Балет | не найдено | Бесплатное: «BOOK A FREE TRIAL CLASS NOW» | Форма на лендинге, дальше связываются вручную | Anastasiya — Master of Sport international class, победительница Универсиады. В команде есть судьи UEG и USAG. Календарь соревнований 2026 и собственный Diamond Cup | + Одностраничник, расписание по вкладкам уровней, сильный hero-CTA, магазин. − Нет цен и отзывов, конструктор Weblium, блоки дублируются |
| 3 | **North Shore Rhythmic Gymnastics Center (NSR)** https://www.northshorerhythmics.com/ | Glenview (2400 Chestnut Ave) и Deerfield (Sachs Rec Center, 455 Lake Cook Rd) | Recreational и competitive, от 4 лет до олимпийского уровня | не найдено (на сайте) | не найдено | Recreational — через системы регистрации Glenview и Deerfield Park District | Олимпийцы Tokyo 2020 (Evita Griskenas, Lili Mizuno), Laura Zeng. Тренеры Natalia Klimouk и Dani Takova. «2024 USA Gymnastics Rhythmic Coaches of the Year» | + Самый сильный бренд и результаты. − Ориентирован на элиту, у новичка нет понятного пути, запись уводит на чужие сайты парков |
| 4 | **Vitrychenko Academy** http://www.vitrychenkoacademy.com/ | 6203 Kirk St, Morton Grove; вторая локация в Arlington Heights. В сторонних каталогах старый адрес в Niles | Level 1 (2,5–5 лет, некомпетитивный), L3–5 (5+), L6–10. Балет | не найдено | Форма «Request FREE Class» на /contact | Форма; waiver и codes of conduct подписываются отдельными формами | Olena Vitrychenko — бронза Олимпиады 1996, 9-кратная чемпионка мира. Natalia Pushkina — «Coach of the Year» 2023. На Yahoo/Yelp 3,0★ из 5 отзывов, есть резко негативные | + Самые сильные регалии. − Сайт образца 2015–2016 года, при проверке сертификат HTTPS был просрочен, футер «© 2015-2016», противоречивые адреса |
| 5 | **Chicago Rhythmics** https://www.chicagorhythmics.com/ | Chicago: South Loop, West Loop, Lincoln Park (6 залов-партнёров) | Beginners с 3,5 лет, Beg/Int 5–6, Intermediate 6+, Competitive Team 6+ | **Опубликованы:** 8 недель, раз в неделю: $208 (45 мин), $252 (60 мин), $348 (90 мин) | **Платное, $15**, оплата через Zelle или PayPal | Три шага: email → оплата → PDF-формы | Alisa и Natalie — участницы Олимпиады 2016 в групповых упражнениях. «USAG Safety Certified and CPR Certified» | + Прозрачные цены, понятный процесс пробного, акцент на безопасности. − Всё вручную (email, PDF), дизайн Weebly 2018 года |
| 6 | **Queen RG Club** https://www.queenrgclub.com/ | 28156 W Northpointe Pkwy, Lake Barrington | Beginners 4–6, Non-Competitive 6–10, Competitive 7–16 (L3–9) | **Опубликованы:** Beginners $150/мес (раз в неделю), $300 (два раза); Non-comp $250/$350/$450 в месяц | Бесплатный try-out через календарь бронирования | Wix Pricing Plans и booking calendar | Проводит Queen RG Cup. Отзыв гимнастки уровня 9 про чувство безопасности | + Цены и онлайн-бронь. − Шаблон Wix, мало информации о тренерах |
| 7 | **Taiga Gymnastics** https://www.taigagymnastics.com/skokie | Skokie (Weber Center), а также Glencoe, Wilmette, Lincolnwood | Pre-school, K-8 (гимнастика с элементами rhythmic и AGG), взрослые | не найдено | не найдено | Через сайт Skokie Park District | «Nordic values», безопасность и радость | Не чистая художественная гимнастика, но конкурирует за тех же детей и за взрослых |
| 8 | **Sokol Naperville Tyrs** https://sokolnaperville.com/our-program/ | Naperville (Naperville Central HS) | «Basic Rhythmic Gymnastics in the Fall» внутри общей программы | на отдельной странице, не извлечено | не найдено | не найдено | не найдено | Далеко от Buffalo Grove, для ElyFlame неактуален |

Не открылись: https://www.rhythmicregion3.com/clubs/illinois/ (DNS), страницы Deerfield Park District (ECONNREFUSED), Yelp (403), LoopNet (403). Список клубов Illinois USA Gymnastics (https://ilusagymnastics.com/clubs/) дисциплину не указывает, ElyFlame в нём нет.

### 2.2 Короткие разборы

- **Rhythmix — главный соперник в поиске по «Buffalo Grove».** Title сайта: «Rhythmic Gymnastics School Buffalo Grove, Chicago, Illinois». Rhythmix выигрывает отзывами (29 из 30 — пятёрки) и 30-летней историей семьи тренеров. Цитата родителя: «We travel 18 miles in one direction to go there but it is totally worth it.» (https://www.trustindex.io/reviews/rhythmixinc.com). Слабые места сайта: пробное спрятано в тексте программы, цен нет, форма регистрации сделана как анкета.
- **AP Rhythmic Academy** выглядит современнее всех остальных. Hero с CTA на бесплатное пробное, расписание по уровням на вкладках, календарь соревнований, собственный турнир, магазин формы. Но отзывов и цен нет, а после отправки формы нужна ручная переписка.
- **NSR** держится на олимпийском бренде. Для родителей трёхлетки он скорее пугает: сайт почти не объясняет, куда идти новичку.
- **Vitrychenko** — самые громкие регалии при самом устаревшем сайте. Отзывы поляризованы, в негативных жалуются на деньги и отношение к детям.
- **Chicago Rhythmics** — лучший пример **прозрачности**: опубликованы цены, стоимость пробного и правила для родителей («parents are not permitted in the gymnastics area»). Процесс при этом ручной.

---

## 3. Платформы регистрации и оплаты

Цены взяты со страниц самих платформ на дату исследования.

| Платформа | Цена | Онлайн-регистрация | Waiver | Автоплатежи | Родительский портал или приложение | Встраивание на сайт | Пробное | Замечания |
|---|---|---|---|---|---|---|---|---|
| **iClassPro** https://www.iclasspro.com/pricing | Signature $139/мес за локацию; Elite $199; Premium $299 (контракт на 12 мес). Branded App: $499 разово плюс $150/мес | Да | Да, online waivers | Да, Payment Services | Да, iClassPro App и портал | Портал `portal.iclasspro.com/<gym>/classes` (пример: https://portal.iclasspro.com/napergym/classes); DIY-сайт включён | Lead capture, пробное — [не проверено] | Стандарт индустрии для гимнастики: skill tracking и оценки учеников |
| **Jackrabbit Class** https://www.jackrabbitclass.com/pricing/ | От $49/мес, зависит от числа учеников на конец месяца; Plus от $93/мес плюс $169 setup; Enterprise $245/мес | Да | Да, e-signature | Да | Да, Parent Portal | Да, «Class Listings» встраиваются на сайт (https://www.jackrabbitclass.com/features/online-registration/) | Да, trial class management | Самый дешёвый полноценный вариант. Пороги числа учеников по тарифам на странице не показаны |
| **Sawyer** https://www.hisawyer.com/for-business/pricing | Launch $79/мес ($71 при оплате за год); Grow $219 ($189); Scale $399 ($379). Карты 3% + $0,30, с родителя booking fee $1,99–3,99 [по данным поиска] | Да | e-signature только с Grow | Автобиллинг и memberships только с Grow | Да, семейные профили | Да | Trial classes только с Grow | Комиссия маркетплейса 30% на Launch обязательна. Цены в сторонних обзорах расходятся с официальной страницей, опираться на неё |
| **Amilia SmartRec** https://www.amilia.com/pricing | Standard $99/мес, Advanced $499. Плюс 1% сервисный сбор и 2,85% + $0,30 за карту | Да | [не проверено] | [не проверено] | Да | Онлайн-магазин | [не проверено] | Рассчитан на парки и муниципалитеты, для маленькой студии избыточен |
| **Pike13** https://www.pike13.com/pricing | Essential $139/мес (годовая оплата) или $159; Advanced $195 или $225; Premium $249 или $286 | Да | Digital waivers только с Advanced | Да, Automated Billing | Да, клиентское приложение | Виджеты только с Advanced | [не проверено] | Больше про студии и фитнес; skill assessments только в Premium |
| **Square Appointments** https://squareup.com/us/en/appointments/pricing | Free-план плюс процессинг; Plus и Premium платные, суммы на странице не извлечены | Онлайн-бронь | Нет | Нет, есть депозиты | Нет | Сайт бронирования | Подходит для пробного как «услуги» | Лёгкий вариант для записи на пробное, не для абонементов |
| **Stripe Payment Links** https://stripe.com/pricing | Без абонентской платы; 2,9% + 30¢ за карту; ACH 0,8% (не больше $5) | Нет | Нет | Stripe Billing отдельно | Нет | Ссылка или кнопка | $10 за пробное: комиссия около $0,59 | Самое простое решение, чтобы брать оплату за пробное |

### Рекомендация: вариант A сейчас, вариант B как следующий этап

- **Вариант A (MVP).** Собственная форма «Book a trial» на сайте. Поля: имя родителя, телефон, email, возраст ребёнка, программа, удобный день. Бронь подтверждается оплатой $10 через Stripe Payment Link с redirect на страницу «Спасибо». Waiver подписывается на первом занятии или через простую e-sign форму. Форме нужен бэкенд-приёмник (Formspree, Netlify Forms или Google Apps Script). Плюсы: $0 в месяц, полный контроль над UX и брендом, путь пробного можно сделать в 2–3 шага. Минусы: ручное подтверждение времени, нет автоплатежей по абонементу.
- **Вариант B (когда пойдут регулярные абонементы).** Jackrabbit, если важна цена: от $49/мес, есть Class Listings для встраивания и trial management. iClassPro, если важны стандарт гимнастической индустрии, skill tracking и приложение: от $139/мес. Sawyer подходит, только если интересен трафик из маркетплейса, но там комиссия и функции ограничены по тарифам.
- **Требование к дизайну при любом варианте:** CTA «Book a trial» и «Register» должны вести на один настраиваемый URL. Тогда переход с A на B — это смена ссылки, а не переделка сайта. Нужно заложить состояние «перенаправляем на портал регистрации».

---

## 4. Лучшие практики: примеры сильных сайтов

| Пример | URL | Что сделано хорошо |
|---|---|---|
| The Little Gym (гимнастика, франшиза) | https://www.thelittlegym.com/ | Два CTA в hero: «Pick Your Perfect Class» и «Free Intro». Программы разбиты по возрасту: Parent/Child с 4 месяцев, Pre-K, Grade School. «Find Your Gym». Отзывы с пометкой «Based on most recent 100 reviews» |
| Goldfish Swim School (плавание) | https://www.goldfishswimschool.com/ | Подбор уровня через «Take Our Swim Assessment» («Not sure what class is right for your child?»). Безопасность на первом плане. Цифры доверия: «300,000+ Hours of Instructor Training». FAQ снимает возражения |
| British Swim School (плавание) | https://www.britishswimschool.com/ | «Start Swim Assessment», группы по возрасту, «4.7 / 5 by 10,000+ Satisfied Swimmers», размер группы «4-6 swimmers», сертификаты инструкторов |
| Tutu School (балет для малышей) | https://www.tutuschool.com/ | Один сильный оффер: «Take the first step with a FREE trial class!» Эмоциональная миссия: «every child should know what it feels like to dance» |
| Premier Martial Arts (единоборства) | https://www.premiermartialarts.com/ | Пробное усилено бонусом: «1 Trial Lesson & Karate Uniform Included», CTA «TRY US OUT TODAY». Аналогия для ElyFlame: пробное за $10 плюс, например, скрандж или фото на память |
| North London Rhythmic Gymnastics Academy (Великобритания) | https://northlondongymnastics.academy/ | Платное пробное (£20) подаётся без смущения. Классы по **году рождения** — родителю не нужно разбираться в уровнях. «All coaches are DBS checked». CTA: «Give your daughter the right start in life - book a trial class now!» |
| Avanti Rhythmics (Австралия) | https://avantirhythmics.com.au/ | «Book a trial», $25, кнопка ведёт прямо в систему бронирования. Награды клуба и отзывы о тренере по имени |
| Club PERÓ (Австралия) | https://www.clubpero.com.au/ | Таблица уровней с часами в неделю. Прозрачный pathway: Beginner → Junior → Intermediate → Competition (по отбору). Сертификаты тренеров (First Aid/CPR, Working with Children). Пробное сейчас приостановлено |
| Chicago Rhythmics (США) | https://www.chicagorhythmics.com/registration.html | Пробное $15 описано в 3 шагах, цены за сессию опубликованы, правила для родителей и блок про безопасность рядом с ценой |

**Паттерны, которые стоит перенести в ElyFlame:**
1. В hero один главный CTA: «Book a $10 trial class». Второстепенный: «Find the right class».
2. Подбор класса в два клика: возраст ребёнка (3–5 / 6+ / взрослый) → программа (Recreational / Competitive / Stretching). Результат — карточка с днями, временем, ценой и той же кнопкой «Book trial».
3. Блок «Your first class» в три шага: что надеть, когда прийти, что будет на занятии.
4. Цифры доверия и сертификаты рядом с CTA: USA Gymnastics membership, SafeSport, CPR, размер группы.
5. Pathway «Recreational L1–2 → Competitive L3–6» одной схемой.
6. Отзывы с именами тренеров, ссылка «See all reviews on Google».
7. Sticky-кнопка «Book trial» на мобильном и tap-to-call.

---

## 5. Аудитория

### 5.1 Мотивы и страхи

По FAQ школ, чек-листам и отзывам:

- **Безопасность и квалификация.** Чек-лист Jackrabbit для родителей: «Look for a gym with experienced safety-certified coaches…», «a USA Gymnastics Member Club or AAU Member Club», соотношение «6-10 kids per coach» (https://www.jackrabbitclass.com/blog/how-to-pick-the-right-gymnastics-gym-for-your-child/). Chicago Rhythmics: «Safety is our number one priority… USAG Safety Certified and CPR Certified».
- **Тренер как человек.** В отзывах тренеров хвалят по имени: «Valerie is amazing! She has a great approach with the kids…» (https://www.rhythmixinc.com/contact/), «Valery always responds to my questions and concerns in a timely way» (Google через Trustindex).
- **Результат для ребёнка — уверенность, а не медали.** «Since she started this program her confidence and concentration have increased dramatically.» (Trustindex, Rhythmix).
- **Чистота и зал.** «The facility is outstanding and extremely well kept.» (Trustindex, Rhythmix).
- **Страх переплатить или попасть в токсичную среду.** Негатив про Vitrychenko: «abnormally strong obsession with money», «they don't know how to teach» (https://local.yahoo.com/info-209869124-vitrychenko-academy-niles/). Против этого страха работают прозрачные цены и политика возвратов.
- **Готовность ездить далеко ради качества.** «We travel 18 miles in one direction…» Значит, SEO стоит строить на весь North Shore и Northwest suburbs, а не только на Buffalo Grove.

### 5.2 Какие вопросы закрывает FAQ

Сводно по https://sandiegorhythms.com/faqs (28 вопросов), https://www.dianasrhythmicclub.com/faqs и https://www.novagymrg.com/what-is-rhythmic-gymnastics:

- Чем художественная гимнастика отличается от спортивной? Только ли она для девочек?
- С какого возраста можно начать? Не поздно ли? Нужен ли опыт?
- Есть ли пробное, сколько стоит, что надеть и принести? «comfortable clothes like shorts or leggings and a t-shirt», «hair pulled up», «no jewelry»
- Как подобрать класс? Как перейти на следующий уровень? Как попасть в соревновательную группу? («6 years old by December 31st» для Development-соревнований, «Usually it takes about a year»)
- Сколько раз в неделю и как долго? Сколько детей на тренера? Какая квалификация у тренеров?
- Цена, политика оплаты, скидки для братьев и сестёр (у Diana's — 10%), скидки за рекомендацию
- Пропуски, отработки, возвраты, выход из программы
- Можно ли смотреть занятие? Нужно ли оставаться? Что если опоздали?
- Где купить мяч, ленту, купальник?

### 5.3 Язык и русскоязычная аудитория

**Демография.** ACS 2020–2024, 5-year, таблица C16001 «Russian, Polish, or other Slavic languages», население от 5 лет, через https://api.censusreporter.org:

| Город | Говорят дома на русском, польском или другом славянском | Доля |
|---|---|---|
| Prospect Heights | 2 960 | 20,2% |
| Wheeling | 6 437 | 17,7% |
| **Buffalo Grove** | **5 507** | **13,4%** |
| Mount Prospect | 6 195 | 11,8% |
| Des Plaines | 6 416 | 11,4% |
| Arlington Heights | 7 389 | 10,4% |
| Vernon Hills | 2 351 | 9,3% |
| Glenview | 3 639 | 8,1% |
| Northbrook | 2 621 | 8,0% |

Ограничение: в этой таблице русский объединён с польским, а польская община в Mount Prospect и Des Plaines большая. Отдельной цифры по русскому для места найти не удалось, детальная таблица B16001 для этих мест через API недоступна. Вторичный источник (блог со ссылкой на «Russian Yellow Pages»): 18,7% русскоязычных в Buffalo Grove, 14,3% в Northbrook, 8,9% в Wheeling (https://www.everygoddamnday.com/2020/01/blog-post.html) **[не проверено]**. Общий фон Buffalo Grove: 38,1% жителей родились за рубежом, медианный доход домохозяйства $129 395 (https://censusreporter.org/profiles/16000US1709447-buffalo-grove-il/, https://datausa.io/profile/geo/buffalo-grove-il).

**Инфраструктура сообщества:**
- Krug Community Circle, 1400 S. Wolf Rd, Wheeling — «a cultural center for the Russian speaking community in the Chicagoland area». Внутри Russian Classical Ballet Academy и Sunday School Unicum (https://www.krugcommunitycircle.com/).
- Russian School of Mathematics — филиал Buffalo Grove / Wheeling, 797 S Buffalo Grove Rd (https://www.facebook.com/RSMWheeling/ — страница не открылась без логина; адрес по https://www.schoolandcollegelistings.com/…) **[не проверено]**.
- ElyFlame занимается в здании Silk Road International School (1250 Radcliffe Rd). Это школа-побратим SRIS Bishkek, Кыргызстан (https://srischicago.com/en/about-us — сейчас «restoring»; данные из поискового сниппета) **[частично не проверено]**. Пост об открытии: https://www.facebook.com/groups/BGSHOPLOCAL/posts/2301239096987823/.
- Rhythmix продвигается в русскоязычном каталоге Russian Flyers (https://www.russianflyers.com/business/5813).

**Нужна ли русская версия? Рекомендация:**
- Основной сайт — на английском. Все конкуренты англоязычные, в семьях дети учатся в американских школах, а часть аудитории — не славяне.
- Добавить **одну русскую посадочную страницу `/ru/`**: программы, цены, запись на пробное, FAQ. На неё вести из Instagram и русскоязычных чатов. Переключатель EN/RU в шапке.
- Технически: отдельные URL, `hreflang` в обе стороны и `x-default`, как требует https://developers.google.com/search/docs/specialty/international/localized-versions. Не переключать язык скриптом на одном URL и не делать автоматический редирект.
- Украинская версия не нужна, русский покрывает большинство. Если среди клиентов много украинских семей, это вопрос тона: стоит проверить с клиентом.
- Проверить у клиента: на каком языке сейчас пишут родители в DM, какая доля текущих учениц из русскоязычных семей.

---

## 6. Локальное SEO и Instagram

### 6.1 Структура данных

- Google: обязательные поля `name` и `address`; рекомендованы `geo`, `openingHoursSpecification`, `telephone`, `priceRange`, `url`. «Use the most specific LocalBusiness sub-type possible» (https://developers.google.com/search/docs/appearance/structured-data/local-business).
- Самый точный тип — **`SportsClub`**: Thing → Organization/Place → LocalBusiness → SportsActivityLocation → SportsClub (https://schema.org/SportsClub, https://schema.org/SportsActivityLocation). Для школы с классами подходит именно он. Можно добавить `ExerciseGym` для stretching-студии, но основным должен быть один тип.
- **Звёзды из своих отзывов не выводить.** Правило Google: «If the entity that's being reviewed controls the reviews about itself, their pages that use LocalBusiness or any other type of Organization structured data are ineligible for star review feature» (https://developers.google.com/search/docs/appearance/structured-data/review-snippet).
- **FAQPage** rich results с 14.09.2023 показываются «only… for well-known, authoritative government and health websites» (https://developers.google.com/search/docs/appearance/structured-data/faqpage). Разметку можно оставить, но ждать сниппета не стоит.

Черновик JSON-LD (значения уточнить у клиента):
```json
{
  "@context": "https://schema.org",
  "@type": "SportsClub",
  "name": "ElyFlame Academy of Rhythmic Gymnastics",
  "url": "https://elyflame.com/",
  "telephone": "+1-224-804-8324",
  "address": {"@type": "PostalAddress","streetAddress": "1250 Radcliffe Rd","addressLocality": "Buffalo Grove","addressRegion": "IL","postalCode": "60089","addressCountry": "US"},
  "sameAs": ["https://www.instagram.com/elyflamerg_yuvkhimenko/","https://www.facebook.com/profile.php?id=61573847340841"]
}
```
Телефон взят из вторичного каталога GymnasticsUS **[не проверено, подтвердить у клиента]**.

### 6.2 Google Business Profile

- Название должно совпадать с реальным: «Your name should reflect your business's real-world name…». Ключевые слова в название добавлять нельзя (https://support.google.com/business/answer/3038177).
- Категория отвечает на вопрос «This business IS a…» — например, Gymnastics center. Stretching — дополнительная категория, если студия действительно ею является.
- Ранжирование строится на relevance, distance и prominence. «More reviews and positive ratings can help your business's local ranking»; «There's no way to request or pay for a better local ranking» (https://support.google.com/business/answer/7091).
- Следствие для продукта: после пробного занятия нужен сценарий «попросить отзыв в Google» — email или SMS со ссылкой. Это нужно вписать в PRD.

### 6.3 Ключевые запросы

Частотность не проверена: доступа к Google Keyword Planner нет. Список — гипотезы по формулировкам, которые конкуренты используют в title:
- `rhythmic gymnastics near me`, `rhythmic gymnastics Buffalo Grove`, `rhythmic gymnastics classes for kids`, `rhythmic gymnastics Northbrook / Wheeling / Arlington Heights / Vernon Hills / Deerfield / Long Grove`
- `gymnastics for 3 year old Buffalo Grove`, `ribbon gymnastics classes`, `rhythmic gymnastics trial class`
- `stretching classes Buffalo Grove`, `flexibility class for dancers / figure skaters`, `adult stretching class near me`
- На русском: `художественная гимнастика Buffalo Grove`, `художественная гимнастика Чикаго`
- Rhythmix делает title «Rhythmic Gymnastics School Buffalo Grove, Chicago, Illinois», Vitrychenko — «Illinois Rhythmic Gymnastics Club». ElyFlame нужен title вида «Rhythmic Gymnastics & Stretching in Buffalo Grove, IL | ElyFlame Academy» и отдельные страницы программ.

### 6.4 Instagram-лента

- **Basic Display API закрыт:** «Starting on December 4th, 2024, Instagram Basic Display API will no longer be available… there will no longer be a set of Instagram APIs for consumer developer apps» (https://developers.facebook.com/blog/post/2024/09/04/update-on-instagram-basic-display-api/).
- **Замена — Instagram API with Instagram Login** или with Facebook Login. Работает только с «Instagram professional account», то есть Business или Creator. Long-lived token «valid for 60 days and can be refreshed». Для своего аккаунта хватает Standard Access, App Review не нужен (https://developers.facebook.com/docs/instagram-platform/overview/).
- **Что это значит для статического HTML, CSS и JS.** Токен нельзя класть в клиентский JS, и его нужно обновлять раз в 60 дней. Нужен минимальный серверный компонент: serverless-функция или cron, который по расписанию обновляет токен и кладёт JSON с последними постами в статический файл.
- **Самый простой вариант без API:** официальный Embed для отдельных публичных постов (кнопка «…» → Embed; https://developers.facebook.com/docs/instagram-platform/embed-button). Для сайта хватит 3–6 закреплённых постов или Reels, обновляемых вручную. Минус: каждый embed грузит скрипт Instagram, это бьёт по скорости на мобильном. Лучше подгружать лениво, после клика по превью.
- oEmbed (`GET /instagram_oembed`, 1000 запросов в час) годится только для отображения; приватные аккаунты не поддерживаются (https://developers.facebook.com/docs/instagram-platform/oembed).
- **Рекомендация:** на MVP — статическая галерея из своих фото (быстро, красиво, под контролем бренда) и кнопка «Follow on Instagram». Живая лента — на этап 2 через serverless. Проверить у клиента, что аккаунт `elyflamerg_yuvkhimenko` переведён в Business или Creator.

---

## 7. Что известно про ElyFlame

| Факт | Источник | Статус |
|---|---|---|
| ELYFLAME Academy of Rhythmic Gymnastics Corp., 1250 Radcliffe Rd, Buffalo Grove, IL 60089 | https://gymnasticsus.com/gyms/gym-elyflame-academy-of-rhythmic-gymnastics-corp-buffalo-grove-il | вторичный |
| Телефон (224) 804-8324; «USAG Member»; «Enrolling Now»; рейтинг 3,8★ (16 отзывов), источник рейтинга не указан | там же | **не проверено** |
| Академия открылась в здании Silk Road International School; в посте упоминается «Trial Cl…» | https://www.facebook.com/groups/BGSHOPLOCAL/posts/2301239096987823/ (текст виден частично) | частично |
| SRIS Chicago (preK–3rd grade, основана в 2023) находится по тому же адресу, 1250 Radcliffe Rd | поисковый сниппет, https://srischicago.com (сейчас «restoring») | не проверено |
| Instagram: title профиля «ElyFlame Academy & Yelizaveta Yuvkhimenko» | поисковая выдача; сама страница требует логина | не открылся |
| Facebook-страница называется «RG Coach Yelizaveta \| Buffalo Grove IL» | https://www.facebook.com/profile.php?id=61573847340841 | виден только заголовок |
| **Yelizaveta Yuvkhimenko, IL** — в «2025-2028 Rhythmic National Judges' List (Dec 8, 2025)» USA Gymnastics, отмечена в первой колонке (L3-5 & Beg Group) с пометкой «P» | https://static.usagym.org/PDFs/Rhythmic/judging/judge_list.pdf | первоисточник. Что значит «P», не расшифровано (вероятно, provisional) — уточнить |
| Статья Columbia Chronicle (2022): Yelizaveta Yuvkhimenko, студентка Columbia College Chicago, родом из Киева, переехала в Чикаго с родителями. Про гимнастику в статье ничего нет | https://columbiachronicle.com/campus/ukrainian-russian-and-polish-students-share-worries-for-home/ | **что это тот же человек, не проверено** |
| elyflame.com: WordPress (PHP 8.2, хостинг hcdn), тема Twenty Twenty-Five, единственный пост «Hello world!» от 09/28/2025. Автор поста показан как личный gmail-адрес | https://elyflame.com/, https://elyflame.com/?p=1 | первоисточник |
| Результаты соревнований учениц ElyFlame | — | не найдено |
| Отзывы на Google или Yelp с текстом | — | не найдено (Yelp отвечает 403, Google Maps не парсится) |
| Членство USAG в официальном поиске клубов | — | не проверено: список IL USAG дисциплину не показывает, ElyFlame в нём нет |

**Что запросить у клиента для PRD:** биографии и фото тренеров (разряды, судейская категория, SafeSport, CPR); подтверждение членства USAG; расписание и цены; политику по пробному ($10 — засчитывается или нет); результаты учениц; 5–10 отзывов родителей с разрешением на публикацию; фото зала; часы работы; схему входа в здание школы; нужен ли русский.

Отдельно: имя автора с личным email на текущем WordPress — утечка контакта. Когда сайт уйдёт с WordPress, вопрос закроется сам.

---

## 8. Что упускают конкуренты и чем может выделиться ElyFlame

1. **Прозрачные цены на сайте.** У ближайших конкурентов (Rhythmix, AP, NSR, Vitrychenko) цен нет. Карточка программы с ценой и фразой «no hidden fees» закрывает главный страх из негативных отзывов.
2. **Запись на пробное за минуту с оплатой онлайн.** У всех остальных «оставьте заявку, мы свяжемся» или email плюс Zelle. ElyFlame может дать: выбрать возраст → выбрать слот → оплатить $10 → получить подтверждение и памятку «what to bring».
3. **Подбор класса по возрасту или году рождения**, как у North London RGA. Ни у одного местного конкурента этого нет.
4. **Stretching & Flexibility для других видов спорта и взрослых** — отдельная воронка, которую не использует никто, кроме названия у AP. Отдельные страницы для фигуристок, танцоров и взрослых, свои ключевые слова и свой CTA.
5. **Раздел «Safety & coaches» как отдельный блок доверия:** SafeSport, CPR, USAG-судейство основателя. Судейская квалификация — сильный и редкий аргумент: судья знает, за что ставят баллы.
6. **Путь новичка до соревнований одной схемой:** L1–2 Recreational (3–5 лет) → L3–6 Competitive (6+), со сроками и требованиями. У NSR и Vitrychenko путь показан только для элиты.
7. **Двуязычие EN + RU.** Ни у кого из конкурентов нет русской версии, хотя тренеры везде русско- или украиноязычные.
8. **Бренд и визуальный уровень.** Сайты конкурентов сделаны на шаблонах Weebly, Wix, Weblium и старого WordPress. Премиальный визуал (маджента, градиент пламени, засечки в духе Cinzel), быстрый мобильный сайт на чистом HTML — заметное отличие само по себе.
9. **Системный сбор отзывов в Google** после пробного и через 30 дней. У Rhythmix 30 отзывов — это достижимая планка.
10. **Страница «Your first class»** с фото входа в здание школы, парковкой, правилами для родителей (можно ли смотреть) и списком вещей. Снимает тревогу перед первым визитом.

---

## 9. Источники

**Конкуренты**
- https://www.rhythmixinc.com/ · /about-us/ · /recreational-rhythmic-gymnastics-program/ · /register · /resources-parents/ · /contact/
- https://www.trustindex.io/reviews/rhythmixinc.com
- https://www.russianflyers.com/business/5813 (вторичный)
- https://aprhythmicacademy.com/
- https://www.northshorerhythmics.com/ · /recreational-rg.html · /coaches.html · /locations.html
- http://www.vitrychenkoacademy.com/ · /classes/ · /about/staff/ · /about/registration-forms/ · /contact/
- https://local.yahoo.com/info-209869124-vitrychenko-academy-niles/
- https://www.chicagorhythmics.com/ · /classes.html · /about.html · /registration.html · /locations.html · /coaches.html
- https://www.queenrgclub.com/ · /plans-pricing
- https://www.taigagymnastics.com/skokie
- https://sokolnaperville.com/our-program/
- https://ilusagymnastics.com/clubs/
- Не открылись: https://www.rhythmicregion3.com/clubs/illinois/, https://www.deerfieldparks.org/175/Rhythmic-Gymnastics, Yelp (403), https://www.loopnet.com/Listing/1250-Radcliffe-Rd-Buffalo-Grove-IL/10953942/ (403), https://classpass.com/… (403)

**Платформы**
- https://www.iclasspro.com/pricing · https://www.iclasspro.com/
- https://www.jackrabbitclass.com/pricing/ · https://www.jackrabbitclass.com/features/online-registration/
- https://www.hisawyer.com/for-business/pricing
- https://www.amilia.com/pricing
- https://www.pike13.com/pricing
- https://squareup.com/us/en/appointments/pricing
- https://stripe.com/pricing

**Лучшие практики**
- https://www.thelittlegym.com/
- https://www.goldfishswimschool.com/
- https://www.britishswimschool.com/
- https://www.tutuschool.com/
- https://www.premiermartialarts.com/
- https://northlondongymnastics.academy/
- https://avantirhythmics.com.au/
- https://www.clubpero.com.au/

**Аудитория**
- https://sandiegorhythms.com/faqs
- https://www.dianasrhythmicclub.com/faqs
- https://www.novagymrg.com/what-is-rhythmic-gymnastics
- https://www.jackrabbitclass.com/blog/how-to-pick-the-right-gymnastics-gym-for-your-child/
- https://api.censusreporter.org/1.0/data/show/latest?table_ids=C16001 (ACS 2024 5-year)
- https://censusreporter.org/profiles/16000US1709447-buffalo-grove-il/
- https://datausa.io/profile/geo/buffalo-grove-il
- https://www.everygoddamnday.com/2020/01/blog-post.html (вторичный, не проверено)
- https://www.krugcommunitycircle.com/

**SEO и Instagram**
- https://developers.google.com/search/docs/appearance/structured-data/local-business
- https://developers.google.com/search/docs/appearance/structured-data/review-snippet
- https://developers.google.com/search/docs/appearance/structured-data/faqpage
- https://developers.google.com/search/docs/specialty/international/localized-versions
- https://schema.org/SportsActivityLocation · https://schema.org/SportsClub
- https://support.google.com/business/answer/3038177 · https://support.google.com/business/answer/7091
- https://developers.facebook.com/blog/post/2024/09/04/update-on-instagram-basic-display-api/
- https://developers.facebook.com/docs/instagram-platform/overview/
- https://developers.facebook.com/docs/instagram-platform/embed-button
- https://developers.facebook.com/docs/instagram-platform/oembed

**ElyFlame**
- https://elyflame.com/ · https://elyflame.com/?p=1
- https://gymnasticsus.com/gyms/gym-elyflame-academy-of-rhythmic-gymnastics-corp-buffalo-grove-il (вторичный)
- https://www.facebook.com/groups/BGSHOPLOCAL/posts/2301239096987823/
- https://www.facebook.com/profile.php?id=61573847340841
- https://www.instagram.com/elyflamerg_yuvkhimenko/ (требует логина)
- https://static.usagym.org/PDFs/Rhythmic/judging/judge_list.pdf
- https://columbiachronicle.com/campus/ukrainian-russian-and-polish-students-share-worries-for-home/ (связь с ElyFlame не проверена)
- https://srischicago.com/en/about-us (сайт на восстановлении)
