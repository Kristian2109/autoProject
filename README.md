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

Получателят е **kristian.petrov1998@gmail.com**, предоставен от клиента.

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

Включени са `lang="bg"`, уникални заглавия и описания, семантични секции, една H1 във всяка страница, alt текстове, Open Graph данни, robots.txt и JSON-LD `AutomotiveBusiness` с бизнес контактите. „CEO“ в заданието е интерпретирано като „SEO“.

Домейнът още не е предоставен. След като го изберете, генерирайте реалните canonical и social URL адреси и XML карта:

```bash
python3 scripts/configure_seo.py https://your-domain.bg
```

Командата може да се изпълнява многократно и поддържа сайт в поддиректория. Примерният адрес в командата трябва да се замени с действителния домейн. Скриптът актуализира HTML файловете в `public/` и записва там `sitemap.xml` и `robots.txt`. Той е помощен локален инструмент; Python не е нужен на хостинга.

Публикуването е ръчно в Cloudflare Pages, както е описано по-долу.

## Cloudflare Pages — manual deployment

Run all commands from the **project root**. Install Node.js 22 or newer with npm. Wrangler is pinned in `package.json` and `package-lock.json`; it is a development dependency only.

### First-time setup

```bash
npm ci
npx wrangler login
npx wrangler pages project create anex-avtotapiceria --production-branch=master
```

Create a **Direct Upload** Pages project without connecting GitHub. `anex-avtotapiceria` is the configured project name; if you choose another name or already have a project, update `name` in `wrangler.jsonc` and use that name when creating the project. Skip project creation for an existing Direct Upload project.

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

Wrangler prints the deployed URL. Git commits and GitHub pushes remain source-control operations; publishing requires the manual command. No deployment workflow or Git integration is configured in this repository.

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

Всичките шест страници са проверени в Chromium при ширини 320, 390, 768, 1024 и 1440 px. Проверени са мобилното меню, филтрите и диалогът на галерията, клавиатурната навигация, валидацията на формата и съдържанието на подготвеното писмо. Няма JavaScript грешки, липсващи ресурси или хоризонтално излизане извън екрана. Автоматичната проверка с axe за WCAG 2 A/AA и WCAG 2.1 AA не отчита нарушения. Проверени са вътрешните връзки, JSON-LD и повторното генериране на SEO адресите.
