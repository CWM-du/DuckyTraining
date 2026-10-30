export const mockTrainingDataReal = {
  user_profile: {
    username: "developer_user",
    level: "FREE",
    ducky_coins: 150,
    streak_days: 4
  },
  daily_cycle: {
    date: "2026-10-30", // Fecha de hoy
    total_exercises: 3,
    completed_exercises: 0,
    exercises: [
      {
        id: "ex_101",
        order: 1,
        type: "ORDER_ALGORITHM",
        title: "Ordena la secuencia de Login",
        instructions: "Arrastra o mueve las líneas de código para formar la estructura correcta de autenticación.",
        state: "AVAILABLE",
        reward_coins: 10,
        content: {
          blocks: [
             // Contenido del JSON 1 de Oscar, adaptado al contrato
            { id: "1", text: "return user;" },
            { id: "2", text: "if (password === user.password) {" },
            { id: "3", text: "const user = db.find(username);" },
            { id: "4", text: "}" }
          ]
        }
      },
      {
        id: "ex_102",
        order: 2,
        type: "MATCH_CONCEPTS",
        title: "Asocia los conceptos de Seguridad",
        instructions: "Selecciona un concepto de la izquierda y conéctalo con su definición correcta a la derecha.",
        state: "AVAILABLE", // Lo pongo en AVAILABLE para que lo puedas probar directamente
        reward_coins: 15,
        content: {
           // Contenido del JSON 2 de Oscar, adaptado al contrato
          left_column: [
            { id: "a", text: "JWT" },
            { id: "b", text: "CSRF" },
            { id: "c", text: "Bcrypt" }
          ],
          right_column: [
            { id: "x", text: "Algoritmo de hashing para contraseñas" },
            { id: "y", text: "Token de autenticación firmado digitalmente" },
            { id: "z", text: "Ataque de falsificación de petición en sitio cruzado" }
          ]
        }
      },
      {
        id: "ex_103",
        order: 3,
        type: "FIND_ERROR",
        title: "Encuentra la vulnerabilidad SQLi",
        instructions: "Haz clic sobre la línea de código que contiene el fallo de seguridad.",
        state: "AVAILABLE", // Lo pongo en AVAILABLE para que lo puedas probar directamente
        reward_coins: 20,
        content: {
           // Contenido del JSON 3 de Oscar, adaptado al contrato
          code_snippet: [
            { line_number: 1, code: "def get_user_profile(request):" },
            { line_number: 2, code: "    username = request.GET.get('user')" },
            { line_number: 3, code: "    query = f\"SELECT * FROM users WHERE name = '{username}'\"" },
            { line_number: 4, code: "    return db.execute(query)" }
          ]
        }
      }
    ]
  }
};