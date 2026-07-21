'use client'

import { useEffect, useMemo, useState } from 'react'
import {
  createProduct,
  deleteProduct,
  createOrder,
  getCurrentUser,
  getProducts,
  loginUser,
  logoutUser,
  registerUser,
  updateProduct,
} from '../lib/api'

const emptyProduct = {
  name: '',
  description: '',
  price: '',
  stock: '',
  photo_url: '',
}

const featuredBenefits = ['Entrega simples', 'Vitrine organizada', 'Compra em poucos cliques', 'Gestao para vendedores']

function formatCurrency(value) {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  }).format(Number(value || 0))
}

function productImage(product) {
  return (
    product.photo_url ||
    product.photo_thumbnail_url ||
    'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=900&q=80'
  )
}

export default function Home() {
  const [authOpen, setAuthOpen] = useState(false)
  const [authMode, setAuthMode] = useState('login')
  const [user, setUser] = useState(null)
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)
  const [notice, setNotice] = useState('')
  const [finishedOrder, setFinishedOrder] = useState(null)

  async function loadProducts() {
    const data = await getProducts()
    setProducts(data)
  }

  useEffect(() => {
    async function boot() {
      try {
        await loadProducts()
        if (localStorage.getItem('delivery_token')) {
          const currentUser = await getCurrentUser()
          setUser(currentUser)
        }
      } catch {
        setNotice('')
      } finally {
        setLoading(false)
      }
    }

    boot()
  }, [])

  async function handleAuthenticated(token) {
    localStorage.setItem('delivery_token', token)
    const currentUser = await getCurrentUser()
    setUser(currentUser)
    setAuthOpen(false)
    setNotice('')
    await loadProducts()
  }

  async function handleLogout() {
    await logoutUser()
    localStorage.removeItem('delivery_token')
    setUser(null)
    setFinishedOrder(null)
  }

  const sellerProducts = useMemo(() => {
    if (!user) {
      return []
    }

    if (user.role === 'admin') {
      return products
    }

    return products.filter((product) => product.seller_id === user.id)
  }, [products, user])

  if (loading) {
    return (
      <main className="loading-screen">
        <div className="loader" />
        <p>Preparando a vitrine...</p>
      </main>
    )
  }

  if (user && finishedOrder) {
    return (
      <ThankYouPage
        order={finishedOrder}
        onBack={() => setFinishedOrder(null)}
        onLogout={handleLogout}
      />
    )
  }

  if (user?.role === 'seller' || user?.role === 'admin') {
    return (
      <SellerDashboard
        user={user}
        products={sellerProducts}
        onLogout={handleLogout}
        onRefresh={loadProducts}
        notice={notice}
        setNotice={setNotice}
      />
    )
  }

  if (user?.role === 'customer') {
    return (
      <CustomerStorefront
        user={user}
        products={products}
        onLogout={handleLogout}
        onFinish={(order) => setFinishedOrder(order)}
        notice={notice}
        onRefresh={loadProducts}
        setNotice={setNotice}
      />
    )
  }

  return (
    <main className="home-shell">
      <Header onAuthOpen={(mode) => {
        setAuthMode(mode)
        setAuthOpen(true)
      }} />

      <section className="hero-section">
        <div className="hero-copy">
          <span className="eyebrow">Delivery para lojas, restaurantes e mercados</span>
          <h1>Delivery Hub</h1>
          <p>
            Uma vitrine digital para vendedores publicarem seus produtos e clientes
            comprarem com praticidade, informacao clara e um fluxo leve do inicio ao fim.
          </p>
          <div className="hero-actions">
            <button className="primary-button" onClick={() => {
              setAuthMode('register')
              setAuthOpen(true)
            }}>
              Comecar agora
            </button>
            <button className="ghost-button" onClick={() => {
              setAuthMode('login')
              setAuthOpen(true)
            }}>
              Entrar
            </button>
          </div>
        </div>

        <div className="hero-visual" aria-label="Mesa com produtos de delivery">
          <img
            src="https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=1200&q=85"
            alt=""
          />
          <div className="floating-order">
            <span>Pedido em destaque</span>
            <strong>{formatCurrency(42.9)}</strong>
            <small>Chegando em 28 min</small>
          </div>
        </div>
      </section>

      <section className="category-strip" aria-label="Destaques do Delivery Hub">
        {featuredBenefits.map((benefit) => (
          <button key={benefit}>{benefit}</button>
        ))}
      </section>

      <section className="preview-section">
        <div>
          <span className="eyebrow">Uma operacao mais clara</span>
          <h2>Produtos bem apresentados, pedidos organizados</h2>
        </div>
        <div className="preview-grid">
          <FeatureCard title="Venda com autonomia" text="Cada vendedor cuida da propria vitrine, ajusta estoque, preco e imagem quando precisar." />
          <FeatureCard title="Compra sem atrito" text="O cliente encontra o produto, monta o carrinho e acompanha o resumo antes de concluir." />
          <FeatureCard title="Base pronta para crescer" text="Pedidos, clientes e vendedores ficam separados por perfil, abrindo caminho para pagamento e status." />
        </div>
      </section>

      {notice && <div className="toast">{notice}</div>}

      {authOpen && (
        <AuthModal
          mode={authMode}
          setMode={setAuthMode}
          onClose={() => setAuthOpen(false)}
          onAuthenticated={handleAuthenticated}
          setNotice={setNotice}
        />
      )}
    </main>
  )
}

