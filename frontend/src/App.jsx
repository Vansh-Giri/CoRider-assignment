import { useState, useEffect } from 'react';
import { authAPI, usersAPI } from './api/api';
import UserForm from './components/UserForm';
import UsersList from './components/UsersList';
import NotesList from './components/NotesList';
import AddNoteForm from './components/AddNoteForm';
import PasswordModal from './components/PasswordModal';
import EditProfileModal from './components/EditProfileModal';
import './App.css';

function App() {
  const [currentUser, setCurrentUser] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);
  const [loading, setLoading] = useState(true);
  const [deleteModal, setDeleteModal] = useState({ isOpen: false });
  const [editProfileModal, setEditProfileModal] = useState({ isOpen: false });

  useEffect(() => {
    checkCurrentUser();
  }, []);

  const checkCurrentUser = async () => {
    try {
      const response = await authAPI.getCurrentUser();
      setCurrentUser(response.data);
    } catch (err) {
      setCurrentUser(null);
    } finally {
      setLoading(false);
    }
  };

  const handleUserLogin = (user) => {
    setCurrentUser(user);
  };

  const handleLogout = async () => {
    try {
      await authAPI.logout();
      setCurrentUser(null);
    } catch (err) {
      console.error('Logout error:', err);
    }
  };

  const handleDeleteAccount = () => {
    setDeleteModal({ isOpen: true });
  };

  const handleEditProfile = () => {
    setEditProfileModal({ isOpen: true });
  };

  const handleDeleteConfirm = async (password) => {
    try {
      const verifyResponse = await authAPI.verifyPassword(currentUser.id, password);
      if (!verifyResponse.data.valid) {
        throw new Error('Invalid password');
      }

      await usersAPI.delete(currentUser.id);
      setCurrentUser(null);
      setDeleteModal({ isOpen: false });
    } catch (err) {
      throw err;
    }
  };

  const handleProfileUpdated = (updatedUser) => {
    setCurrentUser(updatedUser);
    setEditProfileModal({ isOpen: false });
  };

  const handleUserCreated = (newUser, autoLogin = false) => {
    if (autoLogin) {
      setCurrentUser(newUser);
    } else {
      setRefreshKey(prev => prev + 1);
    }
  };

  const handleNoteAdded = (newNote) => {
    setRefreshKey(prev => prev + 1);
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  if (!currentUser) {
    return (
      <div className="App">
        <header className="App-header">
          <h1>Notes App</h1>
          <p>Create an account or login to continue</p>
        </header>
        <main className="App-main login-main">
          <div className="section">
            <UserForm onUserCreated={handleUserCreated} />
          </div>
          <div className="section users-list-section">
            <UsersList 
              key={refreshKey} 
              onUserLogin={handleUserLogin}
            />
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>Notes App</h1>
        <div className="user-info">
          <span>Welcome, {currentUser.name}!</span>
          <div className="header-buttons">
            <button onClick={handleEditProfile} className="edit-profile-btn">
              Edit Profile
            </button>
            <button onClick={handleDeleteAccount} className="delete-account-btn">
              Delete Account
            </button>
            <button onClick={handleLogout} className="logout-btn">
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="App-main notes-main">
        <div className="section">
          <AddNoteForm 
            user={currentUser} 
            onNoteAdded={handleNoteAdded} 
          />
        </div>

        <div className="section notes-section">
          <NotesList 
            key={`${currentUser.id}-${refreshKey}`} 
            user={currentUser} 
          />
        </div>
      </main>

      <PasswordModal
        isOpen={deleteModal.isOpen}
        onClose={() => setDeleteModal({ isOpen: false })}
        onConfirm={handleDeleteConfirm}
        userName={currentUser?.name}
        title="Delete Your Account"
        message="This will permanently delete your account and all your notes. This action cannot be undone."
      />

      <EditProfileModal
        isOpen={editProfileModal.isOpen}
        onClose={() => setEditProfileModal({ isOpen: false })}
        user={currentUser}
        onProfileUpdated={handleProfileUpdated}
      />
    </div>
  );
}

export default App;
