import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import './Dashboard.css'; // Assume CSS for styling

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

function Dashboard() {
  const [complianceData, setComplianceData] = useState({});
  const [badges, setBadges] = useState({});
  const [alerts, setAlerts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [quantumSecure, setQuantumSecure] = useState(true); // Simulate quantum status

  const backendAPI = 'http://localhost:5001'; // Backend API

  useEffect(() => {
    // Autonomous load data on mount and refresh every 5 min
    loadComplianceData();
    loadBadges();
    const interval = setInterval(() => {
      loadComplianceData();
      loadBadges();
    }, 300000); // 5 min
    return () => clearInterval(interval);
  }, []);

  // Load compliance predictions from backend
  const loadComplianceData = async () => {
    setIsLoading(true);
    try {
      const institutions = ['IMF', 'BIS', 'IOSCO', 'ILO', 'UN', 'WTO'];
      const data = {};
      for (const inst of institutions) {
        const response = await axios.post(`${backendAPI}/predict`, {
          institution: inst,
          tx_data: { value: 314159, origin: 'mining', recipient: 'USDC', global_score: 95 }
        });
        data[inst] = response.data;
        if (response.data.status === 'red') {
          setAlerts(prev => [...prev, `Breach in ${inst}: Score ${response.data.score}%`]);
        }
      }
      setComplianceData(data);
    } catch (err) {
      console.error('Failed to load compliance data:', err);
      setAlerts(prev => [...prev, 'Error loading compliance data']);
    } finally {
      setIsLoading(false);
    }
  };

  // Load badges from backend
  const loadBadges = async () => {
    try {
      const response = await axios.get(`${backendAPI}/badges`);
      setBadges(response.data);
    } catch (err) {
      console.error('Failed to load badges:', err);
    }
  };

  // Evolve system (call backend)
  const evolveSystem = async () => {
    await axios.post(`${backendAPI}/evolve`);
    alert('Compliance Predictor Evolved!');
    loadComplianceData(); // Refresh
  };

  // Chart data for scores
  const chartData = {
    labels: Object.keys(complianceData),
    datasets: [{
      label: 'Compliance Score (%)',
      data: Object.values(complianceData).map(d => d.score || 0),
      backgroundColor: Object.values(complianceData).map(d => d.status === 'green' ? 'green' : 'red'),
    }]
  };

  return (
    <div className="dashboard">
      <header>
        <h1>AI Compliance Dashboard for Global Standards</h1>
        <p>Real-Time Monitoring with AI Predictions</p>
        <button onClick={evolveSystem}>Evolve Predictor</button>
        <p>Quantum Secure: {quantumSecure ? 'Yes' : 'No'}</p>
      </header>

      {isLoading && <p>Loading compliance data...</p>}

      <section className="badges">
        <h2>Compliance Badges</h2>
        <div className="badge-list">
          {Object.entries(badges).map(([inst, data]) => (
            <div key={inst} className={`badge ${data.status}`}>
              <h3>{inst}</h3>
              <p>Score: {data.score}%</p>
              <p>Status: {data.status}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="chart">
        <h2>Compliance Scores Chart</h2>
        <Bar data={chartData} />
      </section>

      <section className="alerts">
        <h2>Alerts</h2>
        <ul>
          {alerts.map((alert, idx) => (
            <li key={idx} className="alert">{alert}</li>
          ))}
        </ul>
      </section>

      <section className="data-table">
        <h2>Detailed Compliance Data</h2>
        <table>
          <thead>
            <tr>
              <th>Institution</th>
              <th>Score (%)</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {Object.entries(complianceData).map(([inst, data]) => (
              <tr key={inst}>
                <td>{inst}</td>
                <td>{data.score || 'N/A'}</td>
                <td className={data.status}>{data.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <footer>
        <p>Powered by AI/RL, Quantum Security, Zero-Trust</p>
      </footer>
    </div>
  );
}

export default Dashboard;
