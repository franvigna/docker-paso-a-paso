import { useEffect, useState } from 'react'
import { Becario, BecarioCreate } from './types'
import { BecariosList } from './components/BecariosList'
import { BecarioForm } from './components/BecarioForm'

// URL base de la API — el navegador llama a localhost:8000 directamente
const API = 'http://localhost:8000'

export default function App() {
  const [becarios, setBecarios] = useState<Becario[]>([])

  // Carga los becarios al montar el componente
  async function cargarBecarios() {
    const res = await fetch(`${API}/becarios`)
    const data = await res.json()
    setBecarios(data)
  }

  useEffect(() => { cargarBecarios() }, [])

  async function handleCrear(becario: BecarioCreate) {
    const res = await fetch(`${API}/becarios`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(becario),
    })
    if (!res.ok) {
      const err = await res.json()
      throw new Error(err.detail ?? 'Error al crear')
    }
    await cargarBecarios() // recarga la lista tras crear
  }

  async function handleEliminar(id: number) {
    await fetch(`${API}/becarios/${id}`, { method: 'DELETE' })
    await cargarBecarios() // recarga la lista tras eliminar
  }

  return (
    <div style={{ padding: 24, fontFamily: 'sans-serif' }}>
      <h1>Becarios</h1>

      <h2>Nuevo Becario</h2>
      <BecarioForm onCrear={handleCrear} />

      <h2 style={{ marginTop: 32 }}>Lista de Becarios</h2>
      <BecariosList becarios={becarios} onEliminar={handleEliminar} />
    </div>
  )
}
