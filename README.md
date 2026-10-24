# Анекс — Автотапицерия

Статичен сайт на български с HTML, CSS и JavaScript. Няма framework, runtime зависимости, компилация или backend. Публичните файлове са в `public/`, а Wrangler е само инструмент за локален преглед и ръчно публикуване. Сайтът може да се отвори и директно през `public/index.html`.

## Локален преглед

От директорията на проекта:

```bash
python3 -m http.server 8000 --bind 127.0.0.1 --directory public
```

Отворете `http://localhost:8000`.

## Страници

Всички страници и ресурси по-долу са в `public/`.

- `index.html`: представяне, услуги и избрани изработки.
- `about.html`: история и подход на ателието.
- `services.html`: първоначален списък на услугите и често задавани въпроси.
- `gallery.html`: осем архивни снимки, филтри по категории и достъпен диалог за увеличаване. Стрелките сменят снимката, Escape затваря диалога.
- `contact.html`: телефони, адрес, Google Maps и въпросник за имейл запитване.
- `privacy.html`: информация за работата на формата и външните връзки.

## Формата за запитване

Получателят е **aneksauto@gmail.com**, предоставен от клиента.

Формата проверява задължителните полета и подготвя `mailto:` писмо с услугата, автомобила, описанието и контактите. Посетителят трябва да има настроено пощенско приложение и да изпрати писмото от него. Снимки се прикачват в пощенското приложение. Сайтът не изпраща автоматично имейли, не съхранява въведени данни и не показва фалшиво потвърждение за изпратено запитване. Има и директни имейл връзки.

За автоматично изпращане директно от страницата е нужна отделно конфигурирана услуга за форми или backend. Пазете ключове и SMTP пароли извън клиентския JavaScript.

За промяна на получателя редактирайте `CONTACT_EMAIL` в `assets/js/main.js`, имейл връзките в HTML страниците, `action` на формата и JSON-LD в `index.html`.

## Съдържание и изображения

