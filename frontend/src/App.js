import { useEffect, useState } from 'react';
import { Tooltip, Cell, PieChart, Pie, Legend } from 'recharts';
import './App.css';

const API = '/api';

const LABEL_COLORS = {
  'Positive': '#4caf50',
  'Neutral': '#9e9e9e',
  'Negative': '#f44336',
};

function App() {
  const [stats, setStats] = useState(null);
  const [wordcloud, setWordcloud] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetch(`${API}/stats`).then(r => r.json()),
      fetch(`${API}/wordcloud`).then(r => r.json()),
    ]).then(([statsData, wcData]) => {
      setStats(statsData);
      setWordcloud(wcData.image);
    }).finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="loading">Loading sentiment data...</div>;

  const categoryData = Object.entries(stats.category_counts).map(([name, value]) => ({
    name, value, fill: LABEL_COLORS[name] || '#999'
  }));

  return (
    <div className="app">
      <header className="header">
        <h1>LRT3 Sentiment Analysis</h1>
        <p className="subtitle">Twitter sentiment analysis of Malaysia's LRT3 Shah Alam Line</p>
      </header>

      <div className="stats-row">
        <StatCard label="Total Tweets" value={stats.total} />
        <StatCard label="Latest Tweet" value={new Date(stats.latest_date).toLocaleDateString('en-MY', { year: 'numeric', month: 'short', day: 'numeric' })} />
        <StatCard label="Avg Confidence" value={(stats.avg_confidence * 100).toFixed(1) + '%'} />
      </div>

      <div className="card">
        <h2>Sentiment Categories</h2>
        <div className="chart-box">
          <PieChart width={500} height={300}>
            <Pie data={categoryData} dataKey="value" nameKey="name" label={({ name, value, percent }) => `${name}: ${value} (${(percent * 100).toFixed(0)}%)`}>
              {categoryData.map((entry, i) => (
                <Cell key={i} fill={entry.fill} />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </div>
      </div>

      <div className="card full-width">
        <h2>Word Cloud</h2>
        <div className="wordcloud-container">
          <img src={wordcloud} alt="Word Cloud" className="wordcloud-img" />
        </div>
      </div>

    </div>
  );
}

function StatCard({ label, value }) {
  return (
    <div className="stat-card">
      <div className="stat-value">{value}</div>
      <div className="stat-label">{label}</div>
    </div>
  );
}

export default App;
