import React, { useState } from 'react';
import '../CSS/ProfilePage.css';

const ProfilePage = () => {
  const [activeSection, setActiveSection] = useState('profile');

  const user = {
    username: 'Mr Bean',
    email: 'Beanmr@example.com',
    phoneNumber: '+1 234 567 890',
    profilePic: 'https://i.pinimg.com/564x/0e/2e/9d/0e2e9dc33751fbf4a708c1ecbdaf2d43.jpg', // Placeholder image, replace with an actual URL
  };

  const renderContent = () => {
    switch (activeSection) {
      case 'profile':
        return (
          <div className="content-box profile-centered">
            <img src={user.profilePic} alt="Profile Pic" className="avatar" />
            <h1>{user.username}</h1>
            <p>Email: {user.email}</p>
            <p>Phone: {user.phoneNumber}</p>
            <button className="cta-btn">Update Profile</button>
          </div>
        );
      case 'orderHistory':
        return (
          <div className="content-box">
            <h3>Order History</h3>
            <ul>
              <li>Order #12345 - 2 Apples, 1 Mango - Delivered</li>
              <li>Order #12346 - 1 Watermelon - Pending</li>
            </ul>
            <button className="cta-btn">View Details</button>
          </div>
        );
      case 'wishlist':
        return (
          <div className="content-box">
            <h3>Wishlist</h3>
            <ul>
              <li>Bananas</li>
              <li>Avocados</li>
            </ul>
            <button className="cta-btn">Add More Items</button>
          </div>
        );
      case 'settings':
        return (
          <div className="content-box">
            <h3>Settings</h3>
            <p>Language: English</p>
            <p>Currency: USD</p>
            <button className="cta-btn">Save Changes</button>
          </div>
        );
      case 'privacy':
        return (
          <div className="content-box">
            <h3>Privacy & Security</h3>
            <p>Change your password or set up two-factor authentication.</p>
            <button className="cta-btn">Update Security Settings</button>
          </div>
        );
      default:
        return <p>Select an option from the sidebar</p>;
    }
  };

  return (
    <div className="profile-page">
      <header className="header">
        <h1>Profile Dashboard</h1>
      </header>
      <div className="main-content">
        <div className="sidebar">
          <button
            className={activeSection === 'profile' ? 'active' : ''}
            onClick={() => setActiveSection('profile')}
          >
            Profile
          </button>
          <button
            className={activeSection === 'orderHistory' ? 'active' : ''}
            onClick={() => setActiveSection('orderHistory')}
          >
            Order History
          </button>
          <button
            className={activeSection === 'wishlist' ? 'active' : ''}
            onClick={() => setActiveSection('wishlist')}
          >
            Wishlist
          </button>
          <button
            className={activeSection === 'settings' ? 'active' : ''}
            onClick={() => setActiveSection('settings')}
          >
            Settings
          </button>
          <button
            className={activeSection === 'privacy' ? 'active' : ''}
            onClick={() => setActiveSection('privacy')}
          >
            Privacy & Security
          </button>
        </div>
        <div className="content-area">
          {renderContent()}
        </div>
      </div>
      <footer className="footer">
        <p>&copy; 2024 My E-Commerce Site</p>
      </footer>
    </div>
  );
};

export default ProfilePage;