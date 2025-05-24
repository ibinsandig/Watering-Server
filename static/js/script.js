console.log("Laden script.js");

function ZumBedienpanel(){
    window.location.href = "/control";
}
function ZurMainpage(){
    window.location.href = "/";
}
function ZurInfo(){
    window.location.href = "/info";
}

function fetchLatestData() {
    fetch('/api/latest-data')
        .then(response => response.json())
        .then(data => {
            console.log("Received data:", data);
            if (data.topic === "watering/status") {
                // Beispiel: payload = "moisture:45,pump:on"
                const parts = data.payload.split(',');
                let moisture = '--';
                let pump = '--';
                
                parts.forEach(p => {
                    if (p.startsWith('moisture:')) {
                        moisture = p.split(':')[1];
                    }
                    if (p.startsWith('pump:')) {
                        pump = p.split(':')[1] === 'on' ? 'EIN' : 'AUS';
                    }
                });

                document.getElementById("moisture").textContent = moisture;
                document.getElementById("pump-status").textContent = pump;
            }
        });
}

// Rufe es alle 3 Sekunden auf
setInterval(fetchLatestData, 3000);
