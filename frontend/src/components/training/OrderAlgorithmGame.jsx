import React, { useState } from 'react';

const OrderAlgorithmGame = () => {
  // Datos falsos iniciales desordenados para maquetar
  const [blocks, setBlocks] = useState([
    { id: 'b1', text: 'return user;', order: 1 },
    { id: 'b2', text: 'if (password === user.password) {', order: 2 },
    { id: 'b3', text: 'const user = db.find(username);', order: 3 },
    { id: 'b4', text: '}', order: 4 },
  ]);

  // Función sencilla para mover bloques arriba y abajo visualmente
  const moveBlock = (index, direction) => {
    if ((direction === -1 && index === 0) || (direction === 1 && index === blocks.length - 1)) return;
    
    const newBlocks = [...blocks];
    const temp = newBlocks[index];
    newBlocks[index] = newBlocks[index + direction];
    newBlocks[index + direction] = temp;
    setBlocks(newBlocks);
  };

  return (
    <div className="w-full max-w-2xl mx-auto bg-gray-900 p-6 rounded-2xl shadow-inner border border-gray-700">
      <div className="mb-6 flex justify-between items-center">
        <h4 className="text-white font-bold text-lg flex items-center gap-2">
          <span>🧩</span> Ordena la secuencia de Login
        </h4>
        <span className="bg-gray-800 text-gray-400 text-xs px-3 py-1 rounded-full border border-gray-600">
          ORDER_ALGORITHM
        </span>
      </div>

      <div className="space-y-3">
        {blocks.map((block, index) => (
          <div 
            key={block.id}
            className="flex items-center gap-4 bg-gray-800 border border-gray-600 p-3 rounded-xl hover:border-blue-500 transition-colors group"
          >
            {/* Ícono de arrastre (visual) */}
            <div className="text-gray-500 cursor-grab active:cursor-grabbing group-hover:text-blue-400 px-2">
              ⋮⋮
            </div>

            {/* Código */}
            <div className="flex-1 font-mono text-blue-300 text-sm md:text-base overflow-x-auto">
              {block.text}
            </div>

            {/* Controles para mover (Subir / Bajar) */}
            <div className="flex flex-col gap-1">
              <button 
                onClick={() => moveBlock(index, -1)}
                disabled={index === 0}
                className="text-gray-400 hover:text-white disabled:opacity-30 hover:bg-gray-700 p-1 rounded transition-colors"
                title="Subir"
              >
                ▲
              </button>
              <button 
                onClick={() => moveBlock(index, 1)}
                disabled={index === blocks.length - 1}
                className="text-gray-400 hover:text-white disabled:opacity-30 hover:bg-gray-700 p-1 rounded transition-colors"
                title="Bajar"
              >
                ▼
              </button>
            </div>
          </div>
        ))}
      </div>
      
      {/* Nota visual del estado actual */}
      <div className="mt-6 text-center text-gray-500 text-sm">
        Orden actual: {blocks.map(b => b.id).join(' ➔ ')}
      </div>
    </div>
  );
};

export default OrderAlgorithmGame;