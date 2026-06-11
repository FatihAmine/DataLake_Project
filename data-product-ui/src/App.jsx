import React, { useState, useEffect } from 'react';
import { 
  Database, 
  LayoutDashboard, 
  TrendingUp, 
  ShoppingCart, 
  Layers,
  RefreshCw,
  DollarSign
} from 'lucide-react';
import { 
  AreaChart, 
  Area, 
  BarChart,
  Bar,
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer 
} from 'recharts';
import { ClickHouseService } from './services/ClickHouseService';
import './App.css';

function App() {
  const [isOnline, setIsOnline] = useState(false);
  const [loading, setLoading] = useState(true);
  
  // Data state
  const [metrics, setMetrics] = useState({ total_lines: 0, total_revenue: 0, total_orders: 0 });
  const [salesPerDay, setSalesPerDay] = useState([]);
  const [salesByCategory, setSalesByCategory] = useState([]);
  const [topProducts, setTopProducts] = useState([]);

  const fetchData = async () => {
    setLoading(true);
    try {
      const online = await ClickHouseService.ping();
      setIsOnline(online);
      
      if (online) {
        const [overall, perDay, byCategory, top] = await Promise.all([
          ClickHouseService.getOverallMetrics(),
          ClickHouseService.getSalesPerDay(),
          ClickHouseService.getSalesByCategory(),
          ClickHouseService.getTopProducts()
        ]);
        
        setMetrics(overall || { total_lines: 0, total_revenue: 0, total_orders: 0 });
        setSalesPerDay(perDay || []);
        setSalesByCategory(byCategory || []);
        setTopProducts(top || []);
      }
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 30000); // Poll every 30s
    return () => clearInterval(interval);
  }, []);

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(value || 0);
  };

  const formatNumber = (value) => {
    return new Intl.NumberFormat('en-US').format(value || 0);
  };

  return (
    <div className="app-container">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-logo">
          <Database size={28} />
          <span>SalesProduct</span>
        </div>
        
        <nav className="nav-menu">
          <a className="nav-item active">
            <LayoutDashboard size={20} />
            Dashboard
          </a>
        </nav>
      </aside>

      <main className="main-content">
        <header className="header">
          <h1>Sales Data Product Views</h1>
          
          <div className="header-actions">
            <button className="btn btn-secondary" onClick={fetchData} disabled={loading}>
              <RefreshCw size={18} className={loading ? 'spin' : ''} />
              {loading ? 'Refreshing...' : 'Refresh'}
            </button>
            
            <div className="connection-status glass-panel">
              <span className={`status-dot ${isOnline ? 'online' : 'offline'}`}></span>
              {isOnline ? 'Connected to ClickHouse' : 'Offline'}
            </div>
          </div>
        </header>

        <div className="dashboard animate-fade-in">
          {/* Counters / Metrics Grid */}
          <div className="metrics-grid">
            <div className="metric-card glass-panel">
              <Layers className="metric-icon" size={24} />
              <span className="metric-title">Days Recorded</span>
              <span className="metric-value">{formatNumber(metrics.total_lines)}</span>
            </div>
            
            <div className="metric-card glass-panel">
              <DollarSign className="metric-icon" size={24} />
              <span className="metric-title">Total Revenue</span>
              <span className="metric-value">{formatCurrency(metrics.total_revenue)}</span>
            </div>
            
            <div className="metric-card glass-panel">
              <ShoppingCart className="metric-icon" size={24} />
              <span className="metric-title">Total Units Sold</span>
              <span className="metric-value">{formatNumber(metrics.total_orders)}</span>
            </div>
          </div>

          <div className="charts-grid">
            <div className="chart-panel glass-panel">
              <h3>Sales Per Day</h3>
              <div className="chart-container">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={salesPerDay} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                    <defs>
                      <linearGradient id="colorRevenue" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="var(--primary-color)" stopOpacity={0.8}/>
                        <stop offset="95%" stopColor="var(--primary-color)" stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                    <XAxis dataKey="date" stroke="var(--text-secondary)" tick={{fontSize: 12}} />
                    <YAxis stroke="var(--text-secondary)" tickFormatter={(val) => `$${val / 1000}k`} tick={{fontSize: 12}} />
                    <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" vertical={false} />
                    <Tooltip 
                      contentStyle={{ backgroundColor: 'var(--bg-surface)', borderColor: 'var(--border-color)', borderRadius: '8px' }}
                      itemStyle={{ color: 'var(--text-primary)' }}
                      formatter={(value) => formatCurrency(value)}
                    />
                    <Area type="monotone" dataKey="revenue" stroke="var(--primary-color)" fillOpacity={1} fill="url(#colorRevenue)" />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className="chart-panel glass-panel">
              <h3>Sales by Category </h3>
              <div className="chart-container">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={salesByCategory} margin={{ top: 10, right: 30, left: 0, bottom: 0 }} layout="vertical">
                    <XAxis type="number" stroke="var(--text-secondary)" tickFormatter={(val) => `$${val / 1000}k`} tick={{fontSize: 12}} />
                    <YAxis dataKey="category" type="category" stroke="var(--text-secondary)" tick={{fontSize: 12}} width={100} />
                    <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" horizontal={false} />
                    <Tooltip 
                      contentStyle={{ backgroundColor: 'var(--bg-surface)', borderColor: 'var(--border-color)', borderRadius: '8px' }}
                      itemStyle={{ color: 'var(--text-primary)' }}
                      formatter={(value) => formatCurrency(value)}
                    />
                    <Bar dataKey="revenue" fill="var(--accent-color)" radius={[0, 4, 4, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>

          {/* Top Products Table */}
          <div className="chart-panel glass-panel">
            <h3>Top Products</h3>
            <div className="data-table-container">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Product Name</th>
                    <th>Total Units Sold</th>
                    <th>Total Revenue</th>
                  </tr>
                </thead>
                <tbody>
                  {topProducts.map((product, i) => (
                    <tr key={i}>
                      <td>{product.product}</td>
                      <td>{formatNumber(product.total_units)}</td>
                      <td style={{ color: 'var(--success)', fontWeight: 600 }}>
                        {formatCurrency(product.amount)}
                      </td>
                    </tr>
                  ))}
                  {topProducts.length === 0 && (
                    <tr>
                      <td colSpan="3" style={{ textAlign: 'center', padding: '2rem' }}>No data available in view</td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
