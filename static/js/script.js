console.log("Laden script.js");

// Funktion zum zum Wechseln der Webpage
function ZumBedienpanel(){
    window.location.href = "/control";
}
function ZurMainpage(){
    window.location.href = "/";
}

// Funktion zum Steuern der Pumpe
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

// Funktion zum Laden der letzten Feuchtigkeitsdaten
/*
function fetchLatestData() {
    fetch('/api/latest-data')
        .then(response => response.json())
        .then(data => {
            console.log("Received data:", data);
            if (data.topic === "watering/status") {
                // Beispiel: payload = "moisture:45,pump:on"
                const parts = data.payload.split(',');
                let moistureA = '--';
                let moistureD = '--';
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

//Funktion zum Abrufen des letzten Pumpenstatus
function fetchPumpStatus() {
    fetch('/api/latest-pump')
        .then(response => response.json())
        .then(data => {
            let status = '--';
            if (data.payload === "1") status = "EIN";
            if (data.payload === "0") status = "AUS";
            document.getElementById("pump-status").textContent = status;
        })
        .catch(error => {
            console.error("Fehler beim Abrufen des Pumpenstatus:", error);
        });
}

*/

// Funktion zum Aktualisieren von PlotA und PlotD
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

// Trigger-Wert abfragen
function fetchTrigger() {
    fetch('/api/trigger')
        .then(response => response.json())
        .then(data => {
            document.getElementById("trigger-value").textContent = data.value !== null ? data.value : '--';
        });
}

// Trigger-Wert setzen
function setTrigger() {
    const value = document.getElementById("trigger-input").value;
    if (!value) return;
    fetch('/api/trigger', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ value: value })
    })
    .then(response => response.json())
    .then(data => {
        fetchTrigger();
        document.getElementById("trigger-input").value = '';
    });
}

// Intiales Laden der Plots und Daten
document.addEventListener('DOMContentLoaded', function() {
    refreshPlotA();
    refreshPlotD();
    fetchLatestData();
    fetchTrigger();
});

// 10 Sekunden Aktualisierung für Plots
// eine gewisse Differenz zwischen den Aktualisierungen der Plots muss gegeben sein, damit sie sich nicht gegenseitig überschreiben
setInterval(refreshPlotA, 11000);
setInterval(refreshPlotD, 10000);

// 0,5 Sekunden Aktualisierung für aktuelle Daten
setInterval(fetchLatestData, 500);

// Rufe fetchPumpStatus regelmäßig auf, z.B. alle 0,5 Sekunden:
setInterval(fetchPumpStatus, 500);

// Trigger-Wert regelmäßig abfragen
setInterval(fetchTrigger, 1000);
document.addEventListener('DOMContentLoaded', fetchTrigger);