Бизнес информацията и осемте снимки са извлечени от предоставената [публикация в Бизнес Каталог](https://business-catalog.bg/анекс-димитър-славчев-ет-автотапицер). Взети са контактите на Анекс от фирмената секция; контактите на издателя на каталога не са използвани.

- Основен телефон: **0887 610 536**.
- Допълнителни телефони: **0899 925 524**, **02 929 30 95**.
- Адрес: **София, кв. Св. Троица, бл. 357**.
- Година на основаване: **1994**.
- Публикуваното работно време **08:00–17:00** е обозначено като архивна информация; работните дни и часът за посещение се уточняват по телефона.

Услугите са начален списък от старата публикация и могат да бъдат уточнени със собственика. Не са добавяни цени, измислени отзиви, работни дни или гаранционни обещания. Телефоните, адресът и актуалните услуги трябва да бъдат потвърдени със собственика преди публично публикуване.

Началният банер е отделна **илюстративна снимка**, обозначена в страницата, от [Lorenzo Hamers / Unsplash](https://unsplash.com/photos/the-interior-of-a-car-with-black-leather-seats-rVxBhzRRcL4), под [Unsplash License](https://unsplash.com/license). Снимката не се представя като изработка на Анекс. Галерията използва само снимките от стария сайт.

[Tapiceri.bg](https://tapiceri.bg/) е използван като ориентир за структурата. Текстовете и дизайнът на този сайт са създадени отделно.

## Редактиране

Страниците съдържат реален HTML и са четими без JavaScript. Редактирайте услугите директно в `services.html` и съответните карти в `index.html`. При добавяне на категория актуализирайте списъка в контактната форма. Общите стилове са в `assets/css/style.css`, а менюто, галерията и формата — в `assets/js/main.js`.

Навигацията и footer-ът са статични във всяка страница. При промяна на общите контакти или линкове актуализирайте всички HTML файлове. Няма външни шрифтове или проследяване.

## SEO и публикуване

Включени са `lang="bg"`, уникални заглавия и описания за услугите в София, семантични секции, една H1 във всяка страница, описателни alt текстове и Open Graph данни. Началната страница и контактите съдържат JSON-LD `AutomotiveBusiness` — специализиран вид `LocalBusiness` — със съществуващите име, адрес, телефони и имейл. Не са добавяни непотвърдени работни дни, координати, оценки или профили в Google. В галерията заглавията на изработките са H2 под основното H1, без промяна във външния им вид.

Потвърденият production адрес е **https://anex.bg**. Canonical адресите, социалните метаданни, бизнес и breadcrumb JSON-LD, `sitemap.xml` и `robots.txt` са генерирани за него. За повторно генериране:

```bash
python3 scripts/configure_seo.py https://anex.bg
```

Командата изисква окончателния HTTPS адрес. Не използвайте примерния домейн или временен адрес за преглед. Тя добавя canonical URL, `og:url`, социално изображение, абсолютни адреси в бизнес данните и `BreadcrumbList` за съществуващата навигация. Актуализира HTML файловете в `public/` и записва там `sitemap.xml` и `robots.txt`. Адресите са без `.html`, съответстващи на пренасочванията на Cloudflare Pages. Запазват се съществуващите бизнес данни и видимият текст; повторното изпълнение не дублира метаданните. `404.html` и страници с `noindex` не влизат в sitemap. Помощният инструмент няма допълнителни Python зависимости и не се изпълнява при посещение на сайта.

След първото изпълнение commit-нете генерираните HTML/XML/TXT файлове. Пускайте командата отново при смяна на домейна или добавяне/премахване на страници. Cloudflare Pages продължава да публикува само `public/` без build процес. В Git-свързан Pages проект настройките са Framework: None, Build command: празно, Build output: `public`; ръчният Wrangler workflow е описан по-долу като алтернатива.

Банерът използва същата снимка в WebP с варианти 640/960/1280/1920 px и съгласуван responsive preload. Останалите архивни снимки са малки JPEG файлове с размери в HTML, lazy loading и асинхронно декодиране. `404.html` е технически обработчик, който позволява на Cloudflare да връща истински 404 отговори вместо homepage fallback за несъществуващи адреси. Той е с `noindex` и не е нова страница за SEO съдържание.

Предоставеният от клиента [Google Business Profile](https://share.google/JVaPKbj8iBupffUvb) е записан като `sameAs` в бизнес JSON-LD. Линкът се пренасочва към Google профил „Автотапицер Анекс“; Google блокира автоматизираната проверка на адреса и телефона. Съществуващите контакти са запазени и не са добавяни непотвърдени часове, координати или оценки. Сравнете контактите ръчно с профила при финалния преглед.

При проверката на 19.10.2026 г. `anex.bg` не се разрешаваше през DNS от средата за разработка. Свържете домейна с Cloudflare Pages и проверете HTTPS след активиране на DNS. След публикуване проверете `/robots.txt`, `/sitemap.xml`, canonical адресите и един несъществуващ URL; подайте `https://anex.bg/sitemap.xml` в Google Search Console и проверете бизнес данните с Rich Results Test. Метаданните и sitemap не гарантират позиции или индексиране.

### Оптимизация на съдържанието — 24.10.2026 г.

Основната страница е насочена към „автотапицерия София“, „автотапицерия“ и естествени варианти на „автотапицер“. Оригиналното H1 „Нов живот за интериора“ е запазено, а над него е добавено „Автотапицерия в София · От 1994 г.“. Описанието включва квартала, основните услуги и телефона. Страницата с услуги обяснява ремонт и претапициране на седалки, претапициране на волани, тавани и кори на врати. Вътрешните връзки назовават съответната услуга. Добавени са полезни отговори за частичен ремонт, цена след оглед и адрес на ателието. Запазени са оригиналните рекламни послания в основните заглавия. Бизнесът се представя като ателие или автотапицерия, а бизнес описанието в JSON-LD е съгласувано с видимия текст.

Използвани са естествени варианти на фразите според [SEO ръководството на Google](https://developers.google.com/search/docs/fundamentals/seo-starter-guide). Не е нужно всяка страница да повтаря дословно всички ключови думи. Няма данни от Search Console или инструмент за обем на търсене; изборът на фрази е според услугите и намерението на посетителя, без твърдения за измерена популярност или позиции.

Следващи подобрения по приоритет:

1. След публикуване проверете обновеното съдържание и canonical адресите. На 24.10.2026 г. публичната начална страница и `/services` отговориха с HTTPS 200, `/services.html` пренасочи с 308 към `/services`, а несъществуващ URL върна 404. Достъпни са `robots.txt` с разрешено обхождане и sitemap с шестте страници и правилния домейн. Промените в тази редакция са локални.
2. В Google Search Console подайте `https://anex.bg/sitemap.xml`, проверете индексирането на началната страница и услугите и следете реалните заявки, показвания, кликове и запитвания след повторното обхождане.
3. Потвърдете адреса, телефоните, актуалните услуги и работното време с ателието и Google Business Profile. Поддържайте ги еднакви в сайта и профила. Добавете актуални снимки и отговаряйте на реални отзиви според [насоките на Google за локални резултати](https://support.google.com/business/answer/7091?hl=bg).
4. Добавете собствени актуални снимки преди/след с кратък разказ за действителния ремонт, използвания материал и автомобила. Архивните снимки остават обозначени като архив, а началният банер — като илюстративен.
5. При достатъчно реални проекти и данни за търсене създайте отделни полезни страници за волани, седалки и тавани. Всяка да съдържа различими примери и конкретни отговори; не копирайте една страница с различна ключова дума или квартал.

## Cloudflare Pages — manual deployment

Run all commands from the **project root**. Install Node.js 22 or newer with npm. Wrangler is pinned in `package.json` and `package-lock.json`; it is a development dependency only.

### First-time setup

```bash
npm ci
npx wrangler login
npx wrangler pages project create anex-avtotapiceria --production-branch=master
```

These are the optional **Direct Upload** setup commands. For the existing Git-connected Pages workflow, keep the GitHub connection and skip project creation. `anex-avtotapiceria` is the Wrangler project name; if your existing Pages project has another name, update `name` in `wrangler.jsonc` before using the manual deploy commands.

The production branch is `master`, matching this repository. It labels manual deployments and does not configure automatic Git deployment. If you choose another production branch, use it in project creation and the `deploy` script in `package.json`.

### Deploy

```bash
npm run deploy
```

Equivalent Wrangler command:

```bash
npx wrangler pages deploy --branch=master
```

`wrangler.jsonc` sets `pages_build_output_dir` to `./public`, so Wrangler uploads that folder directly. There is **no build step**. Use `npx wrangler pages deploy public --branch=master` if you prefer an explicit directory. Uploading `.` would include project tooling alongside the site; use the configured `public/` directory instead.

Wrangler prints the deployed URL. With Direct Upload, publishing requires the manual command. With a Git-connected Pages project, deployments follow the production/preview branch controls configured in the Cloudflare dashboard. No GitHub Actions deployment workflow is required.

### Local Pages preview and preview deployment

```bash
npm run dev
```

This serves `public/` through the local Pages runtime. To upload a separate preview deployment manually:

```bash
npm run deploy:preview
```

That command uses the `preview` branch label. Before a production deployment, run the optional SEO helper with the final public domain when it is known.

Cloudflare documents this workflow in [Direct Upload](https://developers.cloudflare.com/pages/get-started/direct-upload/) and [Pages Wrangler configuration](https://developers.cloudflare.com/pages/functions/wrangler-configuration/). A Direct Upload project cannot later be converted to Git integration; automatic Git deployment would require a separate Pages project.

## Проверки

За регресионните проверки на SEO помощника:

```bash
python3 -m unittest discover -s tests -v
```

Те покриват валидиране на HTTPS адреса преди промени по файловете, повторно изпълнение, смяна на домейн, sitemap без 404/noindex страници, запазване на видимия HTML и непроменени контакти в JSON-LD.

Всичките шест страници са проверени в Chromium при ширини 320, 390, 768, 1024 и 1440 px. Проверени са мобилното меню, филтрите и диалогът на галерията, клавиатурната навигация, валидацията на формата и съдържанието на подготвеното писмо. Няма JavaScript грешки, липсващи ресурси или хоризонтално излизане извън екрана. Автоматичната проверка с axe за WCAG 2 A/AA и WCAG 2.1 AA не отчита нарушения. Проверени са вътрешните връзки, JSON-LD и повторното генериране на SEO адресите.
