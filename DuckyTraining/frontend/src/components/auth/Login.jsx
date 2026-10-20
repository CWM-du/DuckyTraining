import React, { useState } from 'react';
import { obtainTokens } from '../../services/authApi';

const Login = ({ onLoginSuccess }) => {
  const [credentials, setCredentials] = useState({ username: '', password: '' });
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e) => {
    setCredentials({
      ...credentials,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      await obtainTokens(credentials.username, credentials.password);
      onLoginSuccess();
    } catch (err) {
      setError(err.message || 'Error al conectar con el servidor. ¿Está Django encendido?');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center p-4">
      <div className="bg-gray-900 border border-gray-800 w-full max-w-md rounded-2xl shadow-2xl p-8">
        
        <div className="text-center mb-8">
          <div className="w-12 h-12 bg-blue-600 rounded-xl mx-auto mb-4 flex items-center justify-center shadow-lg shadow-blue-900/20">
            <span className="text-white font-bold text-xl">/&gt;</span>
          </div>
          <h2 className="text-2xl font-bold text-white mb-1">Iniciar Sesión</h2>
          <p className="text-gray-400 text-sm">Accede a tu panel de entrenamiento</p>
        </div>

        {error && (
          <div className="bg-red-900/30 border border-red-800 text-red-400 p-3 rounded-lg text-sm mb-6 text-center">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-gray-400 text-xs font-bold mb-2 uppercase tracking-wide">
              Usuario
            </label>
            <input
              type="text"
              name="username"
              value={credentials.username}
              onChange={handleChange}
              className="w-full bg-gray-800 text-white border border-gray-700 rounded-xl p-3 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors"
              placeholder="Ej: admin"
              required
            />
          </div>

          <div>
            <label className="block text-gray-400 text-xs font-bold mb-2 uppercase tracking-wide">
              Contraseña
            </label>
            <input
              type="password"
              name="password"
              value={credentials.password}
              onChange={handleChange}
              className="w-full bg-gray-800 text-white border border-gray-700 rounded-xl p-3 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors"
              placeholder="••••••••"
              required
            />
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded-xl transition-colors mt-4 shadow-md disabled:opacity-50 disabled:cursor-not-allowed flex justify-center items-center h-12"
          >
            {isLoading ? (
              <div className="animate-spin rounded-full h-5 w-5 border-t-2 border-b-2 border-white"></div>
            ) : (
              'Entrar'
            )}
          </button>
        </form>

      </div>
    </div>
  );
};

export default Login;