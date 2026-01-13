import { useEffect, useState } from 'react'
import {
  getProducts,
  createProduct,
  updateProduct,
  deleteProduct
} from '../api'

function Products() {
  const [products, setProducts] = useState([])

  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [price, setPrice] = useState('')
  const [stock, setStock] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)


  const [editingId, setEditingId] = useState(null)

async function loadProducts() {
  setLoading(true)
  setError(null)

  try {
    const data = await getProducts()
    setProducts(data)
  } catch (err) {
    setError(err.message)
  } finally {
    setLoading(false)
  }
}

  useEffect(() => {
    loadProducts()
  }, [])

  function handleSubmit(event) {
    event.preventDefault()

    const product = {
      name: name,
      description: description,
      price: Number(price),
      stock: Number(stock)
    }

    if (editingId === null) {
      createProduct(product).then(() => {
        clearForm()
        loadProducts()
      })
    }

    if (editingId !== null) {
      updateProduct(editingId, product).then(() => {
        clearForm()
        loadProducts()
      })
    }
  }

  function handleEdit(product) {
    setName(product.name ?? '')
    setDescription(product.description ?? '')
    setPrice(product.price ?? '')
    setStock(product.stock ?? '')
    setEditingId(product.id)
  }

  function handleDelete(id) {
    deleteProduct(id).then(() => {
      loadProducts()
    })
  }

  function clearForm() {
    setName('')
    setDescription('')
    setPrice('')
    setStock('')
    setEditingId(null)
  }

  function renderSubmitButton() {
    if (editingId === null) {
      return <button type="submit">Create</button>
    }

    return <button type="submit">Update</button>
  }

  function renderCancelButton() {
    if (editingId !== null) {
      return (
        <button type="button" onClick={clearForm}>
          Cancel
        </button>
      )
    }

    return null
  }

  if (loading) {
  return <p>Loading products...</p>
}

if (error !== null) {
  return (
    <div>
      <p>{error}</p>
      <button onClick={loadProducts}>Try again</button>
    </div>
  )
}

return (
  <div>
    <h1>Products</h1>

    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Name"
        value={name}
        onChange={event => setName(event.target.value)}
        required
      />

      <input
        type="text"
        placeholder="Description"
        value={description}
        onChange={event => setDescription(event.target.value)}
      />

      <input
        type="number"
        placeholder="Price"
        value={price}
        onChange={event => setPrice(event.target.value)}
        min="0"
        step="0.01"
        required
      />

      <input
        type="number"
        placeholder="Stock"
        value={stock}
        onChange={event => setStock(event.target.value)}
        min="0"
        required
      />

      {renderSubmitButton()}
      {renderCancelButton()}
    </form>

    <ul>
      {products.map(product => (
        <li key={product.id}>
          <strong>{product.name}</strong> — ${product.price} — stock: {product.stock}

          <button onClick={() => handleEdit(product)}>
            Edit
          </button>

          <button onClick={() => handleDelete(product.id)}>
            Delete
          </button>
        </li>
      ))}
    </ul>
  </div>
)

}

export default Products