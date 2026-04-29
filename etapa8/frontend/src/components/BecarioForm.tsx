import { useState } from 'react'
import { BecarioCreate, Categoria } from '../types'

interface Props {
  onCrear: (becario: BecarioCreate) => Promise<void>
}

const CATEGORIAS: Categoria[] = ['Inicial', 'Intermedio', 'Superior', 'Líder', 'Senior']

const VACIO: BecarioCreate = {
  dni: '',
  nombre: '',
  apellido: '',
  fecha_ingreso: '',
  categoria: 'Inicial',
}

export function BecarioForm({ onCrear }: Props) {
  const [form, setForm] = useState<BecarioCreate>(VACIO)
  const [error, setError] = useState('')

  function handleChange(e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError('')
    try {
      await onCrear(form)
      setForm(VACIO) // limpiar formulario tras crear exitosamente
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Error al crear becario')
    }
  }

  return (
    <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 8, maxWidth: 400 }}>
      <input name="dni"           placeholder="DNI"      value={form.dni}           onChange={handleChange} required />
      <input name="nombre"        placeholder="Nombre"   value={form.nombre}        onChange={handleChange} required />
      <input name="apellido"      placeholder="Apellido" value={form.apellido}       onChange={handleChange} required />
      <input name="fecha_ingreso" type="date"            value={form.fecha_ingreso}  onChange={handleChange} required />
      <select name="categoria" value={form.categoria} onChange={handleChange}>
        {CATEGORIAS.map((c) => <option key={c} value={c}>{c}</option>)}
      </select>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <button type="submit">Crear Becario</button>
    </form>
  )
}
