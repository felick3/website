let products = [];

const grid = document.getElementById('product-grid');
const catBtns = document.querySelectorAll('.cat-btn');

let activeCategory = 'all';

async function loadProducts() {
  const res = await fetch('/api/products');
  products = await res.json();
  renderGrid();
}

function renderGrid() {
  const filtered = activeCategory === 'all'
    ? products
    : products.filter(p => p.category === activeCategory);

  grid.innerHTML = '';

  filtered.forEach((p, i) => {
    const num = String(i + 1).padStart(2, '0');

    const card = document.createElement('div');
    card.className = 'product-card';

    card.innerHTML = `
      <div class="card-img-wrap">
        <img src="${p.image}" alt="${p.name}">
        <span class="card-num">${num}</span>
        <div class="card-overlay">
          <button class="overlay-btn">Просмотреть</button>
        </div>
      </div>
      <div class="card-info">
        <div class="card-category">${p.category_label}</div>
        <div class="card-name">${p.name}</div>
        <div class="card-price">${p.price} ₽</div>
      </div>
    `;

    card.addEventListener('click', () => openModal(p));
    grid.appendChild(card);
  });
}

catBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    catBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    activeCategory = btn.dataset.cat;
    renderGrid();
  });
});

loadProducts();