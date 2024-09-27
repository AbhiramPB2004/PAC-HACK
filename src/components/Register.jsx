import React, { useState } from 'react';
import '../CSS/Register.css';
import axios from 'axios';

//port 1000


function RegisterPage() {
    const [username, setUsername] = useState('');
    const [mobileNumber, setMobileNumber] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        
        const userData = {
            username: username,
            mobile_number: mobileNumber,
            email: email,
            password: password
        };

        axios.post('http://localhost:1000/Register', userData,{
            withCredentials: true,  
          })
            .then(response => {
                console.log(response.data.error);
                if(response.data.error === 'User with this email already exists'){
                    alert('User already exists');
                }else{
                    if(response.data.error === "User registered successfully"){
                        alert('User created');
                        window.location ='/';
                    }else{
                        alert('User not created');
                    }
                    
                }
            })
            .catch(error => {
                console.error('There was an error registering:', error);
            });
    };

    return (
        <div className='RegisterBody'>
            <form onSubmit={handleSubmit} method="post">
                <h1 className='reg'>REGISTER</h1>
                
                <label className='reg' htmlFor="username">Username</label>
                <input 
                    type="text"  
                    id="username" 
                    name="username" 
                    value={username} 
                    onChange={(e) => setUsername(e.target.value)} 
                    required
                />

                <label className='reg' htmlFor="mobile_number">Mobile Number</label>
                <input 
                    type="text" 
                    id="mobile_number" 
                    name="mobile_number" 
                    value={mobileNumber} 
                    onChange={(e) => setMobileNumber(e.target.value)} 
                    required
                />

                <label className='reg' htmlFor="email">Email</label>
                <input 
                    type="email" 
                    id="email" 
                    name="email" 
                    value={email} 
                    onChange={(e) => setEmail(e.target.value)} 
                    required
                />

                <label className='reg'  htmlFor="password">Password</label>
                <input 
                    type="password"  
                    id="password" 
                    name="password" 
                    value={password} 
                    onChange={(e) => setPassword(e.target.value)} 
                    required
                />

                <button className='reg' type="submit">Register</button>
                <a className='Textreg' href="/">Back to Home</a>
            </form>
        </div>
    );
}

export default RegisterPage;
