const mockTrainingData = {
  access_level: "PRO",
  daily_limit: 10,
  cycle_date: "2026-10-18",
  completed_count: 0,
  exercises: [
    {
      number: 1,
      name: "Flujo de Autenticación",
      type: "ORDER_ALGORITHM",
      difficulty: "EASY",
      skill: "Lógica",
      state: "AVAILABLE" // ¡Botón 1 activado!
    },
    {
      number: 2,
      name: "Inyección SQL clásica",
      type: "FIND_ERROR",
      difficulty: "MEDIUM",
      skill: "Seguridad",
      state: "AVAILABLE" // ¡Botón 2 activado!
    },
    {
      number: 3,
      name: "Diccionario Hacker",
      type: "MATCH_CONCEPTS",
      difficulty: "EASY",
      skill: "Teoría",
      state: "AVAILABLE" // ¡Botón 3 activado!
    },
    {
      number: 4,
      name: "Refactorización Limpia",
      type: "FILL_BLANKS",
      difficulty: "HARD",
      skill: "Clean Code",
      state: "BLOCKED_BY_SEQUENCE" // Bloqueado para ver que el diseño sigue funcionando
    },
    {
      number: 5,
      name: "Arquitectura de API",
      type: "MULTIPLE_CHOICE",
      difficulty: "MEDIUM",
      skill: "Sistemas",
      state: "NOT_ACCESSIBLE_BY_LEVEL" // Bloqueado por nivel
    }
  ]
};

export default mockTrainingData;
