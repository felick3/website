# DENIS Shop — Developer History

## Project Overview

A unified Flask web application combining authentication (Auth) and a product catalog (my_catalog) into a single dark-themed fashion store.

**Stack:** Python / Flask · Flask-SQLAlchemy · Flask-Login · Werkzeug · Jinja2 · SQLite · Vanilla JS · CSS

---

## Session 1 — Project Merge

**Task:** Combine two separate projects (`Auth` and `my_catalog`) into one cohesive app.

### Auth project (original)
- Raw SQLite + `hashlib` (sha256)
- Login by **email**
- Password validation: min 8 chars, uppercase, digit, special char
- Routes: `/`, `/register`, `/login`, `/profile`, `/logout`

### my_catalog project (original)
- Flask-SQLAlchemy + Flask-Login + Werkzeug
- Login by **username** (no email field)
- Models: `User`, `Category`, `Product`
- Routes: `/`, `/register`, `/login`, `/logout`, `/category/<id>`, `/product/<id>`

### Decisions made
- **Kept** Flask-SQLAlchemy + Flask-Login + Werkzeug (modern stack from my_catalog)
- **Kept** email-based login and password validation rules from Auth
- **Added** `email` field to `User` model (was missing in my_catalog)
- **Added** `seed_data()` — auto-creates 3 categories + 5 products on first run
- **Added** `base.html` — shared layout with navbar and flash messages

### Final file structure
```
code/shop/
├── app.py           # All routes + Flask-Login + password validation
├── models.py        # User (id, name, email, password, address), Category, Product
└── templates/
    ├── base.html
    ├── catalog.html
    ├── category_products.html
    ├── login.html
    ├── register.html
    └── profile.html
```

### Routes
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/` | Catalog main page |
| GET | `/category/<int:id>` | Products in category |
| GET/POST | `/register` | Registration |
| GET/POST | `/login` | Login |
| GET | `/logout` | Logout (login_required) |
| GET | `/profile` | User profile (login_required) |

---

## Session 2 — UI Redesign

**Task:** Adapt all templates to match a provided Figma Make UI export (`uitemplate.txt`).

### Design system extracted
| Token | Value |
|-------|-------|
| Background | `rgb(13, 13, 13)` |
| Surface (header/footer) | `rgb(26, 26, 26)` |
| Text & borders | `rgb(237, 237, 237)` |
| Heading font | `Playfair Display` (Google Fonts, serif) |
| Body font | System sans-serif (`-apple-system, BlinkMacSystemFont, Segoe UI, Roboto`) |
| Active button | bg `rgb(237,237,237)` / color `rgb(13,13,13)` |
| Ghost button | transparent / border `rgb(237,237,237)` |

### Changes per file

**`base.html`**
- Sticky dark header with brand `DENIS` in Playfair Display
- Icon buttons (SVG): user/profile icon, logout icon
- Flash messages: fixed top-right, dark styled
- Footer: dark `rgb(26,26,26)`, brand, contacts, social icons (Instagram, Telegram, VK, Email), legal links

**`catalog.html`**
- **Hero section**: horizontal scroll gallery, 10 items (videos + Unsplash images), numbered `01–10`, border-right dividers
- **Catalog section**: Playfair Display title, category filter buttons (from DB), 4-column product grid
- Product cards: dark background, hover overlay border, `ПРОСМОТРЕТЬ` label on hover, category label + name + price
- `app.py` updated: `index()` now passes both `categories` and `products`

**`category_products.html`**
- Breadcrumb: `КАТАЛОГ / CATEGORY NAME`
- Same 4-column dark grid as catalog page
- Back link at bottom

**`login.html` / `register.html`**
- Full-height centered layout
- Playfair Display heading
- Borderless underline inputs (no box border, only bottom border)
- Inverted button on hover (bg ↔ transparent)

**`profile.html`**
- 2×2 bordered grid table: Имя, Email, Адрес, Статус
- Two action buttons: `В КАТАЛОГ` (filled), `ВЫЙТИ` (ghost)

---

## Session 3 — Hero Auto-Scroll

**Task:** Make the hero media strip auto-scroll and loop infinitely.

### Implementation

**Technique:** CSS `translateX` animation + JS DOM clone

**HTML structure:**
```html
<section class="hero">                         <!-- overflow: hidden -->
    <div class="hero-belt" id="heroBelt">      <!-- animated, display: flex -->
        <div class="hero-track" id="heroTrack"><!-- 10 original items -->
            ...
        </div>
        <!-- JS clones #heroTrack and appends here as aria-hidden -->
    </div>
</section>
```

**CSS:**
```css
.hero-belt {
    display: flex;
    width: max-content;
    animation: heroScroll 40s linear infinite;
}
.hero-belt:hover { animation-play-state: paused; }

@keyframes heroScroll {
    0%   { transform: translateX(0); }
    100% { transform: translateX(-50%); }
}
```

**JS:**
```js
const belt  = document.getElementById('heroBelt');
const track = document.getElementById('heroTrack');
const clone = track.cloneNode(true);
clone.id = '';
clone.setAttribute('aria-hidden', 'true');
belt.appendChild(clone);
// belt now has [track][clone] side-by-side
// -50% = exactly one track width → seamless loop
```

**Bug fixed:** First attempt cloned `#heroTrack` as a sibling of itself (inside `.hero`), causing two tracks to stack vertically. Fixed by introducing `.hero-belt` as the animated flex container — clone goes inside belt, not beside it.

**Speed control:** Change `40s` in the animation declaration. Lower = faster.

---

## How to Run

```bash
pip install flask flask-sqlalchemy flask-login werkzeug
cd code/shop
python app.py
```

Open: `http://127.0.0.1:5000`

Database `shop.db` is auto-created on first run with seed data.

---

## Known Limitations / TODO

- [ ] Product images are placeholders (`◻`) — no image upload system yet
- [ ] No shopping cart functionality
- [ ] No admin panel to manage categories/products via UI
- [ ] Password reset not implemented
- [ ] `@before_first_request` is deprecated in Flask 2.3+ — migrate `seed_data()` to `with app.app_context()` block
- [ ] No CSRF protection on forms
- [ ] Hero gallery uses hardcoded Unsplash URLs — replace with real product media
