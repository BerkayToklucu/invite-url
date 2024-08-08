function checkURL() {
    const keyword = document.getElementById("searchInput").value;
    fetch('/api/check_invite', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ keyword: keyword })
    })
    .then(response => response.json())
    .then(data => {
        const output = document.getElementById("output");
        const result = document.createElement("p");
        result.textContent = data.result;
        output.appendChild(result);
    })
    .catch(error => console.error('Error:', error));
}