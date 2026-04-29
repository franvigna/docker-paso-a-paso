import { Becario } from '../types'

interface Props {
  becarios: Becario[]
  onEliminar: (id: number) => void
}

export function BecariosList({ becarios, onEliminar }: Props) {
  if (becarios.length === 0) {
    return <p>No hay becarios cargados.</p>
  }

  return (
    <table border={1} cellPadding={8} style={{ borderCollapse: 'collapse', width: '100%' }}>
      <thead>
        <tr>
          <th>ID</th>
          <th>DNI</th>
          <th>Nombre</th>
          <th>Apellido</th>
          <th>Ingreso</th>
          <th>Categoría</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        {becarios.map((b) => (
          <tr key={b.id}>
            <td>{b.id}</td>
            <td>{b.dni}</td>
            <td>{b.nombre}</td>
            <td>{b.apellido}</td>
            <td>{b.fecha_ingreso}</td>
            <td>{b.categoria}</td>
            <td>
              <button onClick={() => onEliminar(b.id)}>Eliminar</button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
