import React, { useEffect, useState } from 'react'

const OrderAlgorithmGame = ({ content, onAnswerChange }) => {
  const [steps, setSteps] = useState(() => content.steps)

  useEffect(() => {
    setSteps(content.steps)
  }, [content])

  useEffect(() => {
    onAnswerChange({ ordered_ids: steps.map((step) => step.id) })
  }, [steps, onAnswerChange])

  const moveStep = (index, direction) => {
    const nextIndex = index + direction
    if (nextIndex < 0 || nextIndex >= steps.length) return
    const updated = [...steps]
    ;[updated[index], updated[nextIndex]] = [updated[nextIndex], updated[index]]
    setSteps(updated)
  }

  return (
    <div className="w-full max-w-2xl mx-auto bg-gray-900 p-6 rounded-2xl">
      <h3 className="text-white font-bold text-lg mb-5">Ordena los pasos</h3>
      <ol className="space-y-3">
        {steps.map((step, index) => (
          <li key={step.id} className="flex items-center gap-4 bg-gray-800 border border-gray-600 p-3 rounded-xl">
            <span className="flex-1 font-mono text-blue-200">{step.text}</span>
            <div className="flex flex-col">
              <button onClick={() => moveStep(index, -1)} disabled={index === 0} aria-label="Subir paso" className="text-white disabled:opacity-30">▲</button>
              <button onClick={() => moveStep(index, 1)} disabled={index === steps.length - 1} aria-label="Bajar paso" className="text-white disabled:opacity-30">▼</button>
            </div>
          </li>
        ))}
      </ol>
    </div>
  )
}

export default OrderAlgorithmGame
