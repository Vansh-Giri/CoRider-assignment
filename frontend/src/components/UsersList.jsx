import { useState, useEffect } from 'react';
import { usersAPI, authAPI } from '../api/api';
import PasswordModal from './PasswordModal';
import LoginModal from './LoginModal';

const UsersList = ({ onUserLogin }) => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [deleteModal, setDeleteModal] = useState({ isOpen: false, user: null });
  const [loginModal, setLoginModal] = useState({ isOpen: false, user: null });

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await usersAPI.getAll();
      setUsers(response.data);
    } catch (err) {
      setError('Failed to fetch users');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteClick = (user) => {
    setDeleteModal({ isOpen: true, user });
  };

  const handleLoginClick = (user) => {
    setLoginModal({ isOpen: true, user });
  };

  const handleDeleteConfirm = async (password) => {
    try {
      // Verify password
      const verifyResponse = await authAPI.verifyPassword(deleteModal.user.id, password);
      if (!verifyResponse.data.valid) {
        throw new Error('Invalid password');
      }

      // Delete user
      await usersAPI.delete(deleteModal.user.id);
      
      // Refresh users list
      await fetchUsers();
      
      setDeleteModal({ isOpen: false, user: null });
    } catch (err) {
      throw err;
    }
  };

  const handleLoginConfirm = async (password) => {
    try {
      // Login with password
      const response = await authAPI.loginWithPassword(loginModal.user.id, password);
      
      // Call parent component's login handler
      onUserLogin(response.data.user);
      
      setLoginModal({ isOpen: false, user: null });
    } catch (err) {
      throw err;
    }
  };

  if (loading) return <div>Loading users...</div>;

  return (
    <div className="users-list-component">
      <h3>All Users</h3>
      {error && <div className="error">{error}</div>}
      
      <div className="users-grid">
        {users.length === 0 ? (
          <p>No users found.</p>
        ) : (
          users.map(user => (
            <div key={user.id} className="user-card">
              <div className="user-info">
                <h4>{user.name}</h4>
                <p>{user.email}</p>
                <small>Joined: {new Date(user.created_at).toLocaleDateString()}</small>
              </div>
              <div className="user-actions">
                <button 
                  onClick={() => handleLoginClick(user)}
                  className="login-btn small"
                  title="Login as this user"
                >
                  Login
                </button>
                <button 
                  onClick={() => handleDeleteClick(user)}
                  className="delete-btn small"
                  title="Delete user"
                >
                  X
                </button>
              </div>
            </div>
          ))
        )}
      </div>
      
      <button onClick={fetchUsers} className="refresh-btn">
        Refresh Users
      </button>

      <PasswordModal
        isOpen={deleteModal.isOpen}
        onClose={() => setDeleteModal({ isOpen: false, user: null })}
        onConfirm={handleDeleteConfirm}
        userName={deleteModal.user?.name}
        title="Delete User"
        message="Enter the user's password to confirm deletion:"
      />

      <LoginModal
        isOpen={loginModal.isOpen}
        onClose={() => setLoginModal({ isOpen: false, user: null })}
        onConfirm={handleLoginConfirm}
        userName={loginModal.user?.name}
      />
    </div>
  );
};

export default UsersList;
