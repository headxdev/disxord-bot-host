// api/templates.js
import { promises as fs } from 'fs';
import path from 'path';

export default async function handler(req, res) {
    if (req.method === 'GET') {
        try {
            // Lade templates.json
            const templatesPath = path.join(process.cwd(), 'cmdtamplates', 'templates.json');
            const templatesJson = await fs.readFile(templatesPath, 'utf-8');
            const templates = JSON.parse(templatesJson);

            // Lade alle Command-Implementierungen
            for (const [key, template] of Object.entries(templates.templates)) {
                // Python Implementation
                const pythonPath = path.join(process.cwd(), 'cmdtamplates', template.file);
                template.python = await fs.readFile(pythonPath, 'utf-8');

                // JavaScript Implementation
                const jsPath = path.join(process.cwd(), 'cmdtamplates', `${key}.js`);
                try {
                    template.javascript = await fs.readFile(jsPath, 'utf-8');
                } catch (e) {
                    template.javascript = '// JavaScript implementation coming soon';
                }

                // C# Implementation
                const csPath = path.join(process.cwd(), 'cmdtamplates', `${key}.cs`);
                try {
                    template.csharp = await fs.readFile(csPath, 'utf-8');
                } catch (e) {
                    template.csharp = '// C# implementation coming soon';
                }
            }

            res.status(200).json(templates);
        } catch (error) {
            console.error('Error loading templates:', error);
            res.status(500).json({ error: 'Failed to load templates' });
        }
    } else {
        res.status(405).json({ error: 'Method not allowed' });
    }
}
