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
                    // Unterstützung für verschiedene Moisture-Typen
                    if (p.startsWith('moisture:') || p.startsWith('moistureA:')) {
                        moistureA = p.split(':')[1];
                    }
                    if (p.startsWith('moistureD:')) {
                        moistureD = p.split(':')[1];
                    }
                    if (p.startsWith('pump:')) {
                        pump = p.split(':')[1] === 'on' ? 'EIN' : 'AUS';
                    }
                    
                });

                document.getElementById("moistureA").textContent = moistureA;
                document.getElementById("moistureD").textContent = moistureD;
                document.getElementById("pump-status").textContent = pump;
            }
        })
        .catch(error => {
            console.error("Fehler beim Abrufen der Daten:", error);
        });
}

function refreshPlotA() {
    const plotImg = document.getElementById("moistureA-plot");
    if (plotImg) {
        const timestamp = new Date().getTime();  
        plotImg.src = `/moistureA-plot?t=${timestamp}`;
        console.log("RefreshPlotA aufgerufen:", plotImg.src);
    }
}

function refreshPlotD() {
    const plotImg = document.getElementById("moistureD-plot");
    if (plotImg) {
        const timestamp = new Date().getTime();  
        plotImg.src = `/moistureD-plot?t=${timestamp}`;
        console.log("RefreshPlotD aufgerufen:", plotImg.src);
    }
}

// Initiale Aktualisierung beim Laden der Seite
document.addEventListener('DOMContentLoaded', function() {
    refreshPlotA();
    refreshPlotD();
    fetchLatestData();
});

// 10 Sekunden Aktualisierung für Plots
setInterval(refreshPlotA, 11000);
setInterval(refreshPlotD, 10000);

// 3 Sekunden Aktualisierung für aktuelle Daten
setInterval(fetchLatestData, 3000);