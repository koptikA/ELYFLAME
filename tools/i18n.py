"""Builds the Russian and Ukrainian pages from the English source.

    python tools/i18n.py

index.html and site.js are the source of truth. The script writes ru/index.html, ru/site.js, uk/index.html and
uk/site.js: every English string from HTML and JS below is swapped for its translation, relative paths get "../",
and the language attributes, canonical URL and switcher follow the page. Never edit ru/ or uk/ by hand.

It stops when a source string from the tables is missing (the English copy changed: update the row) and when visible
English is left on a generated page (a new string: add a row). Program names stay English in option values and in
site.js, because the form logic and the back end key on them; only the visible text is translated.

In translations "~" is a non-breaking space: after one-letter words, before a dash, between a number and its unit.
"""
import io
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGS = {'ru': 1, 'uk': 2}
SITE = 'https://elyflame.com/'

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
    ('aria-label="Video placeholder"', 'aria-label="Место для видео"', 'aria-label="Місце для відео"'),
    ('</span>Performance video</div>', '</span>Видео с~выступления</div>', '</span>Відео з~виступу</div>'),
    ('>Our coaches / Content preview<', '>Наши тренеры / Предпросмотр<', '>Наші тренери / Попередній перегляд<'),
    ('<h2>Guidance with<br><em>heart and purpose.</em></h2>', '<h2>Наставники<br><em>с~душой и~целью.</em></h2>', '<h2>Наставники<br><em>з~душею та~метою.</em></h2>'),
    ('aria-label="Coach photo placeholder">Coach photo<', 'aria-label="Место для фото тренера">Фото тренера<', 'aria-label="Місце для фото тренера">Фото тренера<'),
    ('<h3>[Coach name]</h3>', '<h3>[Имя тренера]</h3>', '<h3>[Ім’я тренера]</h3>'),
    ('>[Credentials]<', '>[Квалификация]<', '>[Кваліфікація]<'),
    ('<p>[One line about the coach’s approach and experience.]</p>', '<p>[Одна строка о~подходе и~опыте тренера]</p>', '<p>[Один рядок про підхід і~досвід тренера]</p>'),
    ('<p>National judge, USA Gymnastics (founder)</p>', '<p>Национальный судья USA Gymnastics (основательница)</p>', '<p>Національна суддя USA Gymnastics (засновниця)</p>'),
    ('<p>USA Gymnastics member club</p>', '<p>Клуб~— член USA Gymnastics</p>', '<p>Клуб~— член USA Gymnastics</p>'),
    ('>Content preview — coach profiles and safety credentials require client confirmation before publication.<',
     '>Предпросмотр: профили тренеров и~квалификацию публикуем только после подтверждения академии<',
     '>Попередній перегляд: профілі тренерів і~кваліфікацію публікуємо лише після підтвердження академії<'),
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
    ('Ask us anything <span', 'Задать вопрос <span', 'Поставити питання <span'),
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
    ('<p>Yes, you are welcome to watch the trial lesson. Regular practices are closed to parents, except open practices.</p>',
     '<p>Пробное~— да, приходите. Обычные тренировки закрыты для родителей, кроме открытых.</p>',
     '<p>Пробне~— так, приходьте. Звичайні тренування закриті для батьків, крім відкритих.</p>'),
    ('<summary>How do we register after the trial?</summary>', '<summary>Как записаться после пробного?</summary>', '<summary>Як записатися після пробного?</summary>'),
    ('<p>After the trial, the Head Coach sends you the registration form. Your child can join practice once the form is complete and the first payment is made.</p>',
     '<p>После пробного главный тренер пришлёт форму регистрации. Ребёнок начнёт заниматься, когда форма будет заполнена и~первый платёж внесён.</p>',
     '<p>Після пробного головний тренер надішле форму реєстрації. Дитина почне займатися, коли форму буде заповнено й~перший платіж внесено.</p>'),
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
KEEP = ['ElyFlame Academy', 'ElyFlame', 'ELYFLAME', 'Buffalo Grove',
        'Radcliffe Road', 'Silk Road International School', 'USA Gymnastics', 'Instagram', 'Facebook',
        'Kirakito Technologies', 'academy@elyflame.com', 'name@example.com', 'Stripe Checkout', 'SMS',
        'English', 'Stretching & Flexibility']


