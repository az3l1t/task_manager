document.addEventListener("DOMContentLoaded", function () {
    const taskList = document.getElementById("task-list-items");
    const taskTitle = document.getElementById("task-title");
    const taskDescription = document.getElementById("task-description");
    const createTaskButton = document.getElementById("create-task");

    createTaskButton.addEventListener("click", function () {
        const title = taskTitle.value;
        const description = taskDescription.value;

        if (title.trim() === "") {
            alert("Task title cannot be empty.");
            return;
        }

        fetch("/tasks", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ title, description }),
        })
            .then((response) => response.json())
            .then(() => {
                taskTitle.value = "";
                taskDescription.value = "";
                loadTasks();
            });
    });

    function loadTasks() {
        fetch("/tasks")
            .then((response) => response.json())
            .then((tasks) => {
                taskList.innerHTML = "";
                tasks.forEach((task) => {
                    const li = document.createElement("li");
                    li.innerHTML = `
                        <strong>${task.title}</strong><br>
                        ${task.description}<br>
                        Status: ${task.status}
                        <button onclick="deleteTask(${task.id})">Delete</button>
                    `;
                    taskList.appendChild(li);
                });
            });
    }

    function deleteTask(taskId) {
        fetch(`/tasks/${taskId}`, {
            method: "DELETE",
        })
            .then((response) => response.json())
            .then(() => {
                loadTasks();
            });
    }

    loadTasks();
});