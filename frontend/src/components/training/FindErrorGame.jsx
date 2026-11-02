import React, { useState } from 'react'

const FindErrorGame = ({ content, onAnswerChange }) => {
  const [selectedBugId, setSelectedBugId] = useState(null)

  const selectBug = (id) => {
    setSelectedBugId(id)
    onAnswerChange({ selected_bug_id: id })
  }

  return (
    <div className="w-full max-w-2xl mx-auto bg-gray-900 p-6 rounded-2xl">
      <h3 className="text-white font-bold text-lg mb-5">Encuentra el fallo</h3>
      <ol className="bg-gray-950 rounded-xl border border-gray-700 overflow-hidden font-mono text-sm py-4">
        {content.code_items.map((item, index) => (
          <li key={item.id}>
            <button
              onClick={() => selectBug(item.id)}
              aria-pressed={selectedBugId === item.id}
              className={`w-full text-left flex gap-4 px-4 py-2 ${
                selectedBugId === item.id
                  ? 'bg-blue-900/50 text-blue-100'
                  : 'text-gray-300 hover:bg-gray-800'
              }`}
            >
              <span className="w-8 text-right text-gray-500 select-none">{index + 1}</span>
              <span className="whitespace-pre">{item.text || ' '}</span>
            </button>
          </li>
        ))}
      </ol>
    </div>
  )
}

export default FindErrorGame
