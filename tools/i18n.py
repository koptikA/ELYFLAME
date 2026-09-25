"""Build RU/UK pages from English sources registered in PAGES.

    python tools/i18n.py

HTML and ABOUT_HTML are shared translation tables; JS translates the shared script.
Each row must exist in at least one source. Every translated page is checked for
English leftovers, including coach JSON fields. Header/footer copies must match
after normalizing relative URLs and current-page markers. Language menus must
match their helper output. Checks finish before any generated files are written.

Add a directory to PAGES for the next page; copy the common shell with valid
relative links and same-page language menus. Assets stay at the site root;
translated shared scripts stay at each language root. Never edit ru/ or uk/ by hand.
In translations, ~ is a non-breaking space. Form option values stay English.
"""
import io
import os
import re
import sys
import posixpath
import json
from urllib.parse import urljoin, urlsplit, urlunsplit
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGS = {'ru': 1, 'uk': 2}
SITE = 'https://elyflame.com/'
# Add an English source directory here when the next standalone page is ready.
PAGES = ('', 'about/', 'stretching/', 'contact/', 'parents/')

# (English fragment exactly as in index.html, Russian, Ukrainian)
HTML = [
    ('<title>ElyFlame — Where Grace Meets Fire</title>',
     '<title>ElyFlame — академия художественной гимнастики в~Баффало-Гров</title>',
     '<title>ElyFlame — академія художньої гімнастики в~Баффало-Гров</title>'),
    ("content=\"Discover rhythmic gymnastics at ElyFlame Academy in Buffalo Grove. Find your child's starting point, explore our programs, and plan a trial lesson.\"",
     'content="Художественная гимнастика в~ElyFlame Academy, Баффало-Гров (Buffalo Grove, Иллинойс). Подберите уровень для ребёнка, узнайте о~программах и~запишитесь на~пробное занятие."',
     'content="Художня гімнастика в~ElyFlame Academy, Баффало-Гров (Buffalo Grove, Іллінойс). Підберіть рівень для дитини, дізнайтеся про програми й~запишіться на~пробне заняття."'),
    ('>Skip to content<', '>Перейти к~содержанию<', '>Перейти до вмісту<'),
    ('<span>$10 trial lesson · pay online or at the academy</span>', '<span>Пробное занятие~— 10~$ · оплата онлайн или в~академии</span>', '<span>Пробне заняття~— 10~$ · оплата онлайн або в~академії</span>'),
    ('<small>ACADEMY OF RHYTHMIC GYMNASTICS</small>', '<small>АКАДЕМИЯ ХУДОЖЕСТВЕННОЙ ГИМНАСТИКИ</small>', '<small>АКАДЕМІЯ ХУДОЖНЬОЇ ГІМНАСТИКИ</small>'),
    ('<span class="dot"></span> Buffalo Grove, Illinois<', '<span class="dot"></span> Баффало-Гров, Иллинойс<', '<span class="dot"></span> Баффало-Гров, Іллінойс<'),
    ('Find your first class <span', 'Подобрать группу <span', 'Підібрати групу <span'),
    ('aria-label="ElyFlame Academy home"', 'aria-label="ElyFlame Academy, на~главную"', 'aria-label="ElyFlame Academy, на~головну"'),
    ('aria-label="Menu"', 'aria-label="Меню"', 'aria-label="Меню"'),
    ('aria-label="Main navigation"', 'aria-label="Основное меню"', 'aria-label="Основне меню"'),
    ('>Home</a>', '>Главная</a>', '>Головна</a>'),
    ('>About</a>', '>Об академии</a>', '>Про академію</a>'),
    (">Parents' Info</a>", '>Родителям</a>', '>Батькам</a>'),
    ('>Stretching</a>', '>Растяжка</a>', '>Розтяжка</a>'),
    ('>Contact</a>', '>Контакты</a>', '>Контакти</a>'),
    ('class="button header-cta" href="#trial">Book a Trial <span', 'class="button header-cta" href="#trial">Записаться <span', 'class="button header-cta" href="#trial">Записатися <span'),
    ('Book a Trial <span aria-hidden="true">→</span>', 'Записаться на~пробное <span aria-hidden="true">→</span>', 'Записатися на~пробне <span aria-hidden="true">→</span>'),
    ('Artistry in motion. Confidence for life.', 'Искусство в~движении. Уверенность на~всю жизнь.', 'Мистецтво в~русі. Впевненість на~все життя.'),
    ('aria-label="Where grace meets fire."', 'aria-label="Где грация встречает огонь."', 'aria-label="Де грація зустрічає вогонь."'),
    # In Russian and Ukrainian the star closes the first line, so the second line starts at the left edge and the accent
    # word keeps its distance from the gymnast.
    ('<span data-reveal>Where grace</span><br><span class="second-line"><span class="hero-star" aria-hidden="true">✳</span><span data-reveal>meets</span> <em data-reveal-accent>fire.</em>',
     '<span data-reveal>Где грация</span><span class="hero-star" aria-hidden="true">✳</span><br><span class="second-line"><span data-reveal>встречает</span> <em data-reveal-accent>огонь.</em>',
     '<span data-reveal>Де грація</span><span class="hero-star" aria-hidden="true">✳</span><br><span class="second-line"><span data-reveal>зустрічає</span> <em data-reveal-accent>вогонь.</em>'),
    ('aria-label="Illustration of a young rhythmic gymnast with a ribbon"', 'aria-label="Иллюстрация: юная гимнастка с~лентой"', 'aria-label="Ілюстрація: юна гімнастка зі стрічкою"'),
    ('<p>Rhythmic gymnastics for girls 6 and up on the path to competition,<br>with first classes from age 3.</p>',
     '<p>Художественная гимнастика для девочек от~6~лет на~пути к~соревнованиям.<br>Первые занятия~— с~3~лет.</p>',
     '<p>Художня гімнастика для дівчаток від~6~років на~шляху до~змагань.<br>Перші заняття~— з~3~років.</p>'),
    ('<span class="trial-note">$10 trial lesson <i>·</i> the academy confirms your time</span>',
     '<span class="trial-note">Пробное занятие~— 10~$ <i>·</i> время подтвердит академия</span>',
     '<span class="trial-note">Пробне заняття~— 10~$ <i>·</i> час підтвердить академія</span>'),
    ('<span>Find the right class</span>', '<span>Найти свою группу</span>', '<span>Знайти свою групу</span>'),
    ('aria-label="Our approach"', 'aria-label="Наш подход"', 'aria-label="Наш підхід"'),
    ('<span>Small beginnings</span>', '<span>С~малого</span>', '<span>З~малого</span>'),
    ('<span>Beautiful movement</span>', '<span>Красота движения</span>', '<span>Краса руху</span>'),
    ('<span>Brave first steps</span>', '<span>Смелые первые шаги</span>', '<span>Сміливі перші кроки</span>'),
    ('<span>A personal path</span>', '<span>Свой путь</span>', '<span>Свій шлях</span>'),
    ('>The champion’s path<', '>Путь чемпионки<', '>Шлях чемпіонки<'),
    ('<h2>Every journey starts<br>with <em>one spark.</em></h2>', '<h2>Каждый путь<br>начинается <em>с~искры.</em></h2>', '<h2>Кожен шлях<br>починається <em>з~іскри.</em></h2>'),
    ('<p>Your child’s first steps or next challenge.<br>Let’s find a place to begin.</p>',
     '<p>Первые шаги ребёнка или новый вызов.<br>Подберём, с~чего начать.</p>',
     '<p>Перші кроки дитини чи новий виклик.<br>Підберемо, з~чого почати.</p>'),
    ('How old is your child?<select', 'Сколько лет ребёнку?<select', 'Скільки років дитині?<select'),
    ('>3 years<', '>3~года<', '>3~роки<'),
    ('>4 years<', '>4~года<', '>4~роки<'),
    ('>5 years<', '>5~лет<', '>5~років<'),
    ('>6 years<', '>6~лет<', '>6~років<'),
    ('>7 years<', '>7~лет<', '>7~років<'),
    ('>8 years<', '>8~лет<', '>8~років<'),
    ('>9 years<', '>9~лет<', '>9~років<'),
    ('>10 years or older<', '>10~лет и~старше<', '>10~років і~старше<'),
    ('Any rhythmic gymnastics experience?<select', 'Есть~ли опыт в~художественной гимнастике?<select', 'Чи є досвід у~художній гімнастиці?<select'),
    ('>A brand-new beginning<', '>Начинаем с~нуля<', '>Починаємо з~нуля<'),
    ('>Some recreational experience<', '>Есть любительский опыт<', '>Є аматорський досвід<'),
    ('>Competitive experience<', '>Выступали на~соревнованиях<', '>Виступали на~змаганнях<'),
    ('aria-label="Six levels of growth"', 'aria-label="Шесть уровней роста"', 'aria-label="Шість рівнів розвитку"'),
    ('>Possible starting point / Level 2<', '>Возможный старт / Уровень~2<', '>Можливий старт / Рівень~2<'),
    ('>Let curiosity lead.<', '>Пусть ведёт любопытство.<', '>Хай веде цікавість.<'),
    ('>Playful movement, growing confidence, and a first friendship with the rope and ball.<',
     '>Игра и~движение, растущая уверенность и~первая дружба со~скакалкой и~мячом.<',
     '>Гра й~рух, дедалі більша впевненість і~перша дружба зі~скакалкою та~м’ячем.<'),
    ('>Great start. The coach will check if your child is ready for the next step.<',
     '>Хорошее начало. Тренер посмотрит, готов~ли ребёнок к~следующему шагу.<',
     '>Гарний початок. Тренер подивиться, чи готова дитина до~наступного кроку.<'),
    ('<small>Your coach will confirm the right level at the trial.</small>',
     '<small>Уровень подтвердит тренер на~пробном занятии</small>',
     '<small>Рівень підтвердить тренер на~пробному занятті</small>'),
    ('>More than movement<', '>Больше, чем движение<', '>Більше, ніж рух<'),
    ('<h2>A little grace.<br>A lot of <em>possibility.</em></h2>', '<h2>Немного грации.<br>Много <em>возможностей.</em></h2>', '<h2>Трохи грації.<br>Багато <em>можливостей.</em></h2>'),
    ('<p>Part sport, part art: rhythmic gymnastics brings movement, music, and apparatus together, so strength and expression grow side by side.</p>',
     '<p>Наполовину спорт, наполовину искусство: художественная гимнастика соединяет движение, музыку и~предметы, поэтому сила и~выразительность растут вместе.</p>',
     '<p>Наполовину спорт, наполовину мистецтво: художня гімнастика поєднує рух, музику й~предмети, тож сила й~виразність зростають разом.</p>'),
    ('<h3>Discover what your child can do</h3>', '<h3>Узнайте, на~что способен ваш ребёнок</h3>', '<h3>Дізнайтеся, на~що здатна ваша дитина</h3>'),
    ('<p>Balance, coordination, and flexibility, one new skill at a time.</p>', '<p>Равновесие, координация и~гибкость~— шаг за~шагом.</p>', '<p>Рівновага, координація та~гнучкість~— крок за~кроком.</p>'),
    ('<h3>Find a personal rhythm</h3>', '<h3>Найдите свой ритм</h3>', '<h3>Знайдіть свій ритм</h3>'),
    ('<p>From playful exploration to the focus of a competitive routine.</p>',
     '<p>От~игры и~первых проб до~сосредоточенности соревновательной программы.</p>',
     '<p>Від~гри й~перших спроб до~зосередженості змагальної програми.</p>'),
    ('Explore your child&#8217;s path <span', 'Подобрать уровень для ребёнка <span', 'Підібрати рівень для дитини <span'),
    # Gallery and video (placeholders until the client's photos and video arrive)
    ('>Inside the academy<', '>Жизнь академии<', '>Життя академії<'),
    ('<h2>Practice, play,<br><em>perform.</em></h2>', '<h2>Учимся, играем,<br><em>выступаем.</em></h2>', '<h2>Вчимося, граємо,<br><em>виступаємо.</em></h2>'),
    ('>Follow us on Instagram <span', '>Мы в~Instagram <span', '>Ми в~Instagram <span'),
    ('aria-label="Photos from classes and performances"', 'aria-label="Фото с~занятий и~выступлений"', 'aria-label="Фото із~занять і~виступів"'),
    ('aria-label="Photo placeholder">Photo<', 'aria-label="Место для фото">Фото<', 'aria-label="Місце для фото">Фото<'),
    ('>On the carpet<', '>На~ковре<', '>На~килимі<'),
    ('<h2>See grace<br><em>in motion.</em></h2>', '<h2>Грация<br><em>в~движении.</em></h2>', '<h2>Грація<br><em>у~русі.</em></h2>'),
    # Coaches: the founder, then the team (cards come from the #team-data array; add rows here for each coach)
    ('>Our coaches<', '>Наши тренеры<', '>Наші тренери<'),
    ('<h2>Guidance with<br><em>heart and purpose.</em></h2>', '<h2>Наставники<br><em>с~душой и~целью.</em></h2>', '<h2>Наставники<br><em>з~душею та~метою.</em></h2>'),
    ('aria-label="Placeholder for the founder’s portrait"', 'aria-label="Место для портрета основательницы"', 'aria-label="Місце для портрета засновниці"'),
    ('>Yelizaveta Yuvkhimenko<', '>Елизавета Ювхименко<', '>Єлизавета Ювхіменко<'),
    ('<p class="founder-role">Founder and head coach</p>', '<p class="founder-role">Основательница и~главный тренер</p>', '<p class="founder-role">Засновниця й~головна тренерка</p>'),
    ('<p>A national judge with USA Gymnastics, Yelizaveta founded ElyFlame Academy to give girls in Buffalo Grove a clear path from their first steps to the competition floor.</p>',
     '<p>Национальный судья USA Gymnastics, Елизавета основала ElyFlame Academy, чтобы у~девочек из~Баффало-Грова был понятный путь от~первых шагов до~соревнований.</p>',
     '<p>Національна суддя USA Gymnastics, Єлизавета заснувала ElyFlame Academy, щоб дівчата з~Баффало-Грова мали зрозумілий шлях від~перших кроків до~змагань.</p>'),
    ('<p>[A sentence from Yelizaveta on why she coaches.]</p>', '<p>[Фраза Елизаветы о~том, почему она тренирует]</p>', '<p>[Фраза Єлизавети про~те, чому вона тренує]</p>'),
    ('>Meet your coach<', '>Ваш тренер<', '>Ваша тренерка<'),
    ('aria-label="Credentials"', 'aria-label="Квалификация"', 'aria-label="Кваліфікація"'),
    ('</svg>National judge, USA Gymnastics</li>', '</svg>Национальный судья USA Gymnastics</li>', '</svg>Національна суддя USA Gymnastics</li>'),
    ('</svg>Member club, USA Gymnastics</li>', '</svg>Клуб~— член USA Gymnastics</li>', '</svg>Клуб~— член USA Gymnastics</li>'),
    ('>The team<', '>Команда<', '>Команда<'),
    ('<p class="eyebrow">Stretching &amp; Flexibility</p>', '<p class="eyebrow">Растяжка и~гибкость</p>', '<p class="eyebrow">Розтяжка та~гнучкість</p>'),
    ('<h2>Great things<br>begin with<br><em>a stretch.</em></h2>', '<h2>Большое<br>начинается<br><em>с~растяжки.</em></h2>', '<h2>Велике<br>починається<br><em>з~розтяжки.</em></h2>'),
    ('<p>For dancers, skaters, and athletes from other sports, and for adults.</p>',
     '<p>Для танцоров, фигуристов, спортсменов из~других видов спорта и~взрослых.</p>',
     '<p>Для танцівників, фігуристів, спортсменів з~інших видів спорту й~дорослих.</p>'),
    ('<p class="muted">A weekly Stretching &amp; Flexibility class for teens, adults, and athletes from other sports.</p>',
     '<p class="muted">Занятие по~растяжке и~гибкости раз в~неделю для подростков, взрослых и~спортсменов из~других видов спорта.</p>',
     '<p class="muted">Заняття з~розтяжки та~гнучкості раз на~тиждень для підлітків, дорослих і~спортсменів з~інших видів спорту.</p>'),
    ('>For parents<', '>Родителям<', '>Батькам<'),
    ('<h2>Little questions.<br><em>Big beginnings.</em></h2>', '<h2>Маленькие вопросы.<br><em>Большие начинания.</em></h2>', '<h2>Маленькі питання.<br><em>Великі починання.</em></h2>'),
    ('<p>A new activity comes with questions.<br>Here’s a little clarity before you visit.</p>',
     '<p>У~нового занятия всегда есть вопросы.<br>Вот ответы до~первого визита.</p>',
     '<p>Нове заняття~— нові питання.<br>Ось відповіді до~першого візиту.</p>'),
    ('<summary>Does my child need experience?</summary>', '<summary>Нужен~ли ребёнку опыт?</summary>', '<summary>Чи потрібен дитині досвід?</summary>'),
    ('<p>No experience is needed to explore the recreational program. At the trial, the coach assesses age, skills, abilities, and strength to recommend a starting point.</p>',
     '<p>Для любительской программы опыт не~нужен. На~пробном занятии тренер оценит возраст, навыки, способности и~силу и~подскажет, с~чего начать.</p>',
     '<p>Для аматорської програми досвід не~потрібен. На~пробному занятті тренер оцінить вік, навички, здібності й~силу та~підкаже, з~чого почати.</p>'),
    ('<summary>How much is a trial lesson?</summary>', '<summary>Сколько стоит пробное занятие?</summary>', '<summary>Скільки коштує пробне заняття?</summary>'),
    ('<p>The trial lesson is $10. You can pay online when you book, or at the academy.</p>',
     '<p>Пробное занятие стоит 10~$. Оплатить можно онлайн при записи или в~академии.</p>',
     '<p>Пробне заняття коштує 10~$. Оплатити можна онлайн під час запису або в~академії.</p>'),
    ('<summary>What if we already have gymnastics experience?</summary>', '<summary>А~если опыт в~гимнастике уже есть?</summary>', '<summary>А~якщо досвід у~гімнастиці вже є?</summary>'),
    ('<p>Tell us about your child&#8217;s previous rhythmic gymnastics training when you get in touch. The trial helps the coach assess the right program and level.</p>',
     '<p>Когда будете записываться, расскажите, где и~как ребёнок занимался раньше. Пробное занятие поможет тренеру подобрать программу и~уровень.</p>',
     '<p>Коли записуватиметеся, розкажіть, де і~як дитина займалася раніше. Пробне заняття допоможе тренеру підібрати програму й~рівень.</p>'),
    ('<summary>Can teens and adults join?</summary>', '<summary>Могут~ли заниматься подростки и~взрослые?</summary>', '<summary>Чи можуть займатися підлітки й~дорослі?</summary>'),
    ('<p>Yes. Stretching &amp; Flexibility is a weekly class open to teens, adults, and athletes from other sports.</p>',
     '<p>Да. Раз в~неделю проходит занятие по~растяжке и~гибкости для подростков, взрослых и~спортсменов из~других видов спорта.</p>',
     '<p>Так. Раз на~тиждень проходить заняття з~розтяжки та~гнучкості для підлітків, дорослих і~спортсменів з~інших видів спорту.</p>'),
    ('<summary>Can parents watch?</summary>', '<summary>Можно~ли родителям смотреть занятия?</summary>', '<summary>Чи можуть батьки дивитися заняття?</summary>'),
    ('<p>You can watch your child’s trial. After that, parents attend with the Head Coach’s permission, at open practices, or as volunteers.</p>',
     '<p>Вы можете посмотреть пробное занятие ребёнка. Дальше~— с~разрешения главного тренера, на~открытых тренировках или в~качестве волонтёра.</p>',
     '<p>Ви можете подивитися пробне заняття дитини. Далі~— з~дозволу головного тренера, на~відкритих тренуваннях або як~волонтер.</p>'),
    ('<summary>How do we register after the trial?</summary>', '<summary>Как записаться после пробного?</summary>', '<summary>Як записатися після пробного?</summary>'),
    ('<p>After your child’s trial, the Head Coach sends an Adobe registration link. Your child can join practice only after the form is complete and the first payment is made.</p>',
     '<p>После пробного главный тренер пришлёт ссылку на~форму регистрации в~Adobe. Ребёнок сможет заниматься только после заполнения формы и~первого платежа.</p>',
     '<p>Після пробного головний тренер надішле посилання на~форму реєстрації в~Adobe. Дитина зможе займатися лише після заповнення форми й~першого платежу.</p>'),
    ('>Visit us<', '>Приходите<', '>Приходьте<'),
    ('<h2>See you<br><em>in Buffalo Grove.</em></h2>', '<h2>До встречи<br><em>в~Баффало-Гров.</em></h2>', '<h2>До зустрічі<br><em>у~Баффало-Гров.</em></h2>'),
    ('>Silk Road International School building<', '>Здание Silk Road International School<', '>Будівля Silk Road International School<'),
    ('Get directions <span', 'Проложить маршрут <span', 'Прокласти маршрут <span'),
    ('>Calls: Mon–Fri 9 am–10 pm, Sat 9 am–5 pm, Sun closed<', '>Звонки: пн–пт 9:00–22:00, сб 9:00–17:00, вс~— выходной<', '>Дзвінки: пн–пт 9:00–22:00, сб 9:00–17:00, нд~— вихідний<'),
    ('>Entrance, parking, drop-off and pick-up: door #11<', '>Вход, парковка, где оставить и~забрать ребёнка: дверь №~11<', '>Вхід, парковка, де залишити й~забрати дитину: двері №~11<'),
    ('>Her story is just beginning.<', '>Её история только начинается.<', '>Її історія тільки починається.<'),
    ('<h2>Let’s light <em>the spark.</em></h2>', '<h2>Зажжём <em>искру.</em></h2>', '<h2>Запалимо <em>іскру.</em></h2>'),
    ('<p>Tell us about your child, pick a trial time, and pay the $10 fee online. The academy confirms every trial.</p>',
     '<p>Расскажите о~ребёнке, выберите время пробного занятия и~оплатите 10~$ онлайн. Академия подтвердит каждую запись.</p>',
     '<p>Розкажіть про дитину, оберіть час пробного заняття й~оплатіть 10~$ онлайн. Академія підтвердить кожен запис.</p>'),
    ('Questions first? Write to <a', 'Есть вопросы? Напишите на~<a', 'Є питання? Напишіть на~<a'),
    ('>Your first step / $10 trial lesson<', '>Первый шаг / Пробное занятие за~10~$<', '>Перший крок / Пробне заняття за~10~$<'),
    ('<h2>A new beginning<br><em>starts here.</em></h2>', '<h2>Всё начинается<br><em>здесь.</em></h2>', '<h2>Усе починається<br><em>тут.</em></h2>'),
    ('<h2 id="booking-title">Book a Trial</h2>', '<h2 id="booking-title">Запись на~пробное занятие</h2>', '<h2 id="booking-title">Запис на~пробне заняття</h2>'),
    ('>Prototype preview — nothing is sent, paid, or reserved. Times shown are samples.<',
     '>Прототип: ничего не~отправляется, не~оплачивается и~не~бронируется. Время указано для примера.<',
     '>Прототип: нічого не~надсилається, не~оплачується й~не~бронюється. Час указано для прикладу.<'),
    ('>There is a problem<', '>Не~все поля заполнены верно<', '>Не~всі поля заповнено правильно<'),
    ('>Your child’s name<', '>Имя ребёнка<', '>Ім’я дитини<'),
    ('>Your child’s age<', '>Возраст ребёнка<', '>Вік дитини<'),
    ('>Rhythmic gymnastics experience<', '>Опыт в~художественной гимнастике<', '>Досвід у~художній гімнастиці<'),
    ('<option value="none">None</option>', '<option value="none">Нет</option>', '<option value="none">Немає</option>'),
    ('<option value="some">Some recreational</option>', '<option value="some">Любительский</option>', '<option value="some">Аматорський</option>'),
    ('<option value="competitive">Competitive</option>', '<option value="competitive">Соревновательный</option>', '<option value="competitive">Змагальний</option>'),
    ('<label for="program">Program</label>', '<label for="program">Программа</label>', '<label for="program">Програма</label>'),
    ('<option value="Recreational">Recreational</option>', '<option value="Recreational">Любительская</option>', '<option value="Recreational">Аматорська</option>'),
    ('<option value="Competitive">Competitive</option>', '<option value="Competitive">Соревновательная</option>', '<option value="Competitive">Змагальна</option>'),
    ('<option value="Stretching &amp; Flexibility">Stretching &amp; Flexibility</option>', '<option value="Stretching &amp; Flexibility">Растяжка и~гибкость</option>', '<option value="Stretching &amp; Flexibility">Розтяжка та~гнучкість</option>'),
    ('>Trial day and time<', '>День и~время пробного<', '>День і~час пробного<'),
    ('<option value="">Select a trial time</option>', '<option value="">Выберите время</option>', '<option value="">Оберіть час</option>'),
    ('>Tuesday 6:00 PM [sample]<', '>Вторник, 18:00 [пример]<', '>Вівторок, 18:00 [приклад]<'),
    ('>Thursday 6:00 PM [sample]<', '>Четверг, 18:00 [пример]<', '>Четвер, 18:00 [приклад]<'),
    ('>Monday 5:00 PM [sample]<', '>Понедельник, 17:00 [пример]<', '>Понеділок, 17:00 [приклад]<'),
    ('>Friday 7:00 PM [sample]<', '>Пятница, 19:00 [пример]<', '>П’ятниця, 19:00 [приклад]<'),
    ('>Sample times; the academy confirms every trial.<', '>Время для примера, академия подтверждает каждую запись<', '>Час для прикладу, академія підтверджує кожен запис<'),
    ('<legend>Trial fee: $10</legend>', '<legend>Пробное занятие: 10~$</legend>', '<legend>Пробне заняття: 10~$</legend>'),
    ('<span>Pay online now (recommended)</span>', '<span>Оплатить онлайн сейчас (рекомендуем)</span>', '<span>Оплатити онлайн зараз (радимо)</span>'),
    ('<span>Pay at the academy</span>', '<span>Оплатить в~академии</span>', '<span>Оплатити в~академії</span>'),
    ('>Parent’s name<', '>Ваше имя<', '>Ваше ім’я<'),
    ('<label for="phone">Phone number</label>', '<label for="phone">Телефон</label>', '<label for="phone">Телефон</label>'),
    ('>A 10-digit US phone number.<', '>Номер в~США, 10~цифр<', '>Номер у~США, 10~цифр<'),
    ('<label for="email">Email</label>', '<label for="email">Эл. почта</label>', '<label for="email">Ел. пошта</label>'),
    ('<span>I agree to be contacted about my child’s trial lesson.</span>', '<span>Разрешаю связаться со~мной по~поводу пробного занятия</span>', '<span>Дозволяю зв’язатися зі~мною щодо пробного заняття</span>'),
    ('<span class="submit-label">Book a Trial</span>', '<span class="submit-label">Записаться</span>', '<span class="submit-label">Записатися</span>'),
    ('<p class="eyebrow">A new beginning</p>', '<p class="eyebrow">Новое начало</p>', '<p class="eyebrow">Новий початок</p>'),
    ('>Your trial request is in.<', '>Заявка на~пробное занятие отправлена.<', '>Заявку на~пробне заняття надіслано.<'),
    ("<p>The academy will confirm your trial time within 24 hours. If the time doesn't work, they'll text you to find another.</p>",
     '<p>Академия подтвердит время в~течение 24~часов. Если время не~подойдёт, вам напишут SMS и~предложат другое.</p>',
     '<p>Академія підтвердить час протягом 24~годин. Якщо час не~підійде, вам напишуть SMS і~запропонують інший.</p>'),
    ('>Prototype confirmation only — no booking was sent or reserved.<', '>Это прототип: заявка никуда не~отправлена, время не~забронировано<', '>Це прототип: заявку нікуди не~надіслано, час не~заброньовано<'),
    ('<h3>Your trial details</h3>', '<h3>Данные записи</h3>', '<h3>Дані запису</h3>'),
    ('<h3>What to bring</h3>', '<h3>Что взять с~собой</h3>', '<h3>Що взяти з~собою</h3>'),
    ('<li>[Comfortable exercise clothes — confirm]</li>', '<li>[Удобная спортивная одежда~— уточнить]</li>', '<li>[Зручний спортивний одяг~— уточнити]</li>'),
    ('<li>[Water bottle — confirm]</li>', '<li>[Бутылка воды~— уточнить]</li>', '<li>[Пляшка води~— уточнити]</li>'),
    ('<li>[Required footwear or equipment — confirm]</li>', '<li>[Обувь или инвентарь~— уточнить]</li>', '<li>[Взуття чи інвентар~— уточнити]</li>'),
    ('>Edit your details<', '>Изменить данные<', '>Змінити дані<'),
    ('alt="ElyFlame Academy of Rhythmic Gymnastics"', 'alt="ElyFlame Academy, академия художественной гимнастики"', 'alt="ElyFlame Academy, академія художньої гімнастики"'),
    ('<p>Where grace meets fire.</p>', '<p>Где грация встречает огонь.</p>', '<p>Де грація зустрічає вогонь.</p>'),
    ('<p>Calls: Mon–Fri 9 am–10 pm<br>Sat 9 am–5 pm · Sun closed</p>', '<p>Звонки: пн–пт 9:00–22:00<br>сб 9:00–17:00 · вс~— выходной</p>', '<p>Дзвінки: пн–пт 9:00–22:00<br>сб 9:00–17:00 · нд~— вихідний</p>'),
    ('aria-label="Footer navigation"', 'aria-label="Разделы сайта"', 'aria-label="Розділи сайту"'),
    ('aria-label="Legal"', 'aria-label="Правовая информация"', 'aria-label="Правова інформація"'),
    ('>Privacy Policy<', '>Политика конфиденциальности<', '>Політика конфіденційності<'),
    ('>Terms of Use<', '>Условия использования<', '>Умови використання<'),
    ('Site by Kirakito Technologies', 'Сайт~— Kirakito Technologies', 'Сайт~— Kirakito Technologies'),
    ('aria-label="Close trial booking"', 'aria-label="Закрыть запись"', 'aria-label="Закрити запис"'),
]

