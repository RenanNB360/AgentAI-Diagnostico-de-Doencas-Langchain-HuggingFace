import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom'
import './Confirmation.css'

const Confirmation = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState('');
  const [error, setError] = useState('');
  
  useEffect(() => {

    const fetchUserData = async () => {
      try {
        const res = await fetch('http://127.0.0.1:8000/register/select')
        if (!res.ok) {
          throw new Error('Erro fetching user data')
        }
        const data = await res.json();
        setUser(data);
      } catch (err) {
        setError(err.message);
      }
    };

    fetchUserData();

  }, []);

  const gotToRegister = async () => {
    try {
      const res = await fetch('http://127.0.0.1:8000/register/delete', {
        method: 'DELETE',
      });
      if (!res.ok) {
        throw new Error('Error deleting record')
      }

      navigate('/register');
    } catch (err) {
      setError(err.message);
    }
    
  };

  const goToDeleteNotification = async () => {
    try {
      const res = await fetch('http://127.0.0.1:8000/register/delete', {
        method: 'DELETE',
      });
      if (!res.ok) {
        throw new Error('Error deleting record')
      }

      navigate('/register/confirmation/notification',
        {state:
          {message: 'The appointment schedule was cancelled, if you wish to reconsider, we are available to schedule a new appointment.'}
        }
      );
    } catch (err) {
      setError(err.message);
    }

  };

  const goToNotification = () => {
    navigate('/register/confirmation/notification',
      {state:
        {message: 'Appointment scheduling completed successfully. Now just show up on the scheduled date and time. If you have any questions, please contact our service channels.'}
      }
    );
  };

    return (
      <div className='container'>
        <div className='card'>
          <div className='return-text'>
            <p>Name: {user.name}</p>
            <p>Gender: {user.gender}</p>
            <p>Age: {user.age}</p>
            <p>Date: {user.date}</p>
            <p>Time: {user.time}</p>
          </div>
          <div className='action-user'>
            <button type='button' onClick={gotToRegister}>Modify</button>
            <button type='button' onClick={goToNotification}>Confirm</button>
            <button type='button' onClick={goToDeleteNotification}>Delete</button>
          </div>
        </div>
      </div>
    );
  };
  
  export default Confirmation;