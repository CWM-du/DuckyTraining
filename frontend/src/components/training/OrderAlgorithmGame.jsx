import React, { useState, useRef } from 'react';

const OrderAlgorithmGame = () => {
  const [blocks, setBlocks] = useState([
    { id: 'b1', text: 'return user;', order: 1 },
    { id: 'b2', text: 'if (password === user.password) {', order: 2 },
    { id: 'b3', text: 'const user = db.find(username);', order: 3 },
    { id: 'b4', text: '}', order: 4 },
  ]);

  // Referencias para saber qué elemento estamos arrastrando y sobre cuál pasamos
  const dragItem = useRef(null);
  const dragOverItem = useRef(null);

  // --- LÓGICA DE DRAG AND DROP NATIVO ---
  
  const handleDragStart = (e, position) => {
    dragItem.current = position;
    // Efecto visual para que se vea un poco transparente al arrastrar
    setTimeout(() => {
      e.target.classList.add('opacity-40', 'border-blue-500');
    }, 0);
  };

  const handleDragEnter = (e, position) => {
    dragOverItem.current = position;
  };

  const handleDragEnd = (e) => {
    // Quitamos las clases visuales al soltar
    e.target.classList.remove('opacity-40', 'border-blue-500');

    // Si hemos soltado en un sitio válido y distinto al original
    if (dragItem.current !== null && dragOverItem.current !== null && dragItem.current !== dragOverItem.current) {
      const newBlocks = [...blocks];
      const draggedItemContent = newBlocks[dragItem.current];
      
      // Sacamos el elemento de su posición original...
      newBlocks.splice(dragItem.current, 1);
      // ...y lo metemos en la nueva posición
      newBlocks.splice(dragOverItem.current, 0, draggedItemContent);
      
      setBlocks(newBlocks);
    }
    
    // Reseteamos las referencias
    dragItem.current = null;
    dragOverItem.current = null;
  };

  // --- LÓGICA ANTIGUA DE LAS FLECHAS (Accesibilidad) ---
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
        <h4 className="text-white font-bold text-lg">
          Ordena la secuencia de Login
        </h4>
        <span className="bg-gray-800 text-gray-400 text-xs px-3 py-1 rounded-full border border-gray-600">
          ORDER_ALGORITHM
        </span>
      </div>

      <div className="space-y-3">
        {blocks.map((block, index) => (
          <div 
            key={block.id}
            draggable // Magia: Esto hace que el div sea arrastrable
            onDragStart={(e) => handleDragStart(e, index)}
            onDragEnter={(e) => handleDragEnter(e, index)}
            onDragEnd={handleDragEnd}
            onDragOver={(e) => e.preventDefault()} // Necesario para permitir soltar
            className="flex items-center gap-4 bg-gray-800 border border-gray-600 p-3 rounded-xl hover:border-blue-500 transition-colors group cursor-grab active:cursor-grabbing"
          >
            {/* Ícono de arrastre */}
            <div className="text-gray-500 group-hover:text-blue-400 px-2">
              ⋮⋮
            </div>

            {/* Código */}
            <div className="flex-1 font-mono text-blue-300 text-sm md:text-base overflow-x-auto select-none">
              {block.text}
            </div>

            {/* Controles para mover con clic (Para móviles y accesibilidad) */}
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
    </div>
  );
};

export default OrderAlgorithmGame;