# (English string literal exactly as in site.js, with its quotes, Russian, Ukrainian)
JS = [
    ("'First steps'", "'Первые шаги'", "'Перші кроки'"),
    ("'Find a rhythm'", "'Свой ритм'", "'Свій ритм'"),
    ("'Build a base'", "'Основа'", "'Основа'"),
    ("'Grow stronger'", "'Сила'", "'Сила'"),
    ("'Find expression'", "'Выразительность'", "'Виразність'"),
    ("'Take the stage'", "'На~ковёр'", "'На~килим'"),
    ("'Age 3'", "'3~года'", "'3~роки'"),
    ("'Ages 4–5'", "'4–5~лет'", "'4–5~років'"),
    ("'Ages 6–7'", "'6–7~лет'", "'6–7~років'"),
    ("'Ages 6+'", "'от~6~лет'", "'від~6~років'"),
    ("'Ages 7+'", "'от~7~лет'", "'від~7~років'"),
    ("'Ages 8+'", "'от~8~лет'", "'від~8~років'"),
    ("'Rope'", "'Скакалка'", "'Скакалка'"),
    ("'Rope, ball'", "'Скакалка, мяч'", "'Скакалка, м’яч'"),
    ("'Rope, ball, hoop'", "'Скакалка, мяч, обруч'", "'Скакалка, м’яч, обруч'"),
    ("'+ Clubs'", "'+~булавы'", "'+~булави'"),
    ("'+ Ribbon (all five)'", "'+~лента (все пять)'", "'+~стрічка (усі п’ять)'"),
    ("'All apparatus'", "'Все предметы'", "'Усі предмети'"),
    ("'A little spark of something big.'", "'Маленькая искра большого пути.'", "'Маленька іскра великого шляху.'"),
    ("'Let curiosity lead.'", "'Пусть ведёт любопытство.'", "'Хай веде цікавість.'"),
    ("'A new chapter begins.'", "'Начинается новая глава.'", "'Починається новий розділ.'"),
    ("'Make room for the next challenge.'", "'Место для нового вызова.'", "'Місце для нового виклику.'"),
    ("'Let expression unfold.'", "'Пусть раскроется выразительность.'", "'Хай розкриється виразність.'"),
    ("'Bring ambition to the floor.'", "'Амбиции~— на~ковёр.'", "'Амбіції~— на~килим.'"),
    ("'An introduction to movement, coordination, and playful exploration with the rope.'",
     "'Знакомство с~движением, координацией и~скакалкой в~игре.'",
     "'Знайомство з~рухом, координацією та~скакалкою в~грі.'"),
    ("'Playful movement, growing confidence, and a first friendship with the rope and ball.'",
     "'Игра и~движение, растущая уверенность и~первая дружба со~скакалкой и~мячом.'",
     "'Гра й~рух, дедалі більша впевненість і~перша дружба зі~скакалкою та~м’ячем.'"),
    ("'Rope, ball, and hoop come together as athletes begin preparing for competition.'",
     "'Скакалка, мяч и~обруч вместе: гимнастки начинают готовиться к~соревнованиям.'",
     "'Скакалка, м’яч і~обруч разом: гімнастки починають готуватися до~змагань.'"),
    ("'Clubs join the repertoire, with a continued focus on stretching and apparatus skills.'",
     "'Добавляются булавы, а~растяжка и~работа с~предметами остаются в~центре внимания.'",
     "'Додаються булави, а~розтяжка й~робота з~предметами лишаються в~центрі уваги.'"),
    ("'The ribbon completes the apparatus repertoire as skills and flexibility develop.'",
     "'Лента завершает набор предметов, пока растут навыки и~гибкость.'",
     "'Стрічка доповнює набір предметів, поки зростають навички й~гнучкість.'"),
    ("'A pathway toward serious competitive gymnastics, with placement assessed by the coach.'",
     "'Путь к~серьёзной соревновательной гимнастике, уровень определяет тренер.'",
     "'Шлях до~серйозної змагальної гімнастики, рівень визначає тренер.'"),
    ('>Start with a coach assessment<', '>Начнём с~оценки тренера<', '>Почнемо з~оцінки тренера<'),
    ("'Starting point / Coach assessment'", "'Старт / Оценка тренера'", "'Старт / Оцінка тренера'"),
    ('`Possible starting point / Level ${', '`Возможный старт / Уровень~${', '`Можливий старт / Рівень~${'),
    ("'Every path is individual.'", "'У~каждого свой путь.'", "'У~кожного свій шлях.'"),
    ('"Age is only part of the picture. Tell us about your child\'s experience, and the coach will help find a suitable starting level at the trial."',
     '"Возраст~— только часть картины. Расскажите об~опыте ребёнка, и~на~пробном занятии тренер поможет подобрать уровень."',
     '"Вік~— лише частина картини. Розкажіть про досвід дитини, і~на~пробному занятті тренер допоможе підібрати рівень."'),
    ("'Monday 5:00 PM'", "'Понедельник, 17:00'", "'Понеділок, 17:00'"),
    ("'Wednesday 5:00 PM'", "'Среда, 17:00'", "'Середа, 17:00'"),
    ("'Tuesday 6:00 PM'", "'Вторник, 18:00'", "'Вівторок, 18:00'"),
    ("'Thursday 6:00 PM'", "'Четверг, 18:00'", "'Четвер, 18:00'"),
    ("'Friday 7:00 PM'", "'Пятница, 19:00'", "'П’ятниця, 19:00'"),
    ('} [sample]`', '} [пример]`', '} [приклад]`'),
    ("'Select a trial time'", "'Выберите время'", "'Оберіть час'"),
    ('"Enter your child\'s name using 2 to 50 characters"', '"Введите имя ребёнка: от~2 до~50 символов"', '"Введіть ім’я дитини: від~2 до~50 символів"'),
    ('"Enter your child\'s age"', '"Введите возраст ребёнка"', '"Введіть вік дитини"'),
    ('"Enter your child\'s age as a whole number from 3 to 99"', '"Введите возраст ребёнка целым числом от~3 до~99"', '"Введіть вік дитини цілим числом від~3 до~99"'),
    ('"Select your child\'s gymnastics experience"', '"Выберите опыт ребёнка в~гимнастике"', '"Оберіть досвід дитини в~гімнастиці"'),
    ("'Select a program'", "'Выберите программу'", "'Оберіть програму'"),
    ("'Select a trial time for this program'", "'Выберите время пробного для этой программы'", "'Оберіть час пробного для цієї програми'"),
    ("'Enter the parent’s name using 2 to 80 characters'", "'Введите ваше имя: от~2 до~80 символов'", "'Введіть ваше ім’я: від~2 до~80 символів'"),
    ("'Enter a 10-digit US phone number'", "'Введите номер телефона в~США из~10~цифр'", "'Введіть номер телефону в~США з~10~цифр'"),
    ("'Enter an email address, like name@example.com'", "'Введите адрес эл. почты, например name@example.com'", "'Введіть адресу ел. пошти, наприклад name@example.com'"),
    ("'Agree to be contacted about the trial lesson'", "'Отметьте согласие на~связь по~поводу пробного занятия'", "'Позначте згоду на~зв’язок щодо пробного заняття'"),
    ("['Child',", "['Ребёнок',", "['Дитина',"),
    ("['Age',", "['Возраст',", "['Вік',"),
    ("['Experience',", "['Опыт',", "['Досвід',"),
    ("['Program',", "['Программа',", "['Програма',"),
    ("['Trial time',", "['Время',", "['Час',"),
    ("['Payment',", "['Оплата',", "['Оплата',"),
    ("'$10 online (prototype: Stripe Checkout goes here)'", "'10~$ онлайн (в~прототипе здесь будет Stripe Checkout)'", "'10~$ онлайн (у~прототипі тут буде Stripe Checkout)'"),
    ("'$10 at the academy'", "'10~$ в~академии'", "'10~$ в~академії'"),
    ("['Parent',", "['Ваше имя',", "['Ваше ім’я',"),
    ("['Phone',", "['Телефон',", "['Телефон',"),
    ("['Email',", "['Эл. почта',", "['Ел. пошта',"),
    ("textContent='Book a Trial'", "textContent='Записаться'", "textContent='Записатися'"),
    ("'Booking…'", "'Отправляем…'", "'Надсилаємо…'"),
    ("'Check the highlighted fields.'", "'Проверьте отмеченные поля'", "'Перевірте позначені поля'"),
    ("'Preparing your prototype confirmation…'", "'Готовим подтверждение прототипа…'", "'Готуємо підтвердження прототипу…'"),
    ("'Something went wrong. Your details are still here. Please try again.'",
     "'Не~получилось отправить. Данные сохранены, попробуйте ещё раз.'",
     "'Не~вдалося надіслати. Дані збережено, спробуйте ще раз.'"),
]

