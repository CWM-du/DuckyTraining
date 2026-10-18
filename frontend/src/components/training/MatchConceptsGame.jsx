import React, { useState } from 'react';

const MatchConceptsGame = () => {
  // Datos falsos: Conceptos a la izquierda y definiciones a la derecha
  const leftItems = [
    { id: 'L1', text: 'Inyección SQL' },
    { id: 'L2', text: 'XSS' },
    { id: 'L3', text: 'Fuerza Bruta' }
  ];
  
  const rightItems = [
    { id: 'R1', text: 'Inyección de scripts maliciosos en el navegador' },
    { id: 'R2', text: 'Múltiples intentos automatizados de login' },
    { id: 'R3', text: 'Manipulación de consultas a la base de datos' }
  ];

  // Estados para manejar la selección y las parejas formadas
  const [selectedLeft, setSelectedLeft] = useState(null);
  const [selectedRight, setSelectedRight] = useState(null);
  const [matches, setMatches] = useState([]); // Array de objetos { left: id, right: id }

  // Función para manejar los clics y emparejar
  const handleSelect = (side, id) => {
    // Si ya está emparejado, no hacemos nada
    if (matches.find(m => m.left === id || m.right === id)) return;

    if (side === 'left') {
      setSelectedLeft(id === selectedLeft ? null : id);
    } else {
      setSelectedRight(id === selectedRight ? null : id);
    }
  };

  // Efecto visual instantáneo cuando se seleccionan ambos lados
  React.useEffect(() => {
    if (selectedLeft && selectedRight) {
      setMatches([...matches, { left: selectedLeft, right: selectedRight }]);
      setSelectedLeft(null);
      setSelectedRight(null);
    }
  }, [selectedLeft, selectedRight, matches]);

  // Función auxiliar para saber el estado de un ítem
  const getItemStatus = (side, id) => {
    const isMatched = matches.find(m => m[side] === id);
    if (isMatched) return 'matched';
    if (side === 'left' && selectedLeft === id) return 'selected';
    if (side === 'right' && selectedRight === id) return 'selected';
    return 'default';
  };

  return (
    <div className="w-full max-w-3xl mx-auto bg-gray-900 p-6 rounded-2xl shadow-inner border border-gray-700">
      
      {/* Cabecera */}
      <div className="mb-6 flex justify-between items-center">
        <h4 className="text-white font-bold text-lg flex items-center gap-2">
           Conecta los conceptos
        </h4>
        <div className="flex gap-4">
          <button 
            onClick={() => setMatches([])}
            className="text-gray-400 hover:text-white text-sm underline transition-colors"
          >
            Reiniciar parejas
          </button>
          <span className="bg-gray-800 text-gray-400 text-xs px-3 py-1 rounded-full border border-gray-600">
            MATCH_CONCEPTS
          </span>
        </div>
      </div>

      {/* Tablero de dos columnas */}
      <div className="grid grid-cols-2 gap-8">
        
        {/* Columna Izquierda */}
        <div className="flex flex-col gap-3">
          {leftItems.map((item) => {
            const status = getItemStatus('left', item.id);
            return (
              <button
                key={item.id}
                onClick={() => handleSelect('left', item.id)}
                className={`p-4 rounded-xl text-left font-bold transition-all border-2
                  ${status === 'default' ? 'bg-gray-800 border-gray-600 text-gray-300 hover:border-blue-400 hover:bg-gray-700' : ''}
                  ${status === 'selected' ? 'bg-blue-900/50 border-blue-500 text-blue-300 shadow-[0_0_15px_rgba(59,130,246,0.3)]' : ''}
                  ${status === 'matched' ? 'bg-green-900/30 border-green-700 text-green-500 opacity-50 cursor-not-allowed' : ''}
                `}
              >
                {item.text}
              </button>
            );
          })}
        </div>

        {/* Columna Derecha */}
        <div className="flex flex-col gap-3">
          {rightItems.map((item) => {
            const status = getItemStatus('right', item.id);
            return (
              <button
                key={item.id}
                onClick={() => handleSelect('right', item.id)}
                className={`p-4 rounded-xl text-left text-sm transition-all border-2
                  ${status === 'default' ? 'bg-gray-800 border-gray-600 text-gray-300 hover:border-blue-400 hover:bg-gray-700' : ''}
                  ${status === 'selected' ? 'bg-blue-900/50 border-blue-500 text-blue-300 shadow-[0_0_15px_rgba(59,130,246,0.3)]' : ''}
                  ${status === 'matched' ? 'bg-green-900/30 border-green-700 text-green-500 opacity-50 cursor-not-allowed' : ''}
                `}
              >
                {item.text}
              </button>
            );
          })}
        </div>

      </div>
    </div>
  );
};

export default MatchConceptsGame;