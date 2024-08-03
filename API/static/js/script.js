document.addEventListener("DOMContentLoaded", function() { // Una vez que el documento esté cargado se ejecuta la función
    const board = document.getElementById("board"); // Se obtiene el elemento con el id "board"
    const cells = document.getElementsByClassName("cell"); // Se obtienen los elementos con la clase "cell"

    for (let cell of cells) { // Se recorren los elementos con la clase "cell"
        cell.addEventListener("click", function(event) { // Cada vez que se haga clic en una celda, se ejecutará la función pasada como parámetro.
            
            // Se obtiene la posición del clic en la celda
            const rect = board.getBoundingClientRect(); 
            const x = event.clientX - rect.left;
            const y = event.clientY - rect.top;
            
            // Se envía la posición del clic al servidor
            console.log("Enviando clic al servidor con coordenadas:", { x: Math.floor(x), y: Math.floor(y) });

            fetch("/click/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ x: Math.floor(x), y: Math.floor(y) })
            })
            .then(response => response.json()) // Se convierte la respuesta a JSON
            .then(data => { // Se obtiene la respuesta
                if (data.status) { // Si la respuesta tiene un status
                    alert(data.status); // Se muestra una alerta con el status
                }
                updateBoard(); // Se actualiza el tablero
            });
        });
    }

    // Se añade un evento al botón "reset" para que al hacer clic se envíe una petición POST al servidor
    document.getElementById("reset").addEventListener("click", function() {

        console.log("Enviando petición de reset al servidor");

        fetch("/reset/", {
            method: "POST"
        })
        .then(response => response.json())
        .then(data => {
            updateBoard();
        });
    });

    // Se actualiza el tablero
    function updateBoard() {
        const boardImage = document.getElementById("board-image"); // Se obtiene el elemento con el id "board-image"
        boardImage.src = "/board/image/?" + new Date().getTime(); // Se actualiza la imagen del tablero
    }

});
