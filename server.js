const express = require('express');
const path = require('path');
const fs = require('fs').promises;
const app = express();
const PORT = 3000;

// Serve static files
app.use(express.static('.'));

// Endpoint to get dashboard data
app.get('/api/dashboard', async (req, res) => {
    try {
        // Read the dashboard files and return as JSON
        const dashboardData = {
            timestamp: new Date().toISOString(),
            files: {
                'enhanced-command-center': await readFileIfExists('enhanced-command-center.md'),
                'command-center': await readFileIfExists('command-center.md'),
                'dashboard': await readFileIfExists('dashboard.md'),
                'task-tracker': await readFileIfExists('task-tracker.md')
            },
            systemStatus: {
                productivityIndex: 87,
                automationLevel: 'High',
                aiEngagement: 'Active',
                missionStatus: 'Operational',
                toolsInstalled: 10,
                skillsAvailable: 50,
                systemsIntegrated: 6,
                automationPotential: 'Very High'
            }
        };
        
        res.json(dashboardData);
    } catch (error) {
        console.error('Error reading dashboard data:', error);
        res.status(500).json({ error: 'Failed to read dashboard data' });
    }
});

// Helper function to read file if it exists
async function readFileIfExists(filePath) {
    try {
        const content = await fs.readFile(filePath, 'utf8');
        return content;
    } catch (error) {
        if (error.code === 'ENOENT') {
            return `File ${filePath} not found`;
        }
        throw error;
    }
}

// Serve the main dashboard page
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'dashboard.html'));
});

// Start the server
app.listen(PORT, () => {
    console.log(`🚀 Netto.AI Dashboard Server running at http://localhost:${PORT}`);
    console.log(`Access your dashboard at: http://localhost:${PORT}`);
    console.log('Press Ctrl+C to stop the server');
});

module.exports = app;