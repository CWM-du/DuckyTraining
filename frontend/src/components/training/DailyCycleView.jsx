import React from 'react';

// Recibimos 'data' como prop desde App.jsx
const DailyCycleView = ({ data }) => {
  
  // Desestructuramos los datos REALES que vienen del backend
  const { access_level, daily_limit, cycle_date, completed_count, exercises } = data;
  
  // Mocks visuales temporales (hasta que el backend los envíe)
  const streak = 4; 
  const ducky_coins = 150; 

  const renderExerciseState = (state) => {
    switch (state) {
      case 'COMPLETED_TODAY':
        return (
          <div className="flex items-center text-green-500 font-bold">
            <span className="text-2xl mr-2">✅</span> Completado
          </div>
        );
      case 'AVAILABLE':
        return (
          <button className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-full transition-transform transform hover:scale-105">
            ¡Jugar! ▶️
          </button>
        );
      case 'BLOCKED_BY_SEQUENCE':
        return (
          <div className="flex items-center text-gray-400 font-semibold">
            <span className="text-xl mr-2">🔒</span> Bloqueado
          </div>
        );
      case 'NOT_ACCESSIBLE_BY_LEVEL':
        return (
          <div className="flex flex-col items-end text-gray-500 text-sm">
            <span>🔒 Nivel Insuficiente</span>
            <span className="bg-yellow-200 text-yellow-800 px-2 py-1 rounded mt-1 text-xs font-bold">
              Requiere PLUS / PRO
            </span>
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6 bg-gray-50 min-h-screen">
      
      {/* CABECERA DE PROGRESO */}
      <div className="bg-white rounded-2xl shadow-sm p-6 mb-8 flex justify-between items-center border border-gray-100">
        <div>
          <h1 className="text-3xl font-extrabold text-gray-800">DuckyTraining</h1>
          <p className="text-gray-500 mt-1">Práctica individual - Fecha: {cycle_date}</p>
        </div>
        <div className="flex gap-6 text-center">
          <div className="bg-orange-100 px-4 py-2 rounded-lg">
            <p className="text-xs text-orange-600 font-bold uppercase">Racha</p>
            <p className="text-2xl font-black text-orange-500">🔥 {streak}</p>
          </div>
          <div className="bg-yellow-100 px-4 py-2 rounded-lg">
            <p className="text-xs text-yellow-600 font-bold uppercase">DuckyCoins</p>
            <p className="text-2xl font-black text-yellow-500">🪙 {ducky_coins}</p>
          </div>
          <div className="bg-purple-100 px-4 py-2 rounded-lg">
            <p className="text-xs text-purple-600 font-bold uppercase">Plan</p>
            <p className="text-2xl font-black text-purple-500">👑 {access_level}</p>
            <p className="text-xs text-purple-400">{daily_limit} retos diarios</p>
          </div>
        </div>
      </div>

      {/* LISTA DE EJERCICIOS */}
      <div className="space-y-4">
        {exercises.map((exercise) => {
          const isAccessible = exercise.state !== 'NOT_ACCESSIBLE_BY_LEVEL';
          const isCompleted = exercise.state === 'COMPLETED_TODAY';
          
          return (
            <div 
              key={exercise.number} 
              className={`flex items-center justify-between p-6 rounded-2xl border-2 transition-all ${
                isCompleted ? 'bg-green-50 border-green-200' :
                isAccessible ? 'bg-white border-transparent shadow-sm hover:shadow-md' : 
                'bg-gray-100 border-gray-200 opacity-70'
              }`}
            >
              <div className="flex items-center gap-4">
                <div className={`w-12 h-12 flex items-center justify-center rounded-full font-black text-lg ${
                  isCompleted ? 'bg-green-200 text-green-700' : 'bg-blue-100 text-blue-600'
                }`}>
                  {exercise.number}
                </div>
                <div>
                  <h3 className="text-xl font-bold text-gray-800">{exercise.name}</h3>
                  <div className="flex gap-2 mt-1 text-sm font-medium">
                    <span className="text-blue-500">{exercise.type ? exercise.type.replace('_', ' ') : 'Formato por confirmar'}</span>
                    <span className="text-gray-300">•</span>
                    <span className={`${exercise.difficulty === 'HARD' ? 'text-red-500' : exercise.difficulty === 'MEDIUM' ? 'text-yellow-500' : 'text-green-500'}`}>
                      {exercise.difficulty}
                    </span>
                  </div>
                  <p className="text-xs text-gray-400 mt-1">Habilidad: {exercise.skill}</p>
                </div>
              </div>

              <div>
                {renderExerciseState(exercise.state)}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default DailyCycleView;