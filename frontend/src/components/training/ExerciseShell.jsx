import React, { useState } from 'react';
import OrderAlgorithmGame from './OrderAlgorithmGame'; // Asegúrate de que este archivo está en la misma carpeta

const ExerciseShell = ({ exercise, onClose }) => {
  // Fases: 'INSTRUCTIONS' -> 'PLAYING' -> 'VALIDATING' -> 'FEEDBACK'
  const [phase, setPhase] = useState('INSTRUCTIONS');
  
  // Resultado simulado para la fase de feedback: 'SUCCESS' o 'ERROR'
  const [feedbackResult, setFeedbackResult] = useState(null);

  // Funciones para simular el flujo (tu compañero las conectará a la API real)
  const handleStart = () => setPhase('PLAYING');
  
  const handleSubmit = (simulatedResult) => {
    setPhase('VALIDATING');
    // Simulamos un tiempo de carga del servidor de 1.5 segundos
    setTimeout(() => {
      setFeedbackResult(simulatedResult);
      setPhase('FEEDBACK');
    }, 1500);
  };

  const handleRetry = () => setPhase('PLAYING');

  return (
    <div className="fixed inset-0 bg-gray-900/80 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="bg-white w-full max-w-3xl rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
        
        {/* HEADER DEL SHELL */}
        <div className="bg-gray-50 border-b border-gray-100 px-6 py-4 flex justify-between items-center">
          <div>
            <span className="text-xs font-bold text-gray-400 uppercase tracking-wider">Ejercicio {exercise.number}</span>
            <h2 className="text-xl font-bold text-gray-800">{exercise.name}</h2>
          </div>
          <button 
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 bg-gray-200 hover:bg-gray-300 rounded-full w-8 h-8 flex items-center justify-center transition-colors"
          >
            ✕
          </button>
        </div>

        {/* CONTENIDO PRINCIPAL (Cambia según la fase) */}
        <div className="p-8 overflow-y-auto flex-grow flex flex-col justify-center min-h-[400px]">
          
          {/* FASE 1: INSTRUCCIONES DINÁMICAS */}
          {phase === 'INSTRUCTIONS' && (
            <div className="text-center max-w-lg mx-auto">
              <div className="text-5xl mb-6">🎯</div>
              <h3 className="text-2xl font-bold text-gray-800 mb-4">Objetivo</h3>
              
              {/* Cambiamos el texto según el tipo de ejercicio */}
              {exercise.type === 'ORDER_ALGORITHM' ? (
                <p className="text-gray-600 mb-8 text-lg">
                  Lee los bloques de código desordenados y colócalos en la secuencia lógica correcta para que el algoritmo funcione.
                </p>
              ) : (
                <p className="text-gray-600 mb-8 text-lg">
                  Analiza el código y encuentra la línea exacta donde se está produciendo el error de seguridad o lógico.
                </p>
              )}

              <button 
                onClick={handleStart}
                className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-full text-lg transition-transform transform hover:scale-105"
              >
                Comenzar Reto
              </button>
            </div>
          )}

          {/* FASE 2: RESOLUCIÓN (El Juego) */}
          {phase === 'PLAYING' && (
            <div className="flex flex-col items-center w-full">
              
              {/* Aquí renderizamos el juego según el tipo */}
              <div className="w-full mb-8">
                {exercise.type === 'ORDER_ALGORITHM' ? (
                  <OrderAlgorithmGame />
                ) : (
                  <div className="w-full bg-gray-800 rounded-xl p-8 text-gray-300 flex items-center justify-center h-64 border-2 border-dashed border-gray-600">
                    <p>Componente {exercise.type} en construcción...</p>
                  </div>
                )}
              </div>
              
              {/* Botones temporales para simular acierto o fallo al maquetar */}
              <div className="flex gap-4">
                <button 
                  onClick={() => handleSubmit('ERROR')}
                  className="bg-red-100 hover:bg-red-200 text-red-600 font-bold py-3 px-6 rounded-xl transition-colors"
                >
                  Simular Fallo
                </button>
                <button 
                  onClick={() => handleSubmit('SUCCESS')}
                  className="bg-green-100 hover:bg-green-200 text-green-700 font-bold py-3 px-6 rounded-xl transition-colors"
                >
                  Simular Acierto
                </button>
              </div>
            </div>
          )}

          {/* FASE 3: VALIDANDO (Loading) */}
          {phase === 'VALIDATING' && (
            <div className="text-center flex flex-col items-center justify-center">
              <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-blue-600 mb-6"></div>
              <h3 className="text-2xl font-bold text-gray-800 mb-2">Validando solución...</h3>
              <p className="text-gray-500">Comprobando con el servidor</p>
            </div>
          )}

          {/* FASE 4: FEEDBACK DINÁMICO */}
          {phase === 'FEEDBACK' && (
            <div className="text-center max-w-lg mx-auto">
              {feedbackResult === 'SUCCESS' ? (
                <>
                  <div className="text-6xl mb-6">🎉</div>
                  <h3 className="text-3xl font-black text-green-600 mb-4">¡Respuesta Correcta!</h3>
                  <p className="text-gray-600 mb-8 text-lg">Has completado el ejercicio perfectamente. +10 XP</p>
                  <button 
                    onClick={onClose}
                    className="bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-8 rounded-full text-lg transition-transform transform hover:scale-105"
                  >
                    Continuar
                  </button>
                </>
              ) : (
                <>
                  <div className="text-6xl mb-6">💡</div>
                  <h3 className="text-3xl font-black text-red-600 mb-4">Hay un error</h3>
                  <div className="bg-red-50 border border-red-200 text-red-800 p-4 rounded-lg mb-8 text-left">
                    <strong>Feedback del servidor:</strong> 
                    {exercise.type === 'ORDER_ALGORITHM' 
                      ? " El orden lógico no es correcto. Recuerda que no puedes usar una variable antes de declararla." 
                      : " La línea seleccionada ejecuta la función, pero el error está en la condición del bucle while (línea 4)."}
                  </div>
                  <button 
                    onClick={handleRetry}
                    className="bg-gray-800 hover:bg-gray-900 text-white font-bold py-3 px-8 rounded-full text-lg transition-transform transform hover:scale-105"
                  >
                    Intentarlo de nuevo
                  </button>
                </>
              )}
            </div>
          )}

        </div>
      </div>
    </div>
  );
};

export default ExerciseShell;