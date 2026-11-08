import React, { useState } from 'react';
import OrderAlgorithmGame from './OrderAlgorithmGame'; 
import FindErrorGame from './FindErrorGame';
import MatchConceptsGame from './MatchConceptsGame';
import axios from 'axios';

const ExerciseShell = ({ exercise, onClose }) => {
  // Fases: 'INSTRUCTIONS' -> 'PLAYING' -> 'VALIDATING' -> 'FEEDBACK'
  const [phase, setPhase] = useState('INSTRUCTIONS');
  
  // Resultado simulado para la fase de feedback: 'SUCCESS' o 'ERROR'
  const [feedbackResult, setFeedbackResult] = useState(null);

  // --- NUEVO: ESTADO PARA LA RESPUESTA REAL DEL USUARIO ---
  const [userAnswer, setUserAnswer] = useState(null);

  const handleStart = () => setPhase('PLAYING');
  
  const handleSubmit = async () => {
    // Si el usuario no ha seleccionado nada aún, podemos avisarle (opcional)
    if (!userAnswer) {
      alert("Por favor, selecciona una respuesta antes de comprobar.");
      return;
    }

    setPhase('VALIDATING');
    
    try {
      const token = localStorage.getItem('access');
      const exerciseNumber = exercise.number || exercise.id;
      
      // Enviamos exactamente lo que el usuario ha seleccionado en el minijuego
      const payload = {
        answer: userAnswer 
      };

      console.log("Enviando a Django:", payload);

      const response = await axios.post(
        `http://localhost:8000/api/training/exercises/${exerciseNumber}/submit/`, 
        payload, 
        { headers: { Authorization: `Bearer ${token}` } }
      );

      console.log("Django responde:", response.data);

      const isSuccess = response.data.correct === true;
      
      setFeedbackResult(isSuccess ? 'SUCCESS' : 'ERROR');
      window.lastServerFeedback = response.data.explanation || "Respuesta incorrecta.";
      setPhase('FEEDBACK');

    } catch (err) {
      console.error("Error en el Submit:", err.response?.data || err.message);
      setFeedbackResult('ERROR');
      setPhase('FEEDBACK');
    }
  };

  const handleRetry = () => {
    setPhase('PLAYING');
    setUserAnswer(null); // Limpiamos la respuesta al reintentar
  };

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
              {exercise.type === 'CONNECT_NETWORK' && (
                <p className="text-gray-600 mb-8 text-lg">
                  Conecta los nodos de red según la topología correcta.
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
                
                {/* 
                  NUEVO: Pasamos la función 'onChange={setUserAnswer}' a los juegos.
                  También deberías pasarles 'data={exercise.content}' para que 
                  sepan qué código/datos pintar.
                */}
                {exercise.type === 'ORDER_ALGORITHM' && (
                  <OrderAlgorithmGame data={exercise.content} onChange={setUserAnswer} />
                )}
                
                {exercise.type === 'FIND_ERROR' && (
                  <FindErrorGame data={exercise.content} onChange={setUserAnswer} />
                )}
                
                {exercise.type === 'CONNECT_NETWORK' && (
                  <MatchConceptsGame data={exercise.content} onChange={setUserAnswer} />
                )}

                {exercise.type !== 'ORDER_ALGORITHM' &&
                  exercise.type !== 'FIND_ERROR' &&
                  exercise.type !== 'CONNECT_NETWORK' && (
                    <div className="w-full bg-gray-800 rounded-xl p-8 text-gray-300 flex items-center justify-center h-64 border-2 border-dashed border-gray-600">
                      <p>Componente {exercise.type} en construcción...</p>
                    </div>
                  )}
              </div>

              {/* Botón de envío unificado (UX) */}
              <div className="mt-4 w-full max-w-2xl mx-auto flex justify-end border-t border-gray-100 pt-6">
                <button
                  onClick={handleSubmit}
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
                    <p className="mt-2">{window.lastServerFeedback}</p>
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