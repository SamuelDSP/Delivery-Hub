const BACKEND_URL =
  process.env.API_URL ||
  process.env.VITE_API_URL ||
  process.env.BACKEND_URL ||
  process.env.NEXT_PUBLIC_API_URL ||
  'http://localhost:8000'
const PROXY_TIMEOUT_MS = 15000

export const runtime = 'nodejs'

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
  const controller = new AbortController()
  const timeoutId = setTimeout(() => controller.abort(), PROXY_TIMEOUT_MS)

  headers.delete('host')
  headers.delete('connection')
  headers.delete('content-length')

  try {
    const response = await fetch(targetUrl, {
      method: request.method,
      headers,
      body: ['GET', 'HEAD'].includes(request.method) ? undefined : await request.arrayBuffer(),
      cache: 'no-store',
      signal: controller.signal,
    })

    const responseHeaders = new Headers(response.headers)
    responseHeaders.delete('content-encoding')
    responseHeaders.delete('content-length')
    responseHeaders.delete('transfer-encoding')

    return new Response(await response.arrayBuffer(), {
      status: response.status,
      statusText: response.statusText,
      headers: responseHeaders,
    })
  } catch (error) {
    const message =
      error.name === 'AbortError'
        ? 'Backend demorou para responder.'
        : 'Nao foi possivel conectar ao backend.'

    return Response.json({ detail: message }, { status: 504 })
  } finally {
    clearTimeout(timeoutId)
  }
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