# Latin text that stays on translated pages: names, the postal address, contacts. In running text and headings the town is
# written in Cyrillic (Баффало-Гров); the address keeps Latin so parents can type it into a map.
KEEP = ['Adobe', 'PDF', 'Google Maps', 'ElyFlame Academy', 'ElyFlame', 'ELYFLAME', 'Buffalo Grove',
        'Radcliffe Road', 'Silk Road International School', 'USA Gymnastics', 'Instagram', 'Facebook',
        'Kirakito Technologies', 'academy@elyflame.com', 'name@example.com', 'Stripe Checkout', 'SMS',
        'English', 'Stretching & Flexibility']

# Shared page copy; rows are checked across all English sources in PAGES.
ABOUT_HTML = [('About ElyFlame — Rhythmic Gymnastics Academy',
  'Об~ElyFlame — академия художественной гимнастики',
  'Про ElyFlame — академія художньої гімнастики'),
 ("Meet ElyFlame Academy: rhythmic gymnastics, our coaches, our training space, and your child's path from "
  'first steps to competition.',
  'Знакомство с~ElyFlame Academy: художественная гимнастика, тренеры, зал и~путь ребёнка от~первых шагов '
  'до~соревнований.',
  'Знайомство з~ElyFlame Academy: художня гімнастика, тренери, зал і~шлях дитини від перших кроків '
  'до~змагань.'),
 ('Meet the coaches <span', 'Познакомиться с~тренерами <span', 'Познайомитися з~тренерами <span'),
 ('About ElyFlame / Buffalo Grove, Illinois',
  'Об~ElyFlame / Баффало-Гров, Иллинойс',
  'Про ElyFlame / Баффало-Гров, Іллінойс'),
 ('<h1>A sport.<br>An art.<br><em>A place to begin.</em></h1>',
  '<h1>Спорт.<br>Искусство.<br><em>Начало пути.</em></h1>',
  '<h1>Спорт.<br>Мистецтво.<br><em>Початок шляху.</em></h1>'),
 ('Movement meets music. A rope, a hoop, a ball, a pair of clubs, a ribbon. And at the center of it all: your '
  'child.',
  'Движение под музыку. Скакалка, обруч, мяч, булавы, лента. И~ребёнок, который учится с~ними работать.',
  'Рух під музику. Скакалка, обруч, м’яч, булави, стрічка. І~дитина, яка вчиться з~ними працювати.'),
 ('Discover the sport <span', 'Узнать о~гимнастике <span', 'Дізнатися про гімнастику <span'),
 ('aria-label="On this page"', 'aria-label="На этой странице"', 'aria-label="На цій сторінці"'),
 ('>The sport<', '>Гимнастика<', '>Гімнастика<'),
 ('>Our story<', '>Наша история<', '>Наша історія<'),
 ('>Our coaches<', '>Наши тренеры<', '>Наші тренери<'),
 ('>Our space<', '>Наш зал<', '>Наш зал<'),
 ('>Achievements<', '>Достижения<', '>Досягнення<'),
 ('>Rhythmic gymnastics<', '>Художественная гимнастика<', '>Художня гімнастика<'),
 ('<h2>Five apparatus.<br>A world of movement.</h2>',
  '<h2>Пять предметов.<br>Мир движения.</h2>',
  '<h2>П’ять предметів.<br>Світ руху.</h2>'),
 ('Rhythmic gymnastics brings together movement, music and apparatus. An Olympic sport since 1984, it makes '
  'room for both athletic skill and artistic expression.',
  'Художественная гимнастика соединяет движение, музыку и~работу с~предметами. Олимпийский вид спорта '
  'с~1984~года, в~котором важны и~спортивное мастерство, и~выразительность.',
  'Художня гімнастика поєднує рух, музику й~роботу з~предметами. Олімпійський вид спорту з~1984~року, в~якому '
  'важливі і~спортивна майстерність, і~виразність.'),
 ('>Rope<', '>Скакалка<', '>Скакалка<'),
 ('>Hoop<', '>Обруч<', '>Обруч<'),
 ('>Ball<', '>Мяч<', '>М’яч<'),
 ('>Clubs<', '>Булавы<', '>Булави<'),
 ('>Ribbon<', '>Лента<', '>Стрічка<'),
 ('Jump. Find a rhythm.', 'Прыгать. Чувствовать ритм.', 'Стрибати. Відчувати ритм.'),
 ('Roll. Turn. Explore space.',
  'Катить. Вращать. Осваивать пространство.',
  'Котити. Обертати. Освоювати простір.'),
 ('Balance. Throw. Catch.', 'Держать равновесие. Бросать. Ловить.', 'Тримати рівновагу. Кидати. Ловити.'),
 ('Two hands. One movement.', 'Две руки. Одно движение.', 'Дві руки. Один рух.'),
 ('Draw a shape in the air.', 'Рисовать в~воздухе.', 'Малювати в~повітрі.'),
 ('Balance and coordination', 'Равновесие и~координация', 'Рівновага й~координація'),
 ('Strength and flexibility', 'Сила и~гибкость', 'Сила й~гнучкість'),
 ('Focus and expression', 'Внимание и~выразительность', 'Увага й~виразність'),
 ('>Why ElyFlame<', '>Почему ElyFlame<', '>Чому ElyFlame<'),
 ('<h2>First steps.<br>Room to grow.</h2>',
  '<h2>Первые шаги.<br>Пространство для роста.</h2>',
  '<h2>Перші кроки.<br>Простір для зростання.</h2>'),
 ('Six levels connect the first introduction to rhythmic gymnastics with a path toward competition. Your '
  'child’s starting level is chosen by the coach at the trial.',
  'Шесть уровней~— от~знакомства с~художественной гимнастикой до~подготовки к~соревнованиям. С~какого уровня '
  'начнёт ребёнок, решит тренер на~пробном занятии.',
  'Шість рівнів~— від знайомства з~художньою гімнастикою до~підготовки до~змагань. З~якого рівня почне дитина, '
  'вирішить тренер на~пробному занятті.'),
 ('Find your child’s starting point <span',
  'Подобрать группу для ребёнка <span',
  'Підібрати групу для дитини <span'),
 ('A coach-led beginning', 'Начало с~тренером', 'Початок із~тренером'),
 ('Age is one part of the picture. Skills, experience and abilities help the coach choose a starting point for '
  'your child.',
  'Тренер учитывает не~только возраст, но~и~навыки, опыт и~способности ребёнка.',
  'Тренер враховує не~лише вік, а~й~навички, досвід і~здібності дитини.'),
 ('A judge’s perspective', 'Взгляд судьи', 'Погляд судді'),
 ('Our founder is a national judge with USA Gymnastics. ElyFlame Academy is a USA Gymnastics member club.',
  'Основательница академии~— национальный судья USA Gymnastics. ElyFlame Academy~— клуб~— член USA Gymnastics.',
  'Засновниця академії~— національна суддя USA Gymnastics. ElyFlame Academy~— клуб~— член USA Gymnastics.'),
 ('Our story &amp; mission', 'История и~миссия', 'Історія та~місія'),
 ('[The story behind ElyFlame.]', '[История ElyFlame.]', '[Історія ElyFlame.]'),
 ('[How the academy began and the mission that guides its coaching.]',
  '[Как появилась академия и~какая миссия определяет её работу.]',
  '[Як виникла академія та~яка місія визначає її роботу.]'),
 ('>Read more<', '>Подробнее<', '>Докладніше<'),
 ('[Founder biography, experience and achievements.]',
  '[Биография, опыт и~достижения основательницы.]',
  '[Біографія, досвід і~досягнення засновниці.]'),
 ('Coach certifications are available on a parent’s request.',
  'Сертификаты тренеров предоставляются по~запросу родителя.',
  'Сертифікати тренерів надаються на~запит батьків.'),
 ('>Inside the academy.<', '>Внутри академии.<', '>Усередині академії.<'),
 ('[Training space photo]', '[Фото зала]', '[Фото залу]'),
 ('[Equipment photo]', '[Фото оборудования]', '[Фото обладнання]'),
 ('Room to practice', 'Место для тренировок', 'Місце для тренувань'),
 ('[Training floor, apparatus and equipment details.]',
  '[Покрытие зала, предметы и~оборудование.]',
  '[Покриття залу, предмети та~обладнання.]'),
 ('[Safety arrangements in the training space.]', '[Меры безопасности в~зале.]', '[Заходи безпеки в~залі.]'),
 ('Your first visit', 'Первый визит', 'Перший візит'),
 ('Use door #11 for entrance, drop-off and pick-up.',
  'Вход, высадка и~встреча детей~— дверь №~11.',
  'Вхід, висадка та~зустріч дітей~— двері №~11.'),
 ('You can watch your child’s trial. After that, parents attend with the Head Coach’s permission, at open '
  'practices, or as volunteers.',
  'Вы можете посмотреть пробное занятие ребёнка. Дальше~— с~разрешения главного тренера, на~открытых '
  'тренировках или в~качестве волонтёра.',
  'Ви можете подивитися пробне заняття дитини. Далі~— з~дозволу головного тренера, на~відкритих тренуваннях '
  'або як~волонтер.'),
 ('Moments to remember.', 'Моменты, которые запомним.', 'Миті, які запам’ятаємо.'),
 ('[Year]', '[Год]', '[Рік]'),
 ('[Competition name]', '[Название соревнования]', '[Назва змагання]'),
 ('[Result, category and level.]', '[Результат, категория и~уровень.]', '[Результат, категорія та~рівень.]'),
 ('Your child’s first chapter', 'Начало пути ребёнка', 'Початок шляху дитини'),
 ('Come meet us.', 'Приходите знакомиться.', 'Приходьте знайомитися.'),
 ('Meet the coach, explore rhythmic gymnastics, and find a starting point for your child.',
  'Познакомьтесь с~тренером, попробуйте художественную гимнастику и~узнайте, с~чего начать ребёнку.',
  'Познайомтеся з~тренером, спробуйте художню гімнастику й~дізнайтеся, з~чого почати дитині.')]

