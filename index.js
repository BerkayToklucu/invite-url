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

        // Renklendirme için değişiklikler
        if (data.result.includes("zaten başka bir sunucu tarafından kullanılıyor. Alternatif:")) {
            result.style.color = "yellow"; // Alternatif önerisi
        } else if (data.result.includes("zaten başka bir sunucu tarafından kullanılıyor, ancak uygun bir alternatif bulunamadı.")) {
            result.style.color = "red"; // Sunucu adı kullanılıyor, alternatif yok
        } else if (data.result.includes("kullanılabilir.")) {
            result.style.color = "green"; // Kullanılabilir
        }

        output.appendChild(result);
    })
    .catch(error => console.error('Error:', error));
}