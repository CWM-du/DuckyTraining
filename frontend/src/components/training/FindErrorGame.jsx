import React, { useState } from 'react';

const FindErrorGame = () => {
  // Datos falsos: un fragmento de código dividido por líneas
  const [codeLines] = useState([
    { id: 1, text: "function authenticateUser(username, password) {" },
    { id: 2, text: "  // Vulnerabilidad de Inyección SQL clásica" },
    { id: 3, text: "  const query = `SELECT * FROM users WHERE username = '${username}'`;" },
    { id: 4, text: "  const user = database.execute(query);" },
    { id: 5, text: "  " },
    { id: 6, text: "  if (user && user.password === password) {" },
    { id: 7, text: "    return true;" },
    { id: 8, text: "  }" },
    { id: 9, text: "  return false;" },
    { id: 10, text: "}" }
  ]);

  // Estado para guardar la línea que el usuario ha seleccionado
  const [selectedLine, setSelectedLine] = useState(null);

  return (
    <div className="w-full max-w-2xl mx-auto bg-gray-900 p-6 rounded-2xl shadow-inner border border-gray-700">
      
      {/* Cabecera del juego */}
      <div className="mb-6 flex justify-between items-center">
        <h4 className="text-white font-bold text-lg flex items-center gap-2">
           Encuentra la vulnerabilidad
        </h4>
        <span className="bg-gray-800 text-gray-400 text-xs px-3 py-1 rounded-full border border-gray-600">
          FIND_ERROR
        </span>
      </div>

      {/* Editor de código simulado */}
      <div className="bg-[#1e1e1e] rounded-xl border border-gray-700 overflow-hidden font-mono text-sm py-4">
        {codeLines.map((line) => {
          const isSelected = selectedLine === line.id;
          
          return (
            <div 
              key={line.id}
              onClick={() => setSelectedLine(line.id)}
              className={`flex cursor-pointer transition-colors group px-4 py-1
                ${isSelected 
                  ? 'bg-blue-900/40 border-l-4 border-blue-500 text-blue-100' 
                  : 'hover:bg-gray-800 border-l-4 border-transparent text-gray-300'
                }`}
            >
              {/* Número de línea */}
              <div className={`w-8 text-right pr-4 select-none ${isSelected ? 'text-blue-400' : 'text-gray-600 group-hover:text-gray-400'}`}>
                {line.id}
              </div>
              
              {/* Texto del código */}
              <div className="whitespace-pre flex-1">
                {line.text || ' '}
              </div>
            </div>
          );
        })}
      </div>

      {/* Indicador de selección actual */}
      <div className="mt-6 text-center text-gray-400 text-sm h-6">
        {selectedLine ? (
          <span>Línea seleccionada: <strong className="text-blue-400">Línea {selectedLine}</strong></span>
        ) : (
          <span>Haz clic en una línea para seleccionarla</span>
        )}
      </div>
    </div>
  );
};

export default FindErrorGame;