STRETCHING_HTML = [('Stretching & Flexibility — ElyFlame Academy',
  'Растяжка и~гибкость — ElyFlame Academy',
  'Розтяжка та~гнучкість — ElyFlame Academy'),
 ('A weekly Stretching and Flexibility class at ElyFlame in Buffalo Grove for teens, adults, dancers, skaters and '
  'athletes from other sports.',
  'Растяжка в~ElyFlame, Баффало-Гров: еженедельное занятие для подростков, взрослых, танцоров, фигуристов '
  'и~спортсменов из~других видов спорта.',
  'Розтяжка в~ElyFlame, Баффало-Гров: щотижневе заняття для підлітків, дорослих, танцівників, фігуристів '
  'і~спортсменів з~інших видів спорту.'),
 ('<h1>Make room<br>for movement.</h1>',
  '<h1>Больше места<br>для движения.</h1>',
  '<h1>Більше місця<br>для руху.</h1>'),
 ('Explore Stretching <span', 'Подробнее о~растяжке <span', 'Докладніше про розтяжку <span'),
 ('>Who it’s for<', '>Для кого<', '>Для кого<'),
 ('>Teens &amp; adults<', '>Подростки и~взрослые<', '>Підлітки й~дорослі<'),
 ('>The class<', '>О~занятии<', '>Про заняття<'),
 ('<h2>Time to<br>stretch.</h2>', '<h2>Время<br>для растяжки.</h2>', '<h2>Час<br>для розтяжки.</h2>'),
 ('Stretching is a way to work on flexibility and explore your range of movement.',
  'Растяжка помогает работать над гибкостью и~изучать амплитуду своих движений.',
  'Розтяжка допомагає працювати над гнучкістю та~досліджувати амплітуду своїх рухів.'),
 ('>Frequency<', '>Частота<', '>Частота<'),
 ('>Once a week<', '>Раз в~неделю<', '>Раз на~тиждень<'),
 ('>Schedule<', '>Расписание<', '>Розклад<'),
 ('[Ask the academy for current class times.]',
  '[Время занятий уточняйте в~академии.]',
  '[Час занять уточнюйте в~академії.]'),
 ('>Duration &amp; starting level<', '>Длительность и~уровень подготовки<', '>Тривалість і~рівень підготовки<'),
 ('[Class duration and entry requirements.]',
  '[Длительность занятия и~требования к~подготовке.]',
  '[Тривалість заняття та~вимоги до~підготовки.]'),
 ('>How the class works<', '>Как проходит занятие<', '>Як проходить заняття<'),
 ('[Class structure, exercises and coaching approach.]',
  '[Структура занятия, упражнения и~подход тренера.]',
  '[Структура заняття, вправи та~підхід тренера.]'),
 ('>Start with a conversation<', '>Начните со~знакомства<', '>Почніть зі~знайомства<'),
 ('<h2>Find your<br>way in.</h2>', '<h2>Найдите<br>свой старт.</h2>', '<h2>Знайдіть<br>свій старт.</h2>'),
 ('Ask the academy about joining the weekly class, or choose Stretching &amp; Flexibility when booking a trial.',
  'Уточните в~академии, как присоединиться к~занятию, или выберите растяжку при записи на~пробное.',
  'Уточніть в~академії, як долучитися до~заняття, або виберіть розтяжку під час запису на~пробне.')]

