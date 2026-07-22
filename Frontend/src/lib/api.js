const API_URL = (process.env.NEXT_PUBLIC_API_URL || '/api/backend').replace(/\/$/, '')
const REQUEST_TIMEOUT_MS = 15000

function getToken() {
  if (typeof window === 'undefined') {
    return null
  }

  return localStorage.getItem('delivery_token')
}

async function request(path, options = {}) {
  const controller = new AbortController()
  const timeoutId = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS)
  const token = getToken()
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  }

  if (token) {
    headers.Authorization = `Bearer ${token}`
  }

  const url = `${API_URL}${path}`
  let response

  try {
    response = await fetch(url, {
      ...options,
      headers,
      signal: controller.signal,
    })
  } catch (error) {
    if (error.name === 'AbortError') {
      throw new Error('O servidor demorou para responder. Tente novamente.')
    }

    throw new Error('Nao foi possivel conectar ao servidor.')
  } finally {
    clearTimeout(timeoutId)
  }

  if (response.status === 204) {
    return null
  }

  const data = await response.json().catch(() => null)

  if (!response.ok) {
    throw new Error(data?.detail || 'Nao foi possivel concluir a acao.')
  }

  return data
}

export async function registerUser(payload) {
  return request('/auth/register', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export async function loginUser(payload) {
  return request('/auth/login', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export async function getCurrentUser() {
  return request('/auth/me')
}

export async function logoutUser() {
  return request('/auth/logout', {
    method: 'POST',
  }).catch(() => null)
}

export async function getProducts() {
  return request('/products/')
}

export async function createProduct(product) {
  return request('/products/', {
    method: 'POST',
    body: JSON.stringify(product),
  })
}

export async function updateProduct(productId, product) {
  return request(`/products/${productId}`, {
    method: 'PUT',
    body: JSON.stringify(product),
  })
}

export async function deleteProduct(productId) {
  return request(`/products/${productId}`, {
    method: 'DELETE',
  })
}

export async function createOrder(items) {
  return request('/orders/', {
    method: 'POST',
    body: JSON.stringify({ items }),
  })
}
