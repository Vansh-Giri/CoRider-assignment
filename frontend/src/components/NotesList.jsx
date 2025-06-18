import { useState, useEffect } from 'react';
import { notesAPI } from '../api/api';

const NotesList = ({ user }) => {
  const [notes, setNotes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (user) {
      fetchNotes();
    } else {
      setNotes([]);
    }
  }, [user]);

  const fetchNotes = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await notesAPI.getByUserId(user.id);
      setNotes(response.data);
    } catch (err) {
      setError('Failed to fetch notes');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteNote = async (noteId) => {
    if (!window.confirm('Are you sure you want to delete this note?')) return;

    try {
      await notesAPI.delete(user.id, noteId);
      setNotes(notes.filter(note => note.id !== noteId));
    } catch (err) {
      setError('Failed to delete note');
    }
  };

  if (!user) {
    return <div className="notes-list">Please select a user to view notes</div>;
  }

  if (loading) return <div>Loading notes...</div>;

  return (
    <div className="notes-list">
      <h3>Notes for {user.name}</h3>
      {error && <div className="error">{error}</div>}
      
      {notes.length === 0 ? (
        <p>No notes found. Create your first note!</p>
      ) : (
        <div className="notes-grid">
          {notes.map(note => (
            <div key={note.id} className="note-card">
              <h4>{note.title}</h4>
              <p>{note.content}</p>
              <div className="note-meta">
                <small>Created: {new Date(note.created_at).toLocaleDateString()}</small>
                {note.updated_at !== note.created_at && (
                  <small>Updated: {new Date(note.updated_at).toLocaleDateString()}</small>
                )}
              </div>
              <button 
                onClick={() => handleDeleteNote(note.id)}
                className="delete-btn"
              >
                Delete
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default NotesList;
