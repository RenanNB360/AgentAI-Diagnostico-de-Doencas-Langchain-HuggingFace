import { useState } from 'react'
import { useNavigate } from 'react-router-dom';
import './Register.css'



const Register = () => {
    const [name, setName] = useState('')
    const [gender, setGender] = useState('')
    const [age, setAge] = useState('')
    const [date, setDate] = useState('')
    const [time, setTime] = useState('')
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
      e.preventDefault();

      const res = await fetch('http://127.0.0.1:8000/register/create', {
        method:'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name,
          gender,
          age,
          date,
          time
        })
      });

      const data = await res.json();
      console.log(data);

      if (res.ok) {
        navigate('/register/confirmation');
      } else {
        console.log('Erro ao registrar');
      }
    }





    return (
      <div className='container'>
        <form onSubmit={handleSubmit}>
          <h1>Patient Registration</h1>

          <div className="form-group">
            <label htmlFor="name">Name:</label>
            <input 
              id="name" 
              name="name" 
              type="text"
              onChange={(e) => setName(e.target.value)}
            />
          </div>

          <div className="form-group">
            <label htmlFor="gender">Gender:</label>
            <input 
              id="gender"
              name="gender"
              type="text"
              onChange={(e) => setGender(e.target.value)}
            />
          </div>

          <div className="form-group">
            <label htmlFor="age">Age:</label>
            <input 
              id="age"
              name="age"
              type="number"
              onChange={(e) => setAge(e.target.value)}
            />
          </div>

          <div className="form-group">
            <label htmlFor="date">Date:</label>
            <input 
              id="date"
              name="date"
              type="date"
              onChange={(e) => setDate(e.target.value)}
            />
          </div>

          <div className="form-group">
            <label htmlFor="time">Time:</label>
            <input 
              id="time"
              name="time"
              type="time"
              onChange={(e) => setTime(e.target.value)}
            />
          </div>

          <div className='create-user'>
            <button type='submit' >Register</button>
          </div>
        </form>
      </div>
    );
  };
  
  export default Register;