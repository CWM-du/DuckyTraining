import React, { useState } from 'react';
import OrderAlgorithmGame from './OrderAlgorithmGame'; // Asegúrate de que este archivo está en la misma carpeta
import FindErrorGame from './FindErrorGame';
import MatchConceptsGame from './MatchConceptsGame';


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
            <div className="text-center max-w-lg mx-auto" >
              <h3 className="text-2xl font-bold text-gray-800 mb-4">Objetivo</h3>

              {exercise.type === 'ORDER_ALGORITHM' && (
                <p className="text-gray-600 mb-8 text-lg">
                  Lee los bloques de código desordenados y colócalos en la secuencia lógica correcta para que el algoritmo funcione.
                </p>
              )}
              {exercise.type === 'FIND_ERROR' && (
                <p className="text-gray-600 mb-8 text-lg">
                  Analiza el código y encuentra la línea exacta donde se está produciendo el error de seguridad o lógico.
                </p>
              )}
              {exercise.type === 'MATCH_CONCEPTS' && (
                <p className="text-gray-600 mb-8 text-lg">
                  Selecciona un concepto de la izquierda y conéctalo con su definición correcta a la derecha.
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
              <div className="w-full mb-8">
                {exercise.type === 'ORDER_ALGORITHM' && <OrderAlgorithmGame />}
                {exercise.type === 'FIND_ERROR' && <FindErrorGame />}
                {exercise.type === 'MATCH_CONCEPTS' && <MatchConceptsGame />}

                {exercise.type !== 'ORDER_ALGORITHM' &&
                  exercise.type !== 'FIND_ERROR' &&
                  exercise.type !== 'MATCH_CONCEPTS' && (
                    <div className="w-full bg-gray-800 rounded-xl p-8 text-gray-300 flex items-center justify-center h-64 border-2 border-dashed border-gray-600">
                      <p>Componente {exercise.type} en construcción...</p>
                    </div>
                  )}
              </div>

              {/* Botón de envío unificado (UX) */}
              <div className="mt-4 w-full max-w-2xl mx-auto flex justify-end border-t border-gray-100 pt-6">
                <button
                  onClick={() => {
                    const randomResult = Math.random() > 0.5 ? 'SUCCESS' : 'ERROR';
                    handleSubmit(randomResult);
                  }}
                  className="bg-gray-800 hover:bg-black text-white font-bold py-3 px-10 rounded-xl transition-all shadow-md hover:shadow-lg flex items-center gap-2"
                >
                  Comprobar respuesta
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
                  <h3 className="text-3xl font-black text-red-600 mb-4">Hay un error</h3>
                  <div className="bg-red-50 border border-red-200 text-red-800 p-4 rounded-lg mb-8 text-left">
                    <strong>Feedback del servidor:</strong>
                    {exercise.type === 'ORDER_ALGORITHM'
                      ? ' El orden lógico no es correcto. Recuerda que no puedes usar una variable antes de declararla.'
                      : ' La línea seleccionada ejecuta la función, pero el error está en la condición del bucle while (línea 4).'}
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