const API_URL = import.meta.env.VITE_API_URL

export async function createProduct(product) {
  const response = await fetch(`${API_URL}/products/`, {//só muda essas rotas caso mude a rota no backend
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(product)
  })

  if (!response.ok) {
    throw new Error('Failed to create product')
  }

  return await response.json()
}

export async function getProductById(productId) {
  const response = await fetch(`${API_URL}/products/${productId}`)

  if (!response.ok) {
    throw new Error('Product not found')
  }

  return await response.json()
}

export async function updateProduct(productId, product) {
  const response = await fetch(`${API_URL}/products/${productId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(product)
  })

  if (!response.ok) {
    throw new Error('Product not found')
  }

  return await response.json()
}

export async function deleteProduct(productId) {
  const response = await fetch(`${API_URL}/products/${productId}`, {
    method: 'DELETE'
  })

  if (!response.ok) {
    throw new Error('Product not found')
  }
}

export async function getProducts() {
  const response = await fetch(`${API_URL}/products/`)
  if (!response.ok) {
    if (response.status === 503) {
      throw new Error('Server is waking up. Please try again.')
    }
    throw new Error('Failed to fetch products')
  }
  return await response.json()
}