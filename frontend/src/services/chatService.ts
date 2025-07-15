import axios from 'axios'

export const sendMessage = async ({
  user_id,
  message,
}: {
  user_id: string
  message: string
}): Promise<string> => {
  const response = await axios.post('http://localhost:8000/api/chat', {
    user_id,
    message,
  })

  return response.data.message
}
