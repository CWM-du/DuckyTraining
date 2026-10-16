export const mockOverviewData = {
  access_level: "FREE",
  daily_limit: 3,
  cycle_date: "2026-10-13",
  completed_count: 1,
  streak: 4, // Dato visual para tu cabecera
  ducky_coins: 150, // Dato visual para tu cabecera
  exercises: [
    {
      number: 1,
      name: "Algoritmo de Login",
      type: "ORDER_ALGORITHM",
      difficulty: "EASY",
      skill: "Logic",
      state: "COMPLETED_TODAY" // Check verde
    },
    {
      number: 2,
      name: "Ordena el Algoritmo",
      type: "ORDER_ALGORITHM",
      difficulty: "MEDIUM",
      skill: "Debugging",
      state: "AVAILABLE" // Botón "¡Jugar!" brillante
    },
    {
      number: 3,
      name: "Red de Oficina",
      type: "CONNECT_NETWORK",
      difficulty: "HARD",
      skill: "Networking",
      state: "BLOCKED_BY_SEQUENCE" // Candado
    },
    {
      number: 4,
      name: "Ataque SQLi",
      type: "FIND_ERROR",
      difficulty: "EASY",
      skill: "Security",
      state: "NOT_ACCESSIBLE_BY_LEVEL" // Grisáceo, etiqueta "PLUS/PRO"
    }
  ]
};