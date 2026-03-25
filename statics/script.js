const form = document.getElementById("taskForm");
const input = document.getElementById("taskInput");
const list = document.getElementById("taskList");

// Load tasks on page load
window.onload = async () => {
    const res = await fetch("/tasks");
    const tasks = await res.json();

    tasks.forEach(addTaskToDOM);
};

// Add task
form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const res = await fetch("/add", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ task: input.value })
    });

    const task = await res.json();
    addTaskToDOM(task);
    input.value = "";
});

// Add task to UI
function addTaskToDOM(task) {
    const li = document.createElement("li");
    li.dataset.id = task.id;

    if (task.done) li.classList.add("done");

    li.innerHTML = `
        <span>${task.text}</span>
        <button>X</button>
    `;

    // Toggle
    li.querySelector("span").onclick = async () => {
        const res = await fetch(`/toggle/${task.id}`, {
            method: "PUT"
        });
        const updated = await res.json();
        li.classList.toggle("done", updated.done);
    };

    // Delete
    li.querySelector("button").onclick = async () => {
        await fetch(`/delete/${task.id}`, {
            method: "DELETE"
        });
        li.remove();
    };

    list.appendChild(li);
}