CONTACT_HTML = [('Contact ElyFlame — Visit Us in Buffalo Grove',
  'Контакты ElyFlame — как добраться в~Баффало-Гров',
  'Контакти ElyFlame — як дістатися в~Баффало-Гров'),
 ('Contact ElyFlame Academy in Buffalo Grove: phone, email, call hours and directions to door 11 at 1250 '
  'Radcliffe Road.',
  'Контакты ElyFlame Academy в~Баффало-Гров: телефон, почта, часы звонков и~вход №~11 по~адресу 1250 Radcliffe '
  'Road.',
  'Контакти ElyFlame Academy в~Баффало-Гров: телефон, пошта, години дзвінків і~вхід №~11 за~адресою 1250 '
  'Radcliffe Road.'),
 ('>Contact ElyFlame<', '>Контакты ElyFlame<', '>Контакти ElyFlame<'),
 ('Questions before your child’s first visit? Call or write to the academy.',
  'Есть вопросы перед первым визитом ребёнка? Позвоните или напишите в~академию.',
  'Є~запитання перед першим візитом дитини? Зателефонуйте або напишіть до~академії.'),
 ('>Plan your visit<', '>Перед визитом<', '>Перед візитом<'),
 ('Plan your visit <span', 'Как нас найти <span', 'Як нас знайти <span'),
 ('<h2>Your way<br>to the academy.</h2>', '<h2>Как найти<br>академию.</h2>', '<h2>Як знайти<br>академію.</h2>'),
 ('<h2>Meet the coach.<br>Try the sport.</h2>',
  '<h2>Познакомьтесь<br>с~тренером.</h2>',
  '<h2>Познайомтеся<br>з~тренером.</h2>'),
 ('Book a trial for your child. The academy will confirm the time with you.',
  'Запишите ребёнка на~пробное. Академия подтвердит время занятия.',
  'Запишіть дитину на~пробне. Академія підтвердить час заняття.')]

