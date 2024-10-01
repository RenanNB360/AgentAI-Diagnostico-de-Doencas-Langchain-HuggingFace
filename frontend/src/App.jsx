import { useState } from 'react'
import './App.css'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Chat from './componentes/Chat/Chat';
import Register from './componentes/Register/Register';
import Confirmation from './componentes/Confirmation/Confirmation';
import Notification from './componentes/Notification/Notification'

function App() {
  const [loggedIn, setLogin] = useState(false)

  return (
    <div className='App'>
      <Router>
        <Routes>
          <Route path="/" element={<Chat />} />
          <Route path="/register" element={<Register />} />
          <Route path="/register/confirmation" element={<Confirmation />} />
          <Route path="/register/confirmation/notification" element={<Notification />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App