'use client'

import { useEffect, useRef, useState, FormEvent } from 'react'
import { Send, Bot, User } from 'lucide-react'
import { sendMessage } from '../../services/chatService'

type Message = {
  id: string
  role: 'user' | 'assistant'
  text: string
}

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const userId = 'user-001'

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    if (!input.trim()) return

    const newUserMessage: Message = {
      id: crypto.randomUUID(),
      role: 'user',
      text: input.trim(),
    }

    setMessages((prev) => [...prev, newUserMessage])
    setIsLoading(true)
    setInput('')

    try {
      const botReply = await sendMessage({ user_id: userId, message: newUserMessage.text })

      const newBotMessage: Message = {
        id: crypto.randomUUID(),
        role: 'assistant',
        text: botReply,
      }

      setMessages((prev) => [...prev, newBotMessage])
    } catch (err) {
      console.error('Error al enviar mensaje:', err)
    } finally {
      setIsLoading(false)
    }
  }

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center">
            <Bot className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-semibold text-gray-900">Projecto Final GenAI</h1>
            <p className="text-sm text-gray-500">Chatbot RAG</p>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-6 py-4 space-y-4">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center">
            <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mb-4">
              <Bot className="w-8 h-8 text-blue-500" />
            </div>
            <h2 className="text-xl font-semibold text-gray-900 mb-2">¡Hola! ¿En qué puedo ayudarte?</h2>
            <p className="text-gray-500 max-w-md">
              Escribe tu mensaje y comenzaremos una conversación. Estoy aquí para responder tus preguntas.
            </p>
            <div className="mt-8 pt-6 border-t border-gray-200">
              <p className="text-sm text-gray-400 mb-3">Desarrollado por:</p>
              <div className="flex flex-wrap justify-center gap-4">
                {[
                  { name: 'Juan Camilo Escobar Naranjo', initial: 'J', from: 'blue-500', to: 'purple-500' },
                  { name: 'Johan Quintero', initial: 'J', from: 'green-500', to: 'teal-500' },
                  { name: 'Alexander Chaverra Vasquez', initial: 'A', from: 'orange-500', to: 'red-500' },
                ].map(({ name, initial, from, to }) => (
                  <div
                    key={name}
                    className="flex items-center space-x-2 bg-white rounded-full px-4 py-2 shadow-sm border border-gray-100"
                  >
                    <div
                      className={`w-8 h-8 bg-gradient-to-r from-${from} to-${to} rounded-full flex items-center justify-center`}
                    >
                      <span className="text-white text-sm font-semibold">{initial}</span>
                    </div>
                    <span className="text-gray-700 font-medium">{name}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`flex items-start space-x-3 ${
                message.role === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              {message.role === 'assistant' && (
                <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center flex-shrink-0">
                  <Bot className="w-4 h-4 text-white" />
                </div>
              )}
              <div
                className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                  message.role === 'user'
                    ? 'bg-blue-500 text-white'
                    : 'bg-white text-gray-900 border border-gray-200'
                }`}
              >
                <div className="whitespace-pre-wrap">{message.text}</div>
              </div>
              {message.role === 'user' && (
                <div className="w-8 h-8 bg-gray-500 rounded-full flex items-center justify-center flex-shrink-0">
                  <User className="w-4 h-4 text-white" />
                </div>
              )}
            </div>
          ))
        )}

        {isLoading && (
          <div className="flex items-start space-x-3">
            <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center flex-shrink-0">
              <Bot className="w-4 h-4 text-white" />
            </div>
            <div className="bg-white text-gray-900 border border-gray-200 px-4 py-2 rounded-lg">
              <div className="flex space-x-1">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100" />
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200" />
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Form */}
      <div className="bg-white border-t border-gray-200 px-6 py-4">
        <form onSubmit={handleSubmit} className="flex space-x-3">
          <div className="flex-1">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Escribe tu mensaje aquí..."
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
              disabled={isLoading}
            />
          </div>
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 transition-colors"
          >
            <Send className="w-5 h-5" />
          </button>
        </form>
      </div>

      {/* Footer */}
      <div className="bg-white border-t border-gray-100 px-6 py-2">
        <div className="flex justify-center items-center space-x-1 text-xs text-gray-400">
          <span>Creado por Alexander, Johan y Juan</span>
        </div>
      </div>
    </div>
  )
}