PARENTS_HTML = [("Parents' Info — ElyFlame Academy", 'Родителям — ElyFlame Academy', 'Батькам — ElyFlame Academy'),
 ("Plan your child's first visit to ElyFlame: trial questions, registration, academy policies, forms, clothing "
  'and equipment.',
  'Первый визит ребёнка в~ElyFlame: вопросы о~пробном, регистрация, правила академии, документы, форма '
  'и~инвентарь.',
  'Перший візит дитини до~ElyFlame: запитання про пробне, реєстрація, правила академії, документи, одяг '
  'та~інвентар.'),
 ('>Parents’ Info<', '>Родителям<', '>Батькам<'),
 ('<h1>Before the<br>first class.</h1>',
  '<h1>Перед первым<br>занятием.</h1>',
  '<h1>Перед першим<br>заняттям.</h1>'),
 ('Plan your child’s first visit, understand registration, and find the academy’s parent information in one '
  'place.',
  'Как подготовиться к~первому визиту ребёнка, зарегистрироваться и~найти нужные документы.',
  'Як підготуватися до~першого візиту дитини, зареєструватися та~знайти потрібні документи.'),
 ('First visit &amp; FAQ', 'Первый визит и~вопросы', 'Перший візит і~запитання'),
 ('After the trial', 'После пробного', 'Після пробного'),
 ('Academy policies', 'Правила академии', 'Правила академії'),
 ('Forms &amp; documents', 'Формы и~документы', 'Форми та~документи'),
 ('Clothing &amp; equipment', 'Форма и~инвентарь', 'Одяг та~інвентар'),
 ('Private lessons', 'Индивидуальные занятия', 'Індивідуальні заняття'),
 ('<h2>A little<br>clarity.</h2>', '<h2>Ответы<br>перед стартом.</h2>', '<h2>Відповіді<br>перед стартом.</h2>'),
 ('What should my child wear?', 'Что надеть ребёнку?', 'Що вдягнути дитині?'),
 ('[Clothing requirements for the trial lesson.]',
  '[Требования к~одежде для пробного занятия.]',
  '[Вимоги до~одягу для пробного заняття.]'),
 ('What should my child bring?', 'Что взять ребёнку с~собой?', 'Що взяти дитині із~собою?'),
 ('[What to bring to the trial lesson.]', '[Что взять на~пробное занятие.]', '[Що взяти на~пробне заняття.]'),
 ('What happens at the first lesson?', 'Как проходит первое занятие?', 'Як проходить перше заняття?'),
 ('The coach assesses your child’s age, skills, abilities and strength to recommend a starting level. You are '
  'welcome to watch the trial.',
  'Тренер оценит возраст, навыки, способности и~силу ребёнка и~порекомендует начальный уровень. Вы можете '
  'посмотреть пробное занятие.',
  'Тренер оцінить вік, навички, здібності та~силу дитини й~порадить початковий рівень. Ви можете подивитися '
  'пробне заняття.'),
 ('What if my child misses a class?',
  'Что делать, если ребёнок пропустит занятие?',
  'Що робити, якщо дитина пропустить заняття?'),
 ('[Absence reporting and make-up class policy.]',
  '[Как сообщить о~пропуске и~можно~ли отработать занятие.]',
  '[Як повідомити про пропуск і~чи можна відпрацювати заняття.]'),
 ('<h2>From a first visit<br>to the next class.</h2>',
  '<h2>От~знакомства<br>к~тренировкам.</h2>',
  '<h2>Від знайомства<br>до~тренувань.</h2>'),
 ('>Coach assessment<', '>Оценка тренера<', '>Оцінка тренера<'),
 ('The coach recommends a starting level for your child at the trial.',
  'На~пробном тренер порекомендует начальный уровень для ребёнка.',
  'На~пробному тренер порадить початковий рівень для дитини.'),
 ('>Adobe registration<', '>Регистрация в~Adobe<', '>Реєстрація в~Adobe<'),
 ('The Head Coach sends the registration link after the trial.',
  'После пробного главный тренер пришлёт ссылку на~регистрацию.',
  'Після пробного головний тренер надішле посилання на~реєстрацію.'),
 ('>Form &amp; first payment<', '>Форма и~первый платёж<', '>Форма й~перший платіж<'),
 ('Both must be complete before your child joins practice.',
  'Чтобы ребёнок начал заниматься, нужно заполнить форму и~внести первый платёж.',
  'Щоб дитина почала займатися, потрібно заповнити форму й~внести перший платіж.'),
 ('<h2>Know what<br>to expect.</h2>', '<h2>Правила<br>для всех.</h2>', '<h2>Правила<br>для всіх.</h2>'),
 ('>Refunds &amp; cancellations<', '>Возвраты и~отмены<', '>Повернення й~скасування<'),
 ('[Refund and cancellation policies.]',
  '[Правила возврата оплаты и~отмены занятий.]',
  '[Правила повернення оплати й~скасування занять.]'),
 ('>Code of conduct<', '>Кодекс поведения<', '>Кодекс поведінки<'),
 ('[Expectations for athletes and families.]',
  '[Правила поведения для спортсменов и~семей.]',
  '[Правила поведінки для спортсменів і~родин.]'),
 ('>Watching practice<', '>Посещение тренировок<', '>Відвідування тренувань<'),
 ('<h2>Paperwork,<br>in one place.</h2>', '<h2>Документы<br>под рукой.</h2>', '<h2>Документи<br>під рукою.</h2>'),
 ('[PDF documents to be supplied by the academy.]',
  '[PDF-документы от~академии.]',
  '[PDF-документи від академії.]'),
 ('>Waiver<', '>Форма согласия<', '>Форма згоди<'),
 ('[Waiver PDF from the academy.]', '[Форма согласия от~академии, PDF.]', '[Форма згоди від академії, PDF.]'),
 ('>Medical form<', '>Медицинская форма<', '>Медична форма<'),
 ('[Medical form PDF from the academy.]',
  '[Медицинская форма от~академии, PDF.]',
  '[Медична форма від академії, PDF.]'),
 ('<h2>Ready for<br>your child’s class.</h2>', '<h2>Всё для<br>занятия.</h2>', '<h2>Усе для<br>заняття.</h2>'),
 ('>Recreational<', '>Любительская программа<', '>Аматорська програма<'),
 ('>Competitive<', '>Соревновательная программа<', '>Змагальна програма<'),
 ('>Stretching &amp; Flexibility<', '>Растяжка и~гибкость<', '>Розтяжка та~гнучкість<'),
 ('[Clothing and equipment for Recreational.]',
  '[Форма и~инвентарь для любительской программы.]',
  '[Одяг та~інвентар для аматорської програми.]'),
 ('[Clothing and equipment for Competitive.]',
  '[Форма и~инвентарь для соревновательной программы.]',
  '[Одяг та~інвентар для змагальної програми.]'),
 ('[Clothing and equipment for Stretching &amp; Flexibility.]',
  '[Форма и~инвентарь для растяжки.]',
  '[Одяг та~інвентар для розтяжки.]'),
 ('<h2>Individual<br>questions.</h2>', '<h2>Личный<br>подход.</h2>', '<h2>Особистий<br>підхід.</h2>'),
 ('[Private lesson availability, format and booking arrangements.]',
  '[Доступность, формат и~порядок записи на~индивидуальные занятия.]',
  '[Доступність, формат і~порядок запису на~індивідуальні заняття.]'),
 ('>A first step together<', '>Первый шаг вместе<', '>Перший крок разом<'),
 ('<h2>Let’s meet<br>your child.</h2>',
  '<h2>Приходите<br>знакомиться.</h2>',
  '<h2>Приходьте<br>знайомитися.</h2>'),
 ('Read the parent guide <span', 'Памятка для родителей <span', 'Пам’ятка для батьків <span'),
 ('Trial first. Registration next.', 'Сначала пробное. Затем регистрация.', 'Спочатку пробне. Потім реєстрація.'),
 ('The Head Coach sends an Adobe registration link after the trial. Your child joins practice after the form and '
  'first payment are complete.',
  'После пробного главный тренер пришлёт ссылку на~регистрацию в~Adobe. Ребёнок начнёт заниматься после '
  'заполнения формы и~первого платежа.',
  'Після пробного головний тренер надішле посилання на~реєстрацію в~Adobe. Дитина почне займатися після '
  'заповнення форми й~першого платежу.')]

