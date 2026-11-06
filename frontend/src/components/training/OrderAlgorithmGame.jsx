import React, { useState, useRef, useEffect } from 'react';

// CAMBIO 1: Recibimos las props 'data' (para cargar el nivel real) y 'onChange' (para avisar al padre)
const OrderAlgorithmGame = ({ data, onChange }) => {
  const [blocks, setBlocks] = useState([
    { id: 'b1', text: 'return user;', order: 1 },
    { id: 'b2', text: 'if (password === user.password) {', order: 2 },
    { id: 'b3', text: 'const user = db.find(username);', order: 3 },
    { id: 'b4', text: '}', order: 4 },
  ]);

// Cargar datos REALES desde el backend
  useEffect(() => {
    // Si Django nos envía el JSON real y trae la llave 'bloques'
    if (data && data.bloques) {
      
      // Transformamos tu JSON al formato que usan nuestras tarjetas arrastrables
      const bloquesFormateados = data.bloques.map(item => ({
        id: item.id,       // En tu JSON: 'B91008', 'B83201', etc.
        text: item.linea   // En tu JSON: 'a = 2', 'b = 5', etc.
      }));
      
      // NOTA: Si tu variable de estado se llama distinto, cambia 'setBlocks' por tu nombre (ej. setItems)
      setBlocks(bloquesFormateados); 
    }
  }, [data]);

  const dragItem = useRef(null);
  const dragOverItem = useRef(null);

  // CAMBIO 2: Función auxiliar para avisar a Django del nuevo orden
  const notifyChange = (newBlocks) => {
    if (onChange) {
      // Extraemos solo los IDs en el nuevo orden para enviarlos al backend
      const ordenIds = newBlocks.map(block => block.id);
      
      // ATENCIÓN: Si tu backend de Django espera otra clave (ej: 'order', 'sequence', 'user_order')
      // cambialo aquí abajo. De momento lo llamamos 'ordered_ids'.
      onChange({ ordered_ids: ordenIds });
    }
  };

  // --- LÓGICA DE DRAG AND DROP NATIVO ---
  const handleDragStart = (e, position) => {
    dragItem.current = position;
    setTimeout(() => {
      e.target.classList.add('opacity-40', 'border-blue-500');
    }, 0);
  };

  const handleDragEnter = (e, position) => {
    dragOverItem.current = position;
  };

  const handleDragEnd = (e) => {
    e.target.classList.remove('opacity-40', 'border-blue-500');

    if (dragItem.current !== null && dragOverItem.current !== null && dragItem.current !== dragOverItem.current) {
      const newBlocks = [...blocks];
      const draggedItemContent = newBlocks[dragItem.current];
      
      newBlocks.splice(dragItem.current, 1);
      newBlocks.splice(dragOverItem.current, 0, draggedItemContent);
      
      setBlocks(newBlocks);
      notifyChange(newBlocks); // <-- Avisamos del cambio tras arrastrar
    }
    
    dragItem.current = null;
    dragOverItem.current = null;
  };

  // --- LÓGICA DE LAS FLECHAS (Accesibilidad) ---
  const moveBlock = (index, direction) => {
    if ((direction === -1 && index === 0) || (direction === 1 && index === blocks.length - 1)) return;
    
    const newBlocks = [...blocks];
    const temp = newBlocks[index];
    newBlocks[index] = newBlocks[index + direction];
    newBlocks[index + direction] = temp;
    
    setBlocks(newBlocks);
    notifyChange(newBlocks); // <-- Avisamos del cambio tras pulsar flechas
  };

  return (
    <div className="w-full max-w-2xl mx-auto bg-gray-900 p-6 rounded-2xl shadow-inner border border-gray-700">
      <div className="mb-6 flex justify-between items-center">
        <h4 className="text-white font-bold text-lg">
          Ordena la secuencia lógica
        </h4>
        <span className="bg-gray-800 text-gray-400 text-xs px-3 py-1 rounded-full border border-gray-600">
          ORDER_ALGORITHM
        </span>
      </div>

      <div className="space-y-3">
        {blocks.map((block, index) => (
          <div 
            key={block.id}
            draggable 
            onDragStart={(e) => handleDragStart(e, index)}
            onDragEnter={(e) => handleDragEnter(e, index)}
            onDragEnd={handleDragEnd}
            onDragOver={(e) => e.preventDefault()} 
            className="flex items-center gap-4 bg-gray-800 border border-gray-600 p-3 rounded-xl hover:border-blue-500 transition-colors group cursor-grab active:cursor-grabbing"
          >
            <div className="text-gray-500 group-hover:text-blue-400 px-2">
              ⋮⋮
            </div>

            <div className="flex-1 font-mono text-blue-300 text-sm md:text-base overflow-x-auto select-none">
              {block.text}
            </div>

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