function Header({ onAuthOpen }) {
  return (
    <header className="site-header">
      <a className="brand" href="#">
        <span>DH</span>
        Delivery Hub
      </a>
      <nav>
        <button onClick={() => onAuthOpen('login')}>Entrar</button>
        <button className="nav-cta" onClick={() => onAuthOpen('register')}>
          Criar conta
        </button>
      </nav>
    </header>
  )
}

function FeatureCard({ title, text }) {
  return (
    <article className="feature-card">
      <h3>{title}</h3>
      <p>{text}</p>
    </article>
  )
}

function AuthModal({ mode, setMode, onClose, onAuthenticated, setNotice }) {
  const [role, setRole] = useState('customer')
  const [form, setForm] = useState({
    username: '',
    email: '',
    identifier: '',
    password: '',
  })
  const [submitting, setSubmitting] = useState(false)

  function updateField(field, value) {
    setForm((current) => ({ ...current, [field]: value }))
  }

  async function handleSubmit(event) {
    event.preventDefault()
    setSubmitting(true)

    try {
      if (mode === 'register') {
        await registerUser({
          username: form.username,
          email: form.email,
          password: form.password,
          role,
        })
        const tokenData = await loginUser({
          identifier: form.email,
          password: form.password,
        })
        await onAuthenticated(tokenData.access_token)
        return
      }

      const tokenData = await loginUser({
        identifier: form.identifier,
        password: form.password,
      })
      await onAuthenticated(tokenData.access_token)
    } catch (error) {
      setNotice(error.message)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="modal-backdrop">
      <section className="auth-modal">
        <button className="close-button" onClick={onClose} aria-label="Fechar">
          x
        </button>
        <div className="auth-aside">
          <span className="eyebrow">Acesso ao delivery</span>
          <h2>{mode === 'login' ? 'Entre para continuar' : 'Crie sua conta'}</h2>
          <p>
            Entre para comprar seus favoritos ou administrar sua propria vitrine
            no Delivery Hub.
          </p>
        </div>

        <form className="auth-form" onSubmit={handleSubmit}>
          <div className="segmented-control">
            <button
              type="button"
              className={mode === 'login' ? 'active' : ''}
              onClick={() => setMode('login')}
            >
              Login
            </button>
            <button
              type="button"
              className={mode === 'register' ? 'active' : ''}
              onClick={() => setMode('register')}
            >
              Cadastro
            </button>
          </div>

          {mode === 'register' && (
            <>
              <label>
                Nome de usuario
                <input
                  value={form.username}
                  onChange={(event) => updateField('username', event.target.value)}
                  required
                />
              </label>
              <label>
                Email
                <input
                  type="email"
                  value={form.email}
                  onChange={(event) => updateField('email', event.target.value)}
                  required
                />
              </label>
              <div className="role-picker">
                <button
                  type="button"
                  className={role === 'customer' ? 'selected' : ''}
                  onClick={() => setRole('customer')}
                >
                  Cliente
                </button>
                <button
                  type="button"
                  className={role === 'seller' ? 'selected' : ''}
                  onClick={() => setRole('seller')}
                >
                  Vendedor
                </button>
              </div>
            </>
          )}

          {mode === 'login' && (
            <label>
              Email ou usuario
              <input
                value={form.identifier}
                onChange={(event) => updateField('identifier', event.target.value)}
                required
              />
            </label>
          )}

          <label>
            Senha
            <input
              type="password"
              minLength={mode === 'register' ? 10 : 8}
              pattern={mode === 'register' ? '^(?=.*[^A-Za-z0-9]).{10,}$' : undefined}
              value={form.password}
              onChange={(event) => updateField('password', event.target.value)}
              required
            />
            {mode === 'register' && (
              <small className="field-hint">Minimo de 10 caracteres e 1 caractere especial.</small>
            )}
          </label>

          <button className="primary-button full" disabled={submitting}>
            {submitting ? 'Aguarde...' : mode === 'login' ? 'Entrar' : 'Criar e entrar'}
          </button>
        </form>
      </section>
    </div>
  )
}

function SellerDashboard({ user, products, onLogout, onRefresh, notice, setNotice }) {
  const [editingId, setEditingId] = useState(null)
  const [form, setForm] = useState(emptyProduct)
  const isAdmin = user.role === 'admin'

  function updateField(field, value) {
    setForm((current) => ({ ...current, [field]: value }))
  }

  function startEdit(product) {
    setEditingId(product.id)
    setForm({
      name: product.name || '',
      description: product.description || '',
      price: String(product.price || ''),
      stock: String(product.stock || ''),
      photo_url: product.photo_url || '',
    })
  }

  function clearForm() {
    setEditingId(null)
    setForm(emptyProduct)
  }

  async function handleSubmit(event) {
    event.preventDefault()
    const payload = {
      name: form.name,
      description: form.description,
      price: Number(form.price),
      stock: Number(form.stock),
      photo_url: form.photo_url || null,
    }

    try {
      if (editingId) {
        await updateProduct(editingId, payload)
        setNotice('Produto atualizado.')
      } else {
        await createProduct(payload)
        setNotice('Produto criado.')
      }

      clearForm()
      await onRefresh()
    } catch (error) {
      setNotice(error.message)
    }
  }

  async function handleDelete(productId) {
    try {
      await deleteProduct(productId)
      setNotice('Produto removido.')
      await onRefresh()
    } catch (error) {
      setNotice(error.message)
    }
  }

  return (
    <main className="app-shell">
      <AppTopbar
        title={isAdmin ? 'Painel administrativo' : 'Painel do vendedor'}
        subtitle={`Ola, ${user.username}`}
        onLogout={onLogout}
      />

      <section className="seller-layout">
        <form className="product-form" onSubmit={handleSubmit}>
          <span className="eyebrow">{editingId ? 'Editar produto' : 'Novo produto'}</span>
          <h2>{editingId ? 'Atualize a vitrine' : 'Cadastre uma oferta'}</h2>
          <label>
            Nome
            <input
              value={form.name}
              onChange={(event) => updateField('name', event.target.value)}
              required
            />
          </label>
          <label>
            Descricao
            <textarea
              value={form.description}
              onChange={(event) => updateField('description', event.target.value)}
              rows="4"
            />
          </label>
          <div className="form-row">
            <label>
              Preco
              <input
                type="number"
                min="0.01"
                step="0.01"
                value={form.price}
                onChange={(event) => updateField('price', event.target.value)}
                required
              />
            </label>
            <label>
              Estoque
              <input
                type="number"
                min="0"
                value={form.stock}
                onChange={(event) => updateField('stock', event.target.value)}
                required
              />
            </label>
          </div>
          <label>
            URL da imagem
            <input
              type="url"
              value={form.photo_url}
              onChange={(event) => updateField('photo_url', event.target.value)}
              placeholder="https://..."
            />
          </label>
          <div className="form-actions">
            <button className="primary-button">{editingId ? 'Salvar' : 'Publicar'}</button>
            {editingId && (
              <button type="button" className="ghost-button" onClick={clearForm}>
                Cancelar
              </button>
            )}
          </div>
        </form>

        <section className="inventory-panel">
          <div className="section-heading">
            <span className="eyebrow">{products.length} itens</span>
            <h2>Seus produtos</h2>
          </div>
          <div className="inventory-list">
            {products.length === 0 && (
              <p className="empty-state">Sua vitrine ainda esta vazia.</p>
            )}
            {products.map((product) => (
              <article className="inventory-item" key={product.id}>
                <img src={productImage(product)} alt="" />
                <div>
                  <h3>{product.name}</h3>
                  <p>{product.description || 'Sem descricao cadastrada.'}</p>
                  <strong>{formatCurrency(product.price)}</strong>
                  <small>Estoque: {product.stock}</small>
                </div>
                <div className="item-actions">
                  <button onClick={() => startEdit(product)}>Editar</button>
                  <button className="danger-button" onClick={() => handleDelete(product.id)}>
                    Excluir
                  </button>
                </div>
              </article>
            ))}
          </div>
        </section>
      </section>

      {notice && <div className="toast">{notice}</div>}
    </main>
  )
}

function CustomerStorefront({ user, products, onLogout, onFinish, notice, onRefresh, setNotice }) {
  const [cart, setCart] = useState([])
  const [query, setQuery] = useState('')
  const [submitting, setSubmitting] = useState(false)

  const filteredProducts = useMemo(() => {
    const normalizedQuery = query.trim().toLowerCase()
    if (!normalizedQuery) {
      return products
    }

    return products.filter((product) => {
      const sellerName = product.seller?.username || ''
      return [product.name, product.description, sellerName]
        .filter(Boolean)
        .some((value) => value.toLowerCase().includes(normalizedQuery))
    })
  }, [products, query])

  const subtotal = cart.reduce((total, item) => total + item.product.price * item.quantity, 0)

  function addToCart(product) {
    const sellerId = cart[0]?.product.seller_id
    if (sellerId && sellerId !== product.seller_id) {
      setNotice('Por enquanto, o carrinho aceita produtos de um vendedor por pedido.')
      return
    }

    setCart((current) => {
      const existing = current.find((item) => item.product.id === product.id)
      if (existing) {
        return current.map((item) =>
          item.product.id === product.id
            ? { ...item, quantity: Math.min(item.quantity + 1, product.stock) }
            : item
        )
      }

      return [...current, { product, quantity: 1 }]
    })
  }

  function updateQuantity(productId, quantity) {
    setCart((current) =>
      current
        .map((item) =>
          item.product.id === productId
            ? { ...item, quantity: Math.max(1, Math.min(quantity, item.product.stock)) }
            : item
        )
        .filter((item) => item.quantity > 0)
    )
  }

  function removeFromCart(productId) {
    setCart((current) => current.filter((item) => item.product.id !== productId))
  }

  async function finishOrder() {
    setSubmitting(true)
    try {
      const order = await createOrder(
        cart.map((item) => ({
          product_id: item.product.id,
          quantity: item.quantity,
        }))
      )
      setCart([])
      await onRefresh()
      onFinish(order)
    } catch (error) {
      setNotice(error.message)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <main className="app-shell">
      <AppTopbar
        title="Produtos disponiveis"
        subtitle={`Boa compra, ${user.username}`}
        onLogout={onLogout}
      />

      <section className="store-hero">
        <div>
          <span className="eyebrow">Vitrine da cidade</span>
          <h1>Escolha produtos frescos, rapidos e perto de voce</h1>
        </div>
      </section>

      <section className="store-tools">
        <label>
          Buscar produto ou vendedor
          <input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Pizza, bolo, mercado..."
          />
        </label>
      </section>

      <section className="customer-layout">
        <div className="product-grid">
        {filteredProducts.length === 0 && (
          <p className="empty-state">Nenhum produto publicado ainda.</p>
        )}
        {filteredProducts.map((product) => {
          const sellerName = product.seller?.username || `Vendedor #${product.seller_id}`

          return (
            <article className="product-card" key={product.id}>
              <img src={productImage(product)} alt="" />
              <div className="product-body">
                <span>{sellerName}</span>
                <h2>{product.name}</h2>
                <p>{product.description || 'Produto disponivel na vitrine.'}</p>
                <div className="product-footer">
                  <strong>{formatCurrency(product.price)}</strong>
                  <small>{product.stock} em estoque</small>
                </div>
                <button className="primary-button" onClick={() => addToCart(product)}>
                  Adicionar
                </button>
              </div>
            </article>
          )
        })}
        </div>

        <aside className="cart-panel">
          <span className="eyebrow">Seu carrinho</span>
          <h2>{cart.length ? `${cart.length} item(ns)` : 'Monte seu pedido'}</h2>
          <div className="cart-list">
            {cart.length === 0 && <p className="empty-state">Adicione produtos para ver o subtotal.</p>}
            {cart.map((item) => (
              <div className="cart-item" key={item.product.id}>
                <div>
                  <strong>{item.product.name}</strong>
                  <small>{formatCurrency(item.product.price)}</small>
                </div>
                <div className="quantity-control">
                  <button onClick={() => updateQuantity(item.product.id, item.quantity - 1)}>-</button>
                  <span>{item.quantity}</span>
                  <button onClick={() => updateQuantity(item.product.id, item.quantity + 1)}>+</button>
                </div>
                <button className="remove-button" onClick={() => removeFromCart(item.product.id)}>
                  Remover
                </button>
              </div>
            ))}
          </div>
          <div className="cart-total">
            <span>Subtotal</span>
            <strong>{formatCurrency(subtotal)}</strong>
          </div>
          <button className="primary-button full" disabled={!cart.length || submitting} onClick={finishOrder}>
            {submitting ? 'Finalizando...' : 'Finalizar pedido'}
          </button>
          <small className="payment-note">Pagamento real entra depois com a API escolhida.</small>
        </aside>
      </section>

      {notice && <div className="toast">{notice}</div>}
    </main>
  )
}

function ThankYouPage({ order, onBack, onLogout }) {
  const sellerName = order?.seller?.username || `Vendedor #${order?.seller_id}`

  return (
    <main className="thank-you-page">
      <AppTopbar
        title="Pedido finalizado"
        subtitle={`Pedido #${order?.id || ''}`}
        onLogout={onLogout}
      />
      <section className="thank-you-card">
        <span className="eyebrow">Obrigado pela preferencia</span>
        <h1>Seu pedido com {sellerName} foi recebido.</h1>
        <p>
          Total de {formatCurrency(order?.total)}. O pedido ficou aguardando pagamento,
          pronto para receber a confirmacao da API de pagamento escolhida.
        </p>
        <button className="primary-button" onClick={onBack}>
          Voltar para produtos
        </button>
      </section>
    </main>
  )
}

function AppTopbar({ title, subtitle, onLogout }) {
  return (
    <header className="app-topbar">
      <div>
        <span className="brand compact">DH</span>
        <div>
          <h1>{title}</h1>
          <p>{subtitle}</p>
        </div>
      </div>
      <button className="logout-button" onClick={onLogout}>
        Sair
      </button>
    </header>
  )
}
