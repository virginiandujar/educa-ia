import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Interacción con agentes | Educa IA',
  description:
    'Material didáctico para comprender qué es un agente de IA, cómo interactuar con él y qué capacidades conviene mantener dentro de la empresa.',
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  );
}
