import { useState, useEffect, useRef } from "react"

function App() {

  const [todos, setTodos] = useState([])

  const inputRef = useRef()

  const todoHandler = (e) => {
    e.preventDefault()
    setTodos([...todos, inputRef.current.value])
    inputRef.current.value = ''
  }

  useEffect(() => {
    console.log(todos)
  }, [todos])

  return (
    <div>
      <form onSubmit={todoHandler}>
        <input ref={inputRef} type="text" placeholder="Enter Todo" />
        <button type="submit">Add</button>
      </form>

      {todos.map((todo, index) => (
        <p key={index}>{todo}</p>
      ))}

    </div>
  )
}

export default App
