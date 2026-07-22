const BACKEND_URL =
  process.env.NEXT_PUBLIC_API_URL ||
  process.env.API_URL ||
  process.env.VITE_API_URL ||
  process.env.BACKEND_URL ||
  'http://localhost:8000'

function buildBackendUrl(path, searchParams) {
  const cleanBase = BACKEND_URL.replace(/\/$/, '')
  const cleanPath = path.join('/')
  const query = searchParams.toString()

  return `${cleanBase}/${cleanPath}${query ? `?${query}` : ''}`
}

async function proxyRequest(request, context) {
  const { path } = await context.params
  const sourceUrl = new URL(request.url)
  const targetUrl = buildBackendUrl(path, sourceUrl.searchParams)
  const headers = new Headers(request.headers)

  headers.delete('host')

  const response = await fetch(targetUrl, {
    method: request.method,
    headers,
    body: ['GET', 'HEAD'].includes(request.method) ? undefined : await request.text(),
    cache: 'no-store',
  })

  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers: response.headers,
  })
}

export async function GET(request, context) {
  return proxyRequest(request, context)
}

export async function POST(request, context) {
  return proxyRequest(request, context)
}

export async function PUT(request, context) {
  return proxyRequest(request, context)
}

export async function DELETE(request, context) {
  return proxyRequest(request, context)
}