STRETCHING_HTML += [('Beyond one sport.', 'За~пределами одного спорта.', 'За~межами одного спорту.'),
 ('>Dancers<', '>Танцоры<', '>Танцівники<'),
 ('>Figure skaters<', '>Фигуристы<', '>Фігуристи<'),
 ('>Martial artists<', '>Единоборцы<', '>Представники єдиноборств<'),
 ('>Runners<', '>Бегуны<', '>Бігуни<'),
 ('>Benefits<', '>Польза<', '>Користь<'),
 ('What stretching<br>can offer.', 'Что даёт<br>растяжка.', 'Що дає<br>розтяжка.'),
 ('[First benefit, to be confirmed by the academy.]',
  '[Первый результат занятий: уточнить у~академии.]',
  '[Перший результат занять: уточнити в~академії.]'),
 ('[Second benefit, to be confirmed by the academy.]',
  '[Второй результат занятий: уточнить у~академии.]',
  '[Другий результат занять: уточнити в~академії.]'),
 ('[Third benefit, to be confirmed by the academy.]',
  '[Третий результат занятий: уточнить у~академии.]',
  '[Третій результат занять: уточнити в~академії.]')]

CONTACT_HTML += [('Let’s talk.', 'На~связи.', 'На~зв’язку.'),
 ('>Call hours<', '>Когда звонить<', '>Коли телефонувати<'),
 ('Mon–Fri 9 am–10 pm<br>Sat 9 am–5 pm<br>Sun closed',
  'Пн–пт 9:00–22:00<br>Сб 9:00–17:00<br>Вс~— выходной',
  'Пн–пт 9:00–22:00<br>Сб 9:00–17:00<br>Нд~— вихідний'),
 ('Write to us.', 'Напишите нам.', 'Напишіть нам.'),
 ('Prototype: this form checks your message but does not send it. Please call or email the academy.',
  'Прототип: форма проверяет сообщение, но~не~отправляет его. Позвоните или напишите на~почту академии.',
  'Прототип: форма перевіряє повідомлення, але~не~надсилає його. Зателефонуйте або напишіть на~пошту '
  'академії.'),
 ('>Your name<', '>Ваше имя<', '>Ваше ім’я<'),
 ('>Message<', '>Сообщение<', '>Повідомлення<'),
 ('Enter your name.', 'Введите ваше имя.', 'Введіть ваше ім’я.'),
 ('Enter a phone number with 10 to 15 digits.',
  'Введите номер телефона: от~10 до~15 цифр.',
  'Введіть номер телефону: від~10 до~15 цифр.'),
 ('Enter your message.', 'Введите сообщение.', 'Введіть повідомлення.'),
 ('Send message', 'Отправить сообщение', 'Надіслати повідомлення'),
 ('Your message passed the prototype check. Nothing was sent. Please call or email the academy.',
  'Сообщение прошло проверку в~прототипе, но~не~было отправлено. Позвоните или напишите на~почту академии.',
  'Повідомлення пройшло перевірку в~прототипі, але~не~було надіслане. Зателефонуйте або напишіть на~пошту '
  'академії.'),
 ('Google Maps: ElyFlame Academy in Buffalo Grove',
  'Google Maps: академия ElyFlame в~Буффало-Гроув',
  'Google Maps: академія ElyFlame у~Буффало-Гроув'),
 ('Door #11: entrance, parking, drop-off and pick-up',
  'Дверь №11: вход, парковка, высадка и~встреча детей',
  'Двері №11: вхід, паркування, висадка й~зустріч дітей'),
 ('Ask about the class', 'Спросить о~занятиях', 'Запитати про заняття'),
 ('Call the academy', 'Позвонить в~академию', 'Зателефонувати в~академію'),
 ('Email the academy', 'Написать в~академию', 'Написати в~академію'),
 ('>Email<', '>Электронная почта<', '>Електронна пошта<'),
 ('>Phone<', '>Телефон<', '>Телефон<'),
 ('Enter a valid email address.', 'Введите корректный адрес почты.', 'Введіть коректну адресу пошти.'),
 ('Ask about private lessons', 'Спросить о~частных занятиях', 'Запитати про приватні заняття'),
 ('Ask us anything', 'Задать вопрос', 'Поставити запитання')]

