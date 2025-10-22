 import React, { useState, useEffect } from 'react';
import './App.css'; 

const API_URL = 'http://127.0.0.1:5000/api';

function App() {

  const [tasks, setTasks] = useState([]);

  const [newTaskTitle, setNewTaskTitle] = useState('');
  
  const [editingTask, setEditingTask] = useState(null); 


  useEffect(() => {

    const fetchTasks = async () => {
      try {
        const response = await fetch(`${API_URL}/tasks`);
        const data = await response.json();
        setTasks(data.tasks); 
      } catch (error) {
        console.error("Error fetching tasks:", error);
      }
    };

    fetchTasks();
  }, []); 


  const handleAddTask = async (e) => {
    e.preventDefault();
    if (!newTaskTitle.trim()) return; 

    try {
      const response = await fetch(`${API_URL}/tasks`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: newTaskTitle }),
      });
      const data = await response.json();
      setTasks([...tasks, data.task]); 
      setNewTaskTitle(''); 
    } catch (error) {
      console.error("Error adding task:", error);
    }
  };


  const handleDeleteTask = async (taskId) => {
    try {
      await fetch(`${API_URL}/tasks/${taskId}`, { method: 'DELETE' });
      setTasks(tasks.filter(task => task.id !== taskId)); 
    } catch (error) {
      console.error("Error deleting task:", error);
    }
  };

  
  const handleUpdateTask = async (e) => {
    e.preventDefault();
    if (!editingTask || !editingTask.title.trim()) return;

    try {
      const response = await fetch(`${API_URL}/tasks/${editingTask.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: editingTask.title }),
      });
      const data = await response.json();
      
      setTasks(tasks.map(task => (task.id === editingTask.id ? data.task : task)));
      setEditingTask(null); 
    } catch (error) {
      console.error("Error updating task:", error);
    }
  };

  
  return (
    <div className="App">
      <header className="App-header">
        <h1>Task Manager</h1>

    
        <form onSubmit={handleAddTask} className="task-form">
          <input
            type="text"
            placeholder="Add a new task"
            value={newTaskTitle}
            onChange={(e) => setNewTaskTitle(e.target.value)}
          />
          <button type="submit">Add Task</button>
        </form>

    
        <ul className="task-list">
          {tasks.map((task) => (
            <li key={task.id}>
              {editingTask && editingTask.id === task.id ? (
    
                <form onSubmit={handleUpdateTask} className="edit-form">
                  <input
                    type="text"
                    value={editingTask.title}
                    onChange={(e) => setEditingTask({ ...editingTask, title: e.target.value })}
                  />
                  <button type="submit">Save</button>
                  <button type="button" onClick={() => setEditingTask(null)}>Cancel</button>
                </form>
              ) : (

                <div className="task-item">
                  <span>{task.title}</span>
                  <div>
                    <button onClick={() => setEditingTask({ ...task })}>Edit</button>
                    <button onClick={() => handleDeleteTask(task.id)}>Delete</button>
                  </div>
                </div>
              )}
            </li>
          ))}
        </ul>
      </header>
    </div>
  );
}

export default App;