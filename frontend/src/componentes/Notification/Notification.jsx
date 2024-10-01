import { useLocation, useNavigate } from 'react-router-dom';
import './Notification.css';
import { TbNurse } from "react-icons/tb";

const Notification = () => {
    const location = useLocation('');
    const message = location.state?.message || 'No message sent';
    const navigate = useNavigate();

    const goToChat = () => {
        navigate('/');
    };

    return (
        <div className='notification-container'>
            <div className='icon'>
                <TbNurse className='icon-inner' />
            </div>
            <div className='notification-message'>
                <p>{message}</p>
            </div>
            <div className='back-chat'>
                <button onClick={goToChat}>Return Chat</button>
            </div>
        </div>
    );
};

export default Notification;
