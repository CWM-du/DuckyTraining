import React, { useState } from 'react'

const ConnectNetworkGame = ({ content, onAnswerChange }) => {
  const [selectedNode, setSelectedNode] = useState(null)
  const [connections, setConnections] = useState([])

  const selectNode = (nodeId) => {
    if (!selectedNode) {
      setSelectedNode(nodeId)
      return
    }
    if (selectedNode === nodeId) {
      setSelectedNode(null)
      return
    }

    const pair = [selectedNode, nodeId].sort()
    const exists = connections.some(
      (connection) => connection[0] === pair[0] && connection[1] === pair[1],
    )
    const updated = exists
      ? connections.filter(
          (connection) => connection[0] !== pair[0] || connection[1] !== pair[1],
        )
      : [...connections, pair]
    setConnections(updated)
    onAnswerChange({ connections: updated })
    setSelectedNode(null)
  }

  return (
    <div className="w-full max-w-2xl mx-auto bg-gray-900 p-6 rounded-2xl">
      <h3 className="text-white font-bold text-lg mb-5">Conecta los nodos</h3>
      <div className="grid grid-cols-2 gap-3">
        {content.nodes.map((node) => (
          <button
            key={node.id}
            onClick={() => selectNode(node.id)}
            aria-pressed={selectedNode === node.id}
            className={`rounded-xl border-2 p-4 text-left ${
              selectedNode === node.id
                ? 'border-blue-400 bg-blue-900 text-white'
                : 'border-gray-600 bg-gray-800 text-gray-200'
            }`}
          >
            {node.label}
          </button>
        ))}
      </div>
      <p className="text-gray-400 text-sm mt-4">
        Selecciona dos nodos para alternar una conexión. Conexiones: {connections.length}
      </p>
    </div>
  )
}

export default ConnectNetworkGame
