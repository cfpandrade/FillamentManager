// Función para obtener los datos de los filamentos
async function fetchData() {
    try {
        const response = await fetch('/filamentos');
        const data = await response.json();
        const output = document.getElementById('output');
        output.innerHTML = ''; // Limpiar contenido anterior
        data.forEach(filamento => {
            const card = document.createElement('div');
            card.className = 'filament-card';
            card.innerHTML = `
                <h2>${filamento.nombre}</h2>
                <p><strong>Marca:</strong> ${filamento.marca}</p>
                <p><strong>Color:</strong> ${filamento.color}</p>
                <p><strong>Tipo:</strong> ${filamento.tipo}</p>
                <p><strong>Peso Restante:</strong> ${filamento.peso_restante}g / ${filamento.peso_total}g</p>
                <p><strong>Cantidad:</strong> ${filamento.cantidad}</p>
                <p><small>Última Actualización: ${new Date(filamento.ultima_actualizacion).toLocaleString()}</small></p>
                <button onclick="editFilament(${filamento.id})">✏️ Edit</button>
                <button onclick="deleteFilament(${filamento.id})">🗑️ Delete</button>
            `;
            output.appendChild(card);
        });
    } catch (error) {
        document.getElementById('output').innerText = 'Error fetching data: ' + error;
    }
}

// Función para mostrar el formulario de agregar/editar
function showAddForm() {
    document.getElementById('form-title').innerText = "Add Filament";
    document.getElementById('filament-form').reset();
    document.getElementById('form-section').style.display = "block";
}

// Función para manejar el envío del formulario
async function handleSubmit(event) {
    event.preventDefault();
    const id = document.getElementById('id').value;
    const nombre = document.getElementById('nombre').value;
    const marca = document.getElementById('marca').value;
    const color = document.getElementById('color').value;
    const tipo = document.getElementById('tipo').value;
    const peso_total = parseInt(document.getElementById('peso_total').value);
    const cantidad = parseInt(document.getElementById('cantidad').value);
    const peso_restante = peso_total;

    const method = id ? 'PUT' : 'POST';
    const url = id ? `/filamentos/${id}` : '/filamentos';

    const body = JSON.stringify({ nombre, marca, color, tipo, peso_total, peso_restante, cantidad });

    try {
        const response = await fetch(url, {
            method,
            headers: { 'Content-Type': 'application/json' },
            body
        });

        if (response.ok) {
            fetchData();
            document.getElementById('form-section').style.display = "none";
        } else {
            const errorData = await response.json();
            alert(`Error: ${errorData.error || 'Error desconocido'}`);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

// Función para eliminar un filamento
async function deleteFilament(id) {
    if (confirm("Are you sure you want to delete this filament?")) {
        try {
            const response = await fetch(`/filamentos/${id}`, { method: 'DELETE' });
            if (response.ok) {
                fetchData();
                alert(`Filament with ID ${id} deleted.`);
            } else {
                alert('Error deleting filament');
            }
        } catch (error) {
            alert('Error: ' + error.message);
        }
    }
}

// Función para cargar un filamento en el formulario de edición
async function editFilament(id) {
    try {
        const response = await fetch(`/filamentos/${id}`);
        if (!response.ok) throw new Error('Failed to fetch filament');
        const filamento = await response.json();
        document.getElementById('form-title').innerText = "Edit Filament";
        document.getElementById('id').value = filamento.id;
        document.getElementById('nombre').value = filamento.nombre;
        document.getElementById('marca').value = filamento.marca;
        document.getElementById('color').value = filamento.color;
        document.getElementById('tipo').value = filamento.tipo;
        document.getElementById('peso_total').value = filamento.peso_total;
        document.getElementById('cantidad').value = filamento.cantidad;
        document.getElementById('form-section').style.display = "block";
    } catch (error) {
        alert('Error fetching filament: ' + error.message);
    }
}
