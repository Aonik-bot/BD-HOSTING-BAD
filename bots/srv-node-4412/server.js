const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

app.get('/', (req, res) => {
  res.json({
    service: 'AONIK Node API Service',
    status: 'operational',
    node: 'Edge-SG-02',
    timestamp: new Date().toISOString()
  });
});

app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', uptime: process.uptime(), memory: process.memoryUsage() });
});

app.listen(PORT, () => {
  console.log(`[AONIK HOSTING] Node.js server running on port ${PORT}`);
});