LANGUAGES = [('en', 'English', 'EN'), ('ru', 'Русский', 'RU'), ('uk', 'Українська', 'UA')]
LANGUAGE = {'en': 'Language', 'ru': 'Язык', 'uk': 'Мова'}
GLOBE = ('<svg class="lang-icon" viewBox="0 0 16 16" aria-hidden="true" focusable="false"><circle cx="8" cy="8" r="6.5"/>'
         '<path d="M1.5 8h13M8 1.5c2 2.2 2 10.8 0 13M8 1.5c-2 2.2-2 10.8 0 13"/></svg>')
CHEVRON = '<svg class="lang-chevron" viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="m4 6 4 4 4-4"/></svg>'


def links(lang, text):
    here = {'en': {'en': './', 'ru': 'ru/', 'uk': 'uk/'}}.get(lang) or {'en': '../', 'ru': '../ru/', 'uk': '../uk/', lang: './'}
    return [f'<a href="{here[code]}" hreflang="{code}" lang="{code}"' + (' aria-current="page"' if code == lang else '')
            + f'>{text(name, label)}</a>' for code, name, label in LANGUAGES]


def lang_menu(lang):
    """Header: a globe, the current code and a chevron; the list shows the languages by their own names."""
    code = {c: label for c, _, label in LANGUAGES}[lang]
    items = ''.join(f'<li>{a}</li>' for a in links(lang, lambda name, label: name))
    return (f'<details class="lang-menu" translate="no"><summary aria-label="{LANGUAGE[lang]}: {code}">{GLOBE}{code}{CHEVRON}'
            f'</summary><ul>{items}</ul></details>')


def lang_pills(lang):
    """Phone menu sheet: a segmented switcher, one tap per language."""
    return (f'<div class="lang-pills" role="group" aria-label="{LANGUAGE[lang]}" translate="no">'
            + ''.join(links(lang, lambda name, label: label)) + '</div>')


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
    read = lambda name: io.open(os.path.join(ROOT, name), encoding='utf-8').read()
    html_src, js_src = read('index.html'), read('site.js')
    for block in (lang_menu('en'), lang_pills('en')):
        assert block in html_src, 'The language switcher in index.html differs from lang_menu()/lang_pills(); keep them in sync.'
    problems = []
    for lang, col in LANGS.items():
        html = swap(html_src, HTML, col, '&nbsp;', 'index.html')
        html = replace_once(html, '<html lang="en">', f'<html lang="{lang}">')
        html = replace_once(html, '<!doctype html>', '<!doctype html>\n<!-- Generated by tools/i18n.py from ../index.html. Edit the English source or the tables in the script, then run it again. -->')
        html = replace_once(html, f'<link rel="canonical" href="{SITE}">', f'<link rel="canonical" href="{SITE}{lang}/">')
        html = replace_once(html, lang_menu('en'), lang_menu(lang))
        html = replace_once(html, lang_pills('en'), lang_pills(lang))
        html = replace_once(html, 'href="/privacy"', f'href="/{lang}/privacy"')
        html = replace_once(html, 'href="/terms"', f'href="/{lang}/terms"')
        html = replace_once(html, 'family=Cinzel:wght@400;500;600&', 'family=Cinzel:wght@400;500;600&family=Spectral+SC:wght@400;500&')
        html = replace_once(html, 'href="site.css"', 'href="../site.css"')
        html = replace_once(html, 'src="hero-reveal.js"', 'src="../hero-reveal.js"')
        html = html.replace('="assets/', '="../assets/')
        js = swap(js_src, JS, col, '\\u00a0', 'site.js')
        js = replace_once(js, 'href="assets/', 'href="../assets/')
        js = f'// Generated by tools/i18n.py from ../site.js. Edit the English source or the tables in the script, then run it again.\n{js}'
        leftovers = Leftovers()
        leftovers.feed(html)
        problems += [f'{lang}/index.html: {s}' for s in leftovers.found] + [f'{lang}/site.js: {s}' for s in js_leftovers(js)]
        os.makedirs(os.path.join(ROOT, lang), exist_ok=True)
        for name, text in (('index.html', html), ('site.js', js)):
            io.open(os.path.join(ROOT, lang, name), 'w', encoding='utf-8', newline='').write(text)
    if problems:
        sys.exit('English left on the translated pages, add rows to the tables:\n  ' + '\n  '.join(problems))
    print('ru/ and uk/ are up to date.')


if __name__ == '__main__':
    main()
