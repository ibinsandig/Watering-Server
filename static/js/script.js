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

function controlPump(turnOn) {
    const action = turnOn ? 'on' : 'off';

    fetch('/api/pump-control', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ action: action })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Pumpenstatus aktualisiert:", data);
    })
    .catch(error => {
        console.error("Fehler beim Steuern der Pumpe:", error);
    });
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

function refreshPlotA() {
    const plotImg = document.getElementById("moistureA-plot");
    const timestamp = new Date().getTime();  
    plotImg.src = `/moistureA-plot?t=${timestamp}`;
}

function refreshPlotD() {
    const plotImg = document.getElementById("moistureD-plot");
    const timestamp = new Date().getTime();  
    plotImg.src = `/moistureD-plot?t=${timestamp}`;

}

// 3,1 Sekunden Aktualisierung
setInterval(refreshPlotA, 10000);
setInterval(refreshPlotD, 10000);

// 3 Sekunden Aktualisierung
setInterval(fetchLatestData, 3000);