LANGUAGES = [('en', 'English', 'EN'), ('ru', 'Русский', 'RU'), ('uk', 'Українська', 'UA')]
LANGUAGE = {'en': 'Language', 'ru': 'Язык', 'uk': 'Мова'}
GLOBE = ('<svg class="lang-icon" viewBox="0 0 16 16" aria-hidden="true" focusable="false"><circle cx="8" cy="8" r="6.5"/>'
         '<path d="M1.5 8h13M8 1.5c2 2.2 2 10.8 0 13M8 1.5c-2 2.2-2 10.8 0 13"/></svg>')
CHEVRON = '<svg class="lang-chevron" viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="m4 6 4 4 4-4"/></svg>'

def relative_url(target, page):
    """A site-root path to a page-relative URL, preserving trailing slashes and anchors."""
    parsed = urlsplit(target)
    destination = parsed.path
    if destination == page and parsed.fragment:
        return '#' + parsed.fragment
    path = posixpath.relpath(destination or '.', page or '.')
    if destination.endswith('/') or not destination:
        path = './' if path == '.' else path + '/'
    return urlunsplit(('', '', path, parsed.query, parsed.fragment))

def links(lang, text, page=''):
    current = ('' if lang == 'en' else lang + '/') + page
    return [f'<a href="{relative_url(("" if code == "en" else code + "/") + page, current)}" hreflang="{code}" lang="{code}"'
            + (' aria-current="page"' if code == lang else '') + f'>{text(name, label)}</a>'
            for code, name, label in LANGUAGES]

def lang_menu(lang, page=''):
    code = {c: label for c, _, label in LANGUAGES}[lang]
    items = ''.join(f'<li>{a}</li>' for a in links(lang, lambda name, label: name, page))
    return (f'<details class="lang-menu" translate="no"><summary aria-label="{LANGUAGE[lang]}: {code}">{GLOBE}{code}{CHEVRON}'
            f'</summary><ul>{items}</ul></details>')

def lang_pills(lang, page=''):
    return (f'<div class="lang-pills" role="group" aria-label="{LANGUAGE[lang]}" translate="no">'
            + ''.join(links(lang, lambda name, label: label, page)) + '</div>')

def root_urls(html, page):
    """Normalize source-local references before translation and shared-shell checks."""
    def rewrite(match):
        attr, value = match.groups()
        parsed = urlsplit(value)
        if parsed.scheme or parsed.netloc or value.startswith('/'):
            return match[0]
        resolved = urlsplit(urljoin(SITE + page, value))
        path = resolved.path.lstrip('/')
        value = urlunsplit(('', '', path, resolved.query, resolved.fragment))
        if not path and not resolved.fragment:
            value = '#'
        return f'{attr}="{value}"'
    return re.sub(r'(href|src|poster|action)="([^"]*)"', rewrite, html)

def page_urls(html, lang, page):
    current = lang + '/' + page
    def rewrite(match):
        attr, value = match.groups()
        if urlsplit(value).scheme or value.startswith('//'):
            return match[0]
        if value in ('/privacy', '/terms'):
            return f'{attr}="/{lang}{value}"'
        parsed = urlsplit(value)
        # Shared assets live at the site root; shared translated JS lives at the locale root.
        if parsed.path.startswith('assets/') or parsed.path in ('site.css', 'hero-reveal.js'):
            target = value
        elif parsed.path.startswith('/'):
            return match[0]
        else:
            target = lang + '/' + value
        return f'{attr}="{relative_url(target, current)}"'
    return re.sub(r'(href|src|poster|action)="([^"]*)"', rewrite, html)

def source_page(html, page):
    for fn, token in ((lang_menu, 'LANG_MENU'), (lang_pills, 'LANG_PILLS')):
        html = replace_once(html, fn('en', page), token)
    return root_urls(html, page)

def check_shared(sources):
    """Relative URLs and the current-page marker may differ; all other shell markup must match."""
    for tag in ('header', 'footer'):
        reference = None
        for page, html in sources.items():
            block = re.search(fr'<{tag}\b.*?</{tag}>', html, re.S).group()
            block = re.sub(r' aria-current="[^"]*"', '', block)
            if reference is None:
                reference = block
            elif block != reference:
                raise ValueError(f'{page}index.html: shared {tag} differs from index.html')

def swap(text, rows, col, nbsp, where):
    for row in sorted(rows, key=lambda r: -len(r[0])):
        if row[0] not in text:
            sys.exit(f'{where}: not found, update the table: {row[0]!r}')
        text = text.replace(row[0], row[col].replace('~', nbsp))
    return text

def replace_once(text, old, new):
    assert text.count(old) == 1, old
    return text.replace(old, new)

class Leftovers(HTMLParser):
    """Collects visible text and text attributes that still contain English words."""
    def __init__(self):
        super().__init__()
        self.skip, self.found = 0, []

    def check(self, s):
        for keep in KEEP:
            s = s.replace(keep, '')
        if re.search(r'[A-Za-z]{3,}', s):
            self.found.append(s.strip())

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'svg'):
            self.skip += 1
        attrs = dict(attrs)
        for k in ('aria-label', 'alt', 'placeholder', 'title'):
            if attrs.get(k):
                self.check(attrs[k])
        if tag == 'meta' and attrs.get('name') == 'description':
            self.check(attrs['content'])

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'svg'):
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip and data.strip():
            self.check(data)

def js_leftovers(js):
    found = []
    for a, b in re.findall(r"'([^'\\\n]*)'|\"([^\"\\\n]*)\"", js):
        s = a or b
        for keep in KEEP:
            s = s.replace(keep, '')
        if ' ' in s and re.search(r'[A-Za-z]{3,} [A-Za-z]{2,}', s) and not re.search(r'[<>{}=#]', s):
            found.append(a or b)
    return found

def main():
    def read(name):
        with io.open(os.path.join(ROOT, name), encoding='utf-8') as source:
            return source.read()
    sources = {page: source_page(read(page + 'index.html'), page) for page in PAGES}
    check_shared(sources)
    rows = HTML + ABOUT_HTML + PARENTS_HTML + CONTACT_HTML + STRETCHING_HTML
    for row in rows:
        if not any(row[0] in html for html in sources.values()):
            sys.exit(f'HTML source not found, update the table: {row[0]!r}')
    js_src = read('site.js')
    problems, outputs = [], {}
    for lang, col in LANGS.items():
        for page, html_src in sources.items():
            html = html_src
            for row in sorted(rows, key=lambda r: -len(r[0])):
                html = html.replace(row[0], row[col].replace('~', '&nbsp;'))
            # Character entities are not decoded inside JSON script elements.
            html = re.sub(r'(<script type="application/json" id="team-data">)(.*?)(</script>)',
                          lambda m: m[1] + m[2].replace('&nbsp;', '\\u00a0') + m[3], html, flags=re.S)
            html = replace_once(html, '<html lang="en">', f'<html lang="{lang}">')
            html = replace_once(html, '<!doctype html>', '<!doctype html>\n<!-- Generated by tools/i18n.py. Edit the English source and translation tables. -->')
            html = replace_once(html, f'<link rel="canonical" href="{SITE}{page}">', f'<link rel="canonical" href="{SITE}{lang}/{page}">')
            html = replace_once(html, 'family=Cinzel:wght@400;500;600&', 'family=Cinzel:wght@400;500;600&family=Spectral+SC:wght@400;500&')
            html = page_urls(html, lang, page)
            html = replace_once(html, 'LANG_MENU', lang_menu(lang, page))
            html = replace_once(html, 'LANG_PILLS', lang_pills(lang, page))
            leftovers = Leftovers()
            leftovers.feed(html)
            # Script content is skipped by HTMLParser: also inspect visible coach fields in the JSON.
            for data in re.findall(r'<script type="application/json" id="team-data">(.*?)</script>', html, re.S):
                for coach in json.loads(data):
                    for field in ('name', 'role', 'focus', 'alt', 'bio'):
                        leftovers.check(coach.get(field, ''))
            problems += [f'{lang}/{page}index.html: {s}' for s in leftovers.found]
            outputs[f'{lang}/{page}index.html'] = html
        js = swap(js_src, JS, col, '\\u00a0', 'site.js')
        outputs[f'{lang}/site.js'] = '// Generated by tools/i18n.py from site.js. Do not edit by hand.\n' + js
        problems += [f'{lang}/site.js: {s}' for s in js_leftovers(js)]
    if problems:
        sys.exit('English left on the translated pages, add rows to the tables:\n  ' + '\n  '.join(problems))
    # Fail before writing any files if a page or translation is inconsistent.
    for name, text in outputs.items():
        destination = os.path.join(ROOT, name)
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        with io.open(destination, 'w', encoding='utf-8', newline='') as out:
            out.write(text)
    print(f'{len(PAGES)} pages in ru/ and uk/ are up to date; shared header/footer checked.')

if __name__ == '__main__':
    main()
