// Tipos que representan los datos del becario — deben coincidir con los modelos Pydantic del backend
export type Categoria = 'Inicial' | 'Intermedio' | 'Superior' | 'Líder' | 'Senior'

export interface Becario {
  id: number
  dni: string
  nombre: string
  apellido: string
  fecha_ingreso: string
  categoria: Categoria
}

export interface BecarioCreate {
  dni: string
  nombre: string
  apellido: string
  fecha_ingreso: string
  categoria: Categoria
}
