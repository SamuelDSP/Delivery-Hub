import './globals.css'

export const metadata = {
  title: 'Delivery Hub',
  description: 'Sistema de delivery para clientes e vendedores',
}

export default function RootLayout({ children }) {
